package com.mission.missionservice.service;

import com.mission.missionservice.repository.GameRepository;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class GameService {

    private final GameRepository gameRepository;

    public GameService(GameRepository gameRepository) {
        this.gameRepository = gameRepository;
    }

    public Map<String, String> impostorWord(String userId) {
        return Map.of(userId, gameRepository.getWord(userId));
    }

    public Map<String, String> guessImpostor(String userId) {
        String impostor = gameRepository.getImpostor();
        if (impostor.equals(userId)) return Map.of("message", "Congratulations! You have found the impostor!");
        else return Map.of("message", "BOOO! The impostor is " + impostor + ", ya fool!");
    }
}
