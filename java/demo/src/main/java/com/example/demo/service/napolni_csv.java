//package com.example.demo.service;
//
//import com.example.demo.model.dataModel;
//import com.example.demo.repository.dataModelRepository;
//import jakarta.annotation.PostConstruct;
//import org.springframework.stereotype.Service;
//
//import java.io.BufferedReader;
//import java.io.File;
//import java.io.FileReader;
//
//@Service
//public class napolni_csv {
//    private final dataModelRepository dataModelRepository;
//
//    public napolni_csv(com.example.demo.repository.dataModelRepository dataModelRepository) {
//        this.dataModelRepository = dataModelRepository;
//    }
//
//    @PostConstruct
//    public void loadCsv() throws Exception {
//        File file = new File("C:\\Users\\Administrator\\Downloads\\demo (2)\\demo\\src\\main\\resources\\ohlcv.csv");
//
//        if (!file.exists()) {
//            System.out.println("CSV not found!");
//            return;
//        }
//
//        BufferedReader reader = new BufferedReader(new FileReader(file));
//        String line;
//        reader.readLine();
//
//        while ((line = reader.readLine()) != null) {
//            String[] p = line.split(",");
//
//            dataModel d = new dataModel();
//            d.setSymbol(p[0]);
//            d.setDate(p[1]);
//            d.setOpen(Double.parseDouble(p[2]));
//            d.setHigh(Double.parseDouble(p[3]));
//            d.setLow(Double.parseDouble(p[4]));
//            d.setClose(Double.parseDouble(p[5]));
//            d.setVolume(Double.parseDouble(p[6]));
//            d.setLastPrice(Double.parseDouble(p[7]));
//            d.setQuoteVolume(Double.parseDouble(p[8]));
//            d.setCount(Integer.parseInt(p[9]));
//
//            dataModelRepository.save(d);
//        }
//
//        System.out.println("CSV IMPORT DONE!");
//    }
//}
