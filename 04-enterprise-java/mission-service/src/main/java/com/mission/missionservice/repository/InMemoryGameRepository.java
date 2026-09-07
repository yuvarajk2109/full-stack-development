package com.mission.missionservice.repository;

import org.springframework.stereotype.Repository;

import java.util.Map;
import java.util.stream.Collectors;

@Repository
public class InMemoryGameRepository implements GameRepository {

    Map<String, String> values = Map.of(
            "1", "Apple",
            "2", "Apple",
            "3", "Apple",
            "4", "Apple",
            "5", "Banana"
    );

    @Override
    public String getWord(String userId) {
        return values.get(userId);
    }

    @Override
    public String getImpostor() {
        try {
            Map<String, Long> valueCounts = values.values().stream()
                    .collect(Collectors.groupingBy(v -> v, Collectors.counting()));

            return values.entrySet().stream()
                    .filter(entry -> valueCounts.get(entry.getValue()) == 1)
                    .map(Map.Entry::getKey)
                    .findFirst()
                    .orElse(null);

        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
