package com.mission.missionservice.service;

import com.mission.missionservice.dto.FeeResponseDto;
import com.mission.missionservice.repository.OrderRepository;
import org.springframework.stereotype.Service;

import java.util.Map;

// Kata: the service layer. Constructor-inject an OrderRepository (no
// @Autowired needed - a single constructor is enough), and implement
// calculateFee(ticker, tradeValue) as tradeValue * repository.findFeeRate(ticker).
// See OrderServiceTest.java for the exact behaviour expected.
@Service
public class OrderService {

    // TODO: add a private final OrderRepository field, and a constructor
    // that accepts one and assigns it.
    private final OrderRepository orderRepository;

    public OrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    public Double calculateFee(String ticker, Double tradeValue) {
        Double feeRate = orderRepository.findFeeRate(ticker);
        return tradeValue * feeRate;
    }
}
