package com.example.demo.repository;

import com.example.demo.model.dataModel;
import lombok.NonNull;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface dataModelRepository extends JpaRepository<dataModel,Long> {
    @NonNull
    List<dataModel>findAll();
    List<dataModel> findAllByCountLessThan(int br);
    @NonNull
    Optional<dataModel> findById(Long id);
    List<dataModel> findBySymbol(@Param("symbol") String name);
}
