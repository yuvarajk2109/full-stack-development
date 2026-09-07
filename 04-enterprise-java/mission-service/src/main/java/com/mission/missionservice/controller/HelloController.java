package com.mission.missionservice.controller;

import com.mission.missionservice.service.HelloService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class HelloController {

    private HelloService helloService;

    public HelloController() {
        this.helloService = new HelloService();
    }

    @GetMapping("/hello")
    public Map<String, String> hello() {
        return helloService.getGreeting();
    }

}
