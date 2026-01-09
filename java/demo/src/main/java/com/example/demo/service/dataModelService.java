package com.example.demo.service;

import com.example.demo.model.dataModel;

import java.util.List;
import java.util.Optional;

public interface dataModelService {
    List<dataModel> findAll();
    List<dataModel> findAllByCountLessThan(int br);
    Optional<dataModel> findById(Long id);
    List<dataModel> findBySymbol(String name);
}
