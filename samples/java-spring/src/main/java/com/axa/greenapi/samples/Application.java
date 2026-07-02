package com.axa.greenapi.samples;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.util.*;

/**
 * Sample API for the Green Score workshop.
 *
 * BASELINE (intentional): no pagination, no ETag, no compression, /events
 * endpoint returns a JSON array instead of SSE. Participants will iterate
 * during Act 2 & 3 to improve the score.
 */
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

@RestController
@RequestMapping("/items")
class ItemsController {

    private static final List<Map<String, Object>> ITEMS;
    static {
        List<Map<String, Object>> l = new ArrayList<>();
        for (int i = 1; i <= 200; i++) {
            Map<String, Object> m = new LinkedHashMap<>();
            m.put("id", i);
            m.put("title", "Item #" + i);
            m.put("description", "Long description body ".repeat(20));
            m.put("updatedAt", Instant.now().toString());
            l.add(m);
        }
        ITEMS = Collections.unmodifiableList(l);
    }

    // ❌ DE11: no pagination — returns everything.
    @GetMapping
    public List<Map<String, Object>> list() {
        return ITEMS;
    }

    // ❌ DE02/03: no ETag support.
    @GetMapping("/{id}")
    public Map<String, Object> get(@PathVariable int id) {
        return ITEMS.stream()
                .filter(m -> Integer.valueOf(id).equals(m.get("id")))
                .findFirst()
                .orElseThrow(() -> new RuntimeException("not found"));
    }

    // ❌ AR01: polling-style endpoint. Should become SSE.
    @GetMapping("/events")
    public List<Map<String, Object>> events() {
        return ITEMS.subList(0, 5);
    }

    // ✅ DE06 baseline: delta sync via ?since=<epoch>
    @GetMapping("/changes")
    public List<Map<String, Object>> changes(@RequestParam(required = false) Long since) {
        return ITEMS.subList(0, 3);
    }

    @PostMapping
    public Map<String, Object> create(@RequestBody Map<String, Object> body) {
        body.put("id", ITEMS.size() + 1);
        return body;
    }
}

