package com.mission.missionservice.controller;

import com.mission.missionservice.service.OrderService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

// Kata: the controller layer. Constructor-inject an OrderService, and add a
// @GetMapping("/orders/{ticker}/fee") method that takes the ticker as a
// @PathVariable and the trade value as a @RequestParam double tradeValue,
// then returns service.calculateFee(ticker, tradeValue).
//
// Try: curl "http://localhost:8080/orders/AAPL/fee?tradeValue=10000"
@RestController
public class OrderController {

    // TODO: add a private final OrderService field, and a constructor that
    // accepts one and assigns it.
    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    // TODO: add the @GetMapping method described above.
    @GetMapping("/orders/{ticker}/fee")
    public Map<String, Double> calculateFee(@PathVariable String ticker, @RequestParam Double tradeValue) {
        return orderService.calculateFee(ticker, tradeValue);
    }
}
