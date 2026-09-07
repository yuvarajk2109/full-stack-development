package com.mission.missionservice.repository;

import org.springframework.stereotype.Repository;

import java.util.HashMap;
import java.util.Map;
import java.util.NoSuchElementException;

@Repository
public class PortfolioRepositoryInMemoryImpl implements PortfolioRepository {

    private static final Map<String, Double> portfolio = Map.of(
            "P1", 1000.00,
            "P2", 5000.00,
            "P3", 10000.00
    );

    @Override
    public Double findTotalPortfolioValue(String clientId) {
        Double value = portfolio.get(clientId);
        if (value == null) {
            throw new NoSuchElementException("Client with " +  clientId + " not found");
        }
        return value;
    }
}
