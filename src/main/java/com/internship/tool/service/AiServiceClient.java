package com.internship.tool.service;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.RestClientException;
import java.util.HashMap;
import java.util.Map;

@Service
public class AiServiceClient {
    private final RestTemplate restTemplate;

    public AiServiceClient(RestTemplate restTemplate) {
    this.restTemplate = restTemplate;
}

    private static final String BASE_URL = "http://localhost:5000";
    private static final int TIMEOUT = 10000; // 10 seconds

    private HttpEntity<Map<String, String>> buildRequest(String input) {
        Map<String, String> body = new HashMap<>();
        body.put("input", input);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        return new HttpEntity<>(body, headers);
    }

    public String callDescribe(String input) {
        try {
            ResponseEntity<String> response = restTemplate.exchange(
                    BASE_URL + "/describe",
                    HttpMethod.POST,
                    buildRequest(input),
                    String.class
            );

            return response.getBody();

        } catch (RestClientException e) {
            System.err.println("[AI] /describe failed: " + e.getMessage());
            return null;
        }
    }

    public String callRecommend(String input) {
        try {
            ResponseEntity<String> response = restTemplate.exchange(
                    BASE_URL + "/recommend",
                    HttpMethod.POST,
                    buildRequest(input),
                    String.class
            );

            return response.getBody();

        } catch (RestClientException e) {
            System.err.println("[AI] /recommend failed: " + e.getMessage());
            return null;
        }
    }

    public String callGenerateReport(String input) {
        try {
            ResponseEntity<String> response = restTemplate.exchange(
                    BASE_URL + "/generate-report",
                    HttpMethod.POST,
                    buildRequest(input),
                    String.class
            );

            return response.getBody();

        } catch (RestClientException e) {
            System.err.println("[AI] /generate-report failed: " + e.getMessage());
            return null;
        }
    }
}