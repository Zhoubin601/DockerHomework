package cn.memorygarden;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.springframework.web.server.ResponseStatusException;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class GardenTests {
    @TempDir Path directory;

    @Test
    void scoresSurviveReopeningAndRepeatedSubmissionIsIdempotent() throws Exception {
        var first = new ScoreRepository(directory.toString());
        assertEquals(0, first.ranking("easy").total());
        assertNull(first.ranking("easy").bestDurationMs());
        var saved = first.save("game-a", "小花 ' DROP TABLE scores;", "easy", 8, 16000);
        assertEquals(saved.id(), first.save("game-a", "不能覆盖", "easy", 1, 1).id());
        first.save("game-b", "更少步数", "easy", 6, 30000);
        first.save("game-c", "更快完成", "easy", 6, 25000);
        first.save("game-d", "另一难度", "normal", 8, 20000);

        var reopened = new ScoreRepository(directory.toString());
        var ranking = reopened.ranking("easy");
        assertTrue(Files.size(directory.resolve("garden.db")) > 0);
        assertEquals(3, ranking.total());
        assertEquals(16000L, ranking.bestDurationMs());
        assertEquals(List.of("更快完成", "更少步数", "小花 ' DROP TABLE scores;"), ranking.scores().stream().map(ScoreRepository.Score::nickname).toList());
        assertEquals(1, reopened.ranking("normal").total());
    }

    @Test
    void cardsRemainSecretAndInvalidMovesCannotSaveScores() throws Exception {
        var engine = new GameService(new ScoreRepository(directory.toString()));
        for (String difficulty : List.of("easy", "normal", "hard")) {
            var game = engine.create(difficulty);
            assertEquals(GameService.pairsFor(difficulty) * 2, game.cards().size());
            assertTrue(game.cards().stream().allMatch(card -> card.symbol() == null));
        }
        var game = engine.create("easy");
        assertThrows(ResponseStatusException.class, () -> engine.create("unknown"));
        assertThrows(ResponseStatusException.class, () -> engine.flip(game.id(), -1));
        assertThrows(ResponseStatusException.class, () -> engine.flip(game.id(), 12));
        assertThrows(ResponseStatusException.class, () -> engine.save(game.id(), "小花"));
        var one = engine.flip(game.id(), 0);
        assertEquals(0, one.moves());
        assertTrue(one.timerRunning());
        assertNotNull(one.cards().getFirst().symbol());
        assertEquals(1, one.cards().stream().filter(card -> card.symbol() != null).count());
        assertThrows(ResponseStatusException.class, () -> engine.flip(game.id(), 0));
        var paused = engine.pause(game.id(), true);
        assertEquals("paused", paused.status());
        assertFalse(paused.timerRunning());
        assertTrue(paused.cards().stream().allMatch(card -> card.symbol() == null));
        assertThrows(ResponseStatusException.class, () -> engine.flip(game.id(), 1));
        var resumed = engine.pause(game.id(), false);
        assertEquals("playing", resumed.status());
        assertEquals(one.cards().getFirst().symbol(), resumed.cards().getFirst().symbol());
        assertThrows(ResponseStatusException.class, () -> engine.flip(game.id(), 0));
        engine.abandon(game.id());
        assertThrows(ResponseStatusException.class, () -> engine.view(game.id()));
    }

    @Test
    void completedGameUsesServerMetricsAndCanBeSavedExactlyOnce() throws Exception {
        var repository = new ScoreRepository(directory.toString());
        var engine = new GameService(repository);
        var game = engine.create("easy");
        Map<String, List<Integer>> known = new HashMap<>();
        for (int index = 0; index < game.cards().size(); index += 2) {
            var first = engine.flip(game.id(), index);
            known.computeIfAbsent(first.cards().get(index).symbol(), ignored -> new ArrayList<>()).add(index);
            game = engine.flip(game.id(), index + 1);
            known.computeIfAbsent(game.cards().get(index + 1).symbol(), ignored -> new ArrayList<>()).add(index + 1);
            if (game.lockedForMs() > 0) {
                int extra = (index + 2) % game.cards().size();
                var id = game.id();
                assertThrows(ResponseStatusException.class, () -> engine.flip(id, extra));
                Thread.sleep(game.lockedForMs() + 30);
            }
        }
        game = engine.view(game.id());
        for (List<Integer> pair : known.values()) {
            if (game.cards().get(pair.getFirst()).matched()) continue;
            engine.flip(game.id(), pair.getFirst());
            game = engine.flip(game.id(), pair.getLast());
        }
        assertEquals("completed", game.status());
        assertEquals(6, game.matchedPairs());
        assertFalse(game.timerRunning());
        assertTrue(game.moves() >= 6);
        var id = game.id();
        assertThrows(ResponseStatusException.class, () -> engine.save(id, "   "));
        assertThrows(ResponseStatusException.class, () -> engine.save(id, "x".repeat(17)));
        var saved = engine.save(game.id(), "小花6085");
        assertEquals(game.moves(), saved.moves());
        assertEquals(game.elapsedMs(), saved.durationMs());
        assertEquals(saved.id(), engine.save(game.id(), "重复提交").id());
        assertEquals(1, repository.ranking("easy").total());
        assertEquals("小花6085", repository.ranking("easy").scores().getFirst().nickname());
    }
}
