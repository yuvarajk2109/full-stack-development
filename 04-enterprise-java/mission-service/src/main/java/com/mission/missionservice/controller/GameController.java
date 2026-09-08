package com.mission.missionservice.controller;

import com.mission.missionservice.service.GameService;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class GameController {

    private final GameService gameService;

    public GameController(GameService gameService) {
        this.gameService = gameService;
    }

    @GetMapping("impostor/word/{userId}")
    public Map<String, String> impostorWord(@AuthenticationPrincipal Jwt jwt, @PathVariable String userId) {
        return this.gameService.impostorWord(userId);
    }

    // Post to Guess the Impostor - Give Client ID
    @PostMapping("impostor/{userId}")
    public Map<String, String> guessImpostor(@AuthenticationPrincipal Jwt jwt, @PathVariable String userId) {
        return this.gameService.guessImpostor(userId);
    }
}
