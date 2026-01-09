package com.example.demo.controller;

import com.example.demo.model.dataModel;
import com.example.demo.service.dataModelService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@CrossOrigin(origins = {"http://localhost:3000", "*"})
@RestController
@RequestMapping(value = "/api")
@Validated


public class dataModelController {

    private final dataModelService dataModelService;

    public dataModelController(dataModelService dataModelService) {
        this.dataModelService = dataModelService;
    }

    @GetMapping("/all")
    public ResponseEntity<List<dataModel>> getAll() {
        List<dataModel> list = dataModelService.findAll();
        return new ResponseEntity<>(list, HttpStatus.OK);
    }

    @GetMapping("/countLessThan/{br}")
    public ResponseEntity<List<dataModel>> getAllByCountLessThan(@PathVariable int br) {
        List<dataModel> list = dataModelService.findAllByCountLessThan(br);
        return new ResponseEntity<>(list, HttpStatus.OK);
    }

    @GetMapping("/symbol/{symbol}")
    public ResponseEntity<List<dataModel>> getBySymbol(@PathVariable String symbol) {
        List<dataModel> list = dataModelService.findBySymbol(symbol);
        if (list.isEmpty()) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        return ResponseEntity.ok(list);
    }

    @GetMapping("/{id}")
    public ResponseEntity<dataModel> getById(@PathVariable Long id) {
        Optional<dataModel> result = dataModelService.findById(id);
        return result.map(dataModel -> new ResponseEntity<>(dataModel, HttpStatus.OK))
                .orElseGet(() -> new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }
}
//public class dataModelContorller {
//    private final dataModelService dataModelService;
//
//    public dataModelContorller(com.example.demo.service.dataModelService dataModelService) {
//        this.dataModelService = dataModelService;
//    }
//
//    @GetMapping("/all")
//    public String getAll(){
//        dataModelService.findAll();
//        return "redirect:/all";
//    }
//    @GetMapping("/lessThan")
//    public String getAllCountLessThan(@PathVariable int br){
//        dataModelService.findAllByCountLessThan(br);
//        return "redirect:/lessThan";
//    }
//
//    @GetMapping("/api/{id}")
//    public String showById(@PathVariable Long id, Model model){
//        Optional<dataModel> dataModel=dataModelService.findById(id);
//        model.addAttribute("tochen","tochen");
//        return "details";
//    }
//
//}
