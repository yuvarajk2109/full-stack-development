package com.mission.missionservice.repository;

import org.springframework.stereotype.Repository;

@Repository
public interface PortfolioRepository {
    Double findTotalPortfolioValue(String clientId);
}
