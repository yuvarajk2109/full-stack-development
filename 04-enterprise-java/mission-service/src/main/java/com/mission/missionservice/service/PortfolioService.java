package com.mission.missionservice.service;

import com.mission.missionservice.repository.PortfolioRepository;
import org.springframework.stereotype.Service;

import java.time.Clock;
import java.time.Instant;
import java.util.Map;

@Service
public class PortfolioService {

    private final PortfolioRepository portfolioRepository;
    private final Clock clock;

    public PortfolioService(PortfolioRepository portfolioRepository, Clock clock) {
        this.portfolioRepository = portfolioRepository;
        this.clock = clock;
    }

    public Map<String, String> getPortfolio(String clientId) {
       Double value = portfolioRepository.findTotalPortfolioValue(clientId);
       Instant asOf = clock.instant();
       return Map.of(
           "Client ID", clientId,
           "Value", value.toString(),
           "As of", asOf.toString()
       );
    }
}
