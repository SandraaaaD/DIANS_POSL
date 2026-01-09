import asyncio
import sys
import aiohttp
import time
from datetime import datetime, timedelta, date
import asyncpg

DB_CONFIG = {
    'host': 'my_postgres',
    'port': 5432,
    'user': 'postgres',
    'password': 'postgres',
    'database': 'dians_baza',
}

# DB_CONFIG = { 'host': 'das-db-2026.postgres.database.azure.com',
#               'port': 5432,
#               'user': 'postgres',
#               'password': 'sd7589F!nk!',
#               'database': 'example_db',
#               }

STABILNI = ['USDT', 'BUSD', 'USDC', 'DAI', 'TUSD', 'USDP', 'USD']
KRAJ = object()


async def filter1(sesija, izlez):
    odg = await sesija.get("https://api.binance.com/api/v3/ticker/24hr")
    podaci = await odg.json(content_type=None)

    validni = []
    for t in podaci:
        try:
            quoteVolume = float(t.get('quoteVolume', 0))
            volume = float(t.get('volume', 0))
            count = float(t.get('count', 0))
            symbol = t.get('symbol', '')
        except:
            continue

        if quoteVolume >= 500 and volume > 0 and count > 0 and any(symbol.endswith(q) for q in STABILNI):
            validni.append(symbol)

    for sym in validni[:1000]:
        await izlez.put(sym)
    await izlez.put(KRAJ)


async def filter2(vlez, izlez, db_pool):
    while True:
        sym = await vlez.get()
        if sym is KRAJ:
            for _ in range(NUM_PIPELINES):
                await izlez.put(KRAJ)
            break

        async with db_pool.acquire() as conn:
            rez = await conn.fetchrow(
                "SELECT MAX(date) FROM ohlcv WHERE symbol = $1",
                sym
            )

        if rez and rez['max']:
            posleden_datum = rez['max']
            if isinstance(posleden_datum, date):
                if posleden_datum >= (datetime.now().date() - timedelta(days=2)):
                    continue
            else:
                if posleden_datum.date() >= (datetime.now().date() - timedelta(days=2)):
                    continue
        else:
            posleden_datum = None

        await izlez.put((sym, posleden_datum))


async def filter3(sesija, vlez, db, semafor):
    while True:
        nes = await vlez.get()
        if nes is KRAJ:
            await db.put(KRAJ)
            break

        sym, posleden_datum = nes

        if posleden_datum is None:
            start_date = datetime(2015, 1, 1)
            print(f"Симбол {sym}: Нема податоци во базата, започнувам од 2015")
        else:
            if isinstance(posleden_datum, date):
                start_date = datetime.combine(posleden_datum, datetime.min.time()) + timedelta(days=1)
            else:
                start_date = posleden_datum + timedelta(days=1)

            days_to_update = (datetime.now().date() - start_date.date()).days
            if days_to_update <= 0:
                continue
            print(f"Симбол {sym}: Ажурирам {days_to_update} денови од {start_date.date()}")

        start_ms = int(start_date.timestamp() * 1000)
        end_ms = int(datetime.now().timestamp() * 1000)

        if start_ms >= end_ms:
            continue

        redovi = []
        async with semafor:
            next_start = start_ms
            batch_count = 0
            while next_start < end_ms:
                params = {
                    "symbol": sym,
                    "interval": "1d",
                    "startTime": next_start,
                    "endTime": end_ms,
                    "limit": 1000
                }

                try:
                    response = await sesija.get("https://api.binance.com/api/v3/klines", params=params)
                    data = await response.json(content_type=None)

                    if not data or (isinstance(data, dict) and 'code' in data):
                        break

                    batch_count += 1
                    for d in data:
                        try:
                            dt_obj = datetime.fromtimestamp(d[0] / 1000)
                            dt_date = dt_obj.date()
                            redovi.append((
                                sym,
                                dt_date,
                                float(d[1]), float(d[2]), float(d[3]), float(d[4]),
                                float(d[5]), float(d[4]), float(d[7]), int(d[8])
                            ))
                        except:
                            continue

                    if data:
                        posledno = data[-1][0]
                    else:
                        posledno = None

                    if posledno is None or posledno <= next_start:
                        break

                    next_start = posledno + 1
                    await asyncio.sleep(0.01)

                except Exception as e:
                    print(f"Грешка при преземање на податоци за {sym}: {e}")
                    break

        if redovi:
            print(f"Симбол {sym}: Преземени {len(redovi)} нови записи")
            for r in redovi:
                await db.put(r)
        else:
            print(f"Симбол {sym}: Нема нови податоци за преземање")


async def zapisuvac(database, db_pool):
    async with db_pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS ohlcv (
                symbol TEXT,
                date DATE,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                lastPrice REAL,
                quoteVolume REAL,
                count INTEGER,
                PRIMARY KEY (symbol, date)
            )
        ''')

        await conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_symbol_date 
            ON ohlcv(symbol, date DESC)
        ''')

        paket = []
        total = 0
        simboli = {}

        while True:
            stavka = await database.get()
            if stavka is KRAJ:
                if paket:
                    await conn.executemany(
                        '''
                        INSERT INTO ohlcv 
                        (symbol, date, open, high, low, close, volume, lastPrice, quoteVolume, count)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                        ON CONFLICT (symbol, date) DO NOTHING
                        ''',
                        paket
                    )
                    total += len(paket)
                    print(f"Зачувани {total} записи")
                break

            paket.append(stavka)

            symbol = stavka[0]
            if symbol not in simboli:
                simboli[symbol] = 0
            simboli[symbol] += 1

            if len(paket) >= 10000:
                await conn.executemany(
                    '''
                    INSERT INTO ohlcv 
                    (symbol, date, open, high, low, close, volume, lastPrice, quoteVolume, count)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                    ON CONFLICT (symbol, date) DO NOTHING
                    ''',
                    paket
                )
                total += len(paket)
                print(f"Зачувани {total} записи")
                paket = []

        print(f"\nСтатистика за ажурирање:")
        print(f"Вкупно записи: {total}")
        print(f"Вкупно симболи: {len(simboli)}")
        for sym, count in list(simboli.items())[:10]:  # Прикажи само првите 10
            print(f"  {sym}: {count} записи")


async def proveri_sostojba_na_bazata(db_pool):
    async with db_pool.acquire() as conn:
        result = await conn.fetchrow("SELECT COUNT(*) as count FROM ohlcv")
        total_records = result['count'] if result else 0

        result = await conn.fetchrow("SELECT COUNT(DISTINCT symbol) as count FROM ohlcv")
        total_symbols = result['count'] if result else 0

        result = await conn.fetchrow("SELECT MAX(date) as latest_date FROM ohlcv")
        latest_date = result['latest_date'] if result and result['latest_date'] else None

        print(f"Тековна состојба на базата:")
        print(f"  Вкупно записи: {total_records}")
        print(f"  Вкупно симболи: {total_symbols}")
        print(f"  Најнов датум: {latest_date}")

        if latest_date:
            if isinstance(latest_date, date):
                days_since_update = (datetime.now().date() - latest_date).days
            else:
                days_since_update = (datetime.now().date() - latest_date.date()).days

            print(f"  Денови од последно ажурирање: {days_since_update}")

            if days_since_update <= 1:
                print(f"  Базата е ажурирана! Ќе се проверат само симболите што недостасуваат.")
            elif days_since_update > 30:
                print(f"  Внимание: Базата не е ажурирана повеќе од 30 дена!")
            else:
                print(f"  Базата ќе се ажурира за последните {days_since_update} дена.")


NUM_PIPELINES = 50

async def run_update():
    print("\nupdate:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    pocetno_vreme = time.time()

    try:
        db_pool = await asyncpg.create_pool(**DB_CONFIG)
    except Exception as e:
        print(f"Грешка при поврзување со Postgres: {e}")
        return

    # -------------------------------------------------------
    async with db_pool.acquire() as conn:
        await conn.execute('''
                           CREATE TABLE IF NOT EXISTS ohlcv
                           (
                               symbol
                               TEXT,
                               date
                               DATE,
                               open
                               REAL,
                               high
                               REAL,
                               low
                               REAL,
                               close
                               REAL,
                               volume
                               REAL,
                               lastPrice
                               REAL,
                               quoteVolume
                               REAL,
                               count
                               INTEGER,
                               PRIMARY
                               KEY
                           (
                               symbol,
                               date
                           )
                               )
                           ''')
        await conn.execute('''
                           CREATE INDEX IF NOT EXISTS idx_symbol_date
                               ON ohlcv(symbol, date DESC)
                           ''')
    # -------------------------------------------------------

    await proveri_sostojba_na_bazata(db_pool)

    filter1_queue = asyncio.Queue()
    filter2_queue = asyncio.Queue()
    db_queue = asyncio.Queue()

    sem = asyncio.Semaphore(50)

    async with aiohttp.ClientSession() as sesija:
        writer = asyncio.create_task(zapisuvac(db_queue, db_pool))
        f1 = asyncio.create_task(filter1(sesija, filter1_queue))
        f2 = asyncio.create_task(filter2(filter1_queue, filter2_queue, db_pool))
        f3 = [
            asyncio.create_task(filter3(sesija, filter2_queue, db_queue, sem))
            for _ in range(NUM_PIPELINES)
        ]

        await asyncio.gather(f1, f2, *f3)
        await writer

    await db_pool.close()

    print(f"Update заврши за {time.time() - pocetno_vreme:.1f} секунди")

async def main():
    print("Binance updater стартуван (на секои 10 минути)")
    print("=" * 60)

    while True:
        start = time.time()

        await run_update()

        elapsed = time.time() - start
        sleep_time = max(0, 200 - elapsed)

        print(f" Следен update за {sleep_time:.1f} секунди\n")
        await asyncio.sleep(sleep_time)


if __name__ == "__main__":
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())