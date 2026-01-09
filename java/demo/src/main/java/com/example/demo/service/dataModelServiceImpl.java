package com.example.demo.service;

import com.example.demo.model.dataModel;
import com.example.demo.repository.dataModelRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class dataModelServiceImpl implements dataModelService{
    private final dataModelRepository dataModelRepository;

    public dataModelServiceImpl(com.example.demo.repository.dataModelRepository dataModelRepository) {
        this.dataModelRepository = dataModelRepository;
    }


    @Override
    public List<dataModel> findAll() {
        return dataModelRepository.findAll();
    }

    @Override
    public List<dataModel> findAllByCountLessThan(int br) {
        return dataModelRepository.findAllByCountLessThan(br);
    }

    @Override
    public Optional<dataModel> findById(Long id) {
        return dataModelRepository.findById(id);
    }

    @Override
    public List<dataModel> findBySymbol(String name) {
        return dataModelRepository.findBySymbol(name);
    }

}
