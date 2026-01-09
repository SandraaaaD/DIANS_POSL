package com.example.demo.model;


import jakarta.persistence.*;
import lombok.*;

import java.io.Serializable;
import java.time.LocalDate;

@Data
@Entity
@Table(name = "ohlcv")
@NoArgsConstructor
@AllArgsConstructor

@Getter
@Setter
@IdClass(DataModelId.class)
public class dataModel {

//    @Id
//    @GeneratedValue(strategy = GenerationType.IDENTITY)
//    private Long id;

    @Id
    @Column(name = "symbol")
    private String symbol;

    @Id
    @Column(name = "date")
//    @Temporal(TemporalType.DATE)
    private LocalDate date;  

    @Column(name = "open")
    private Double open;

    @Column(name = "high")  
    private Double high;     

    @Column(name = "low")
    private Double low;

    @Column(name = "close")
    private Double close;

    @Column(name = "volume")
    private Double volume;

    @Column(name = "lastprice")  
    private Double lastPrice;

    @Column(name = "quotevolume")  
    private Double quoteVolume;

    @Column(name = "count")
    private Integer count;

    public void setHigh(double high) {
        this.high=high;
    }
}

@Data
class DataModelId implements Serializable {
    private String symbol;
    private LocalDate date;
}
