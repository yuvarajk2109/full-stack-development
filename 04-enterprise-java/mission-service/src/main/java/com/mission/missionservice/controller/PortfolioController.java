package com.mission.missionservice.controller;

import com.mission.missionservice.service.PortfolioService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class PortfolioController {

    private final PortfolioService portfolioService;

    public PortfolioController(PortfolioService portfolioService) {
        this.portfolioService = portfolioService;
    }

    @GetMapping("/portfolio/{clientId}")
    public Map<String, String> getPortfolio(@PathVariable String clientId) {
        return portfolioService.getPortfolio(clientId);
    }
}
