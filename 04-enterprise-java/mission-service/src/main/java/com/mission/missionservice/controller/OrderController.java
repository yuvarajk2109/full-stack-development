package com.mission.missionservice.controller;

import com.mission.missionservice.dto.FeeResponseDto;
import com.mission.missionservice.dto.OrderRequestDto;
import com.mission.missionservice.dto.OrderResponseDto;
import com.mission.missionservice.service.OrderService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

// Kata: the controller layer. Constructor-inject an OrderService, and add a
// @GetMapping("/orders/{ticker}/fee") method that takes the ticker as a
// @PathVariable and the trade value as a @RequestParam double tradeValue,
// then returns service.calculateFee(ticker, tradeValue).
//
// Try: curl "http://localhost:8080/orders/AAPL/fee?tradeValue=10000"
@RestController
@RequestMapping("/orders")
public class OrderController {

    // TODO: add a private final OrderService field, and a constructor that
    // accepts one and assigns it.
    private final OrderService orderService;
    private final Map<String, OrderResponseDto> orders = new ConcurrentHashMap<>();
    private final AtomicInteger idSequence = new AtomicInteger(1);

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    // TODO: add the @GetMapping method described above.
    @GetMapping("/{ticker}/fee")
    public ResponseEntity<FeeResponseDto> calculateFee(@PathVariable String ticker, @RequestParam Double tradeValue) {
        FeeResponseDto response = new FeeResponseDto(orderService.calculateFee(ticker, tradeValue));
        return ResponseEntity.ok(response);
    }

    @GetMapping("/{id}")
    public ResponseEntity<OrderResponseDto> getOrder(@PathVariable String id) {
        OrderResponseDto order = orders.get(id);
        if (order == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(order);
    }

    @PostMapping
    public ResponseEntity<OrderResponseDto> submitOrder(@Valid @RequestBody OrderRequestDto request) {
        double tradeValue = request.quantity() * request.price();
        double fee = orderService.calculateFee(request.ticker(), tradeValue);
        String id = String.valueOf(idSequence.getAndIncrement());
        OrderResponseDto response = new OrderResponseDto(id, "ACCEPTED", fee, null);

        URI location = URI.create("/orders/" + id);
        return ResponseEntity.created(location).body(response);
    }
}
