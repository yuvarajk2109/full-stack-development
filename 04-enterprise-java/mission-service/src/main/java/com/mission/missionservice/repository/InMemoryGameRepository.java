package com.mission.missionservice.repository;

import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Map;

@Repository
public class InMemoryGameRepository implements GameRepository {

    Map<String, String> values = Map.of(
            "1", "Apple",
            "2", "Orange",
            "3", "Apple",
            "4", "Apple",
            "5", "Apple"
    );

    @Override
    public String getWord(String userId) {
        return values.get(userId);
    }

    @Override
    public String getImpostor() {
        return "2";
    }
}
