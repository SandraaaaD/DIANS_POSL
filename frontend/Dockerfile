#FROM ubuntu:latest
#LABEL authors="Sandra"
#
#ENTRYPOINT ["top", "-b"]

# 1. База: користиме Node image
FROM node:20

# 2. Работна папка во контейнерот
WORKDIR /app

# 3. Копирај package.json и package-lock.json
COPY package*.json ./

# 4. Инсталирај dependencies
RUN npm install

# 5. Копирај го цел src и public
COPY public ./public
COPY src ./src

# 6. Build на React апликацијата
RUN npm run build

# 7. Користиме nginx за да го сервираме build
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html

# 8. Отворен порт
EXPOSE 80

# 9. Команда за стартување на nginx
CMD ["nginx", "-g", "daemon off;"]
