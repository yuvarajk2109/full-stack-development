package com.mission.missionservice.repository;

import org.springframework.stereotype.Repository;

@Repository
public interface GameRepository {
    String getWord(String userId);
    String getImpostor();
}
