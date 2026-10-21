package cn.memorygarden;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api")
public class GardenController {
    private final GameService games;
    private final ScoreRepository scores;

    public GardenController(GameService games, ScoreRepository scores) { this.games = games; this.scores = scores; }

    @GetMapping("/health")
    public Map<String, String> health() {
        scores.ranking("easy");
        return Map.of("status", "UP", "application", "memory-game6085", "database", "SQLite");
    }

    @PostMapping("/games")
    @ResponseStatus(HttpStatus.CREATED)
    public GameService.GameView create(@Valid @RequestBody CreateRequest request) { return games.create(request.difficulty()); }

    @GetMapping("/games/{id}")
    public GameService.GameView view(@PathVariable UUID id) { return games.view(id); }

    @PostMapping("/games/{id}/flip")
    public GameService.GameView flip(@PathVariable UUID id, @RequestBody FlipRequest request) { return games.flip(id, request.index()); }

    @PostMapping("/games/{id}/pause")
    public GameService.GameView pause(@PathVariable UUID id, @RequestBody PauseRequest request) { return games.pause(id, request.paused()); }

    @DeleteMapping("/games/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void abandon(@PathVariable UUID id) { games.abandon(id); }

    @PostMapping("/games/{id}/score")
    public ScoreRepository.Score save(@PathVariable UUID id, @Valid @RequestBody ScoreRequest request) { return games.save(id, request.nickname()); }

    @GetMapping("/leaderboard")
    public ScoreRepository.Ranking ranking(@RequestParam(defaultValue = "normal") String difficulty) {
        GameService.pairsFor(difficulty);
        return scores.ranking(difficulty);
    }

    public record CreateRequest(@NotBlank String difficulty) {}
    public record FlipRequest(int index) {}
    public record PauseRequest(boolean paused) {}
    public record ScoreRequest(@NotBlank @Size(max = 32) String nickname) {}
}
