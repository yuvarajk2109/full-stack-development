package com.mission.missionservice.service;

import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class HelloService {
    public Map<String, String> getGreeting() {
        return Map.of("message", "May the force be with you");
    }
}
