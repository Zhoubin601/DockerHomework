package cn.memorygarden;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.security.SecureRandom;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class GameService {
    private static final List<String> SYMBOLS = List.of("sprout", "tulip", "daisy", "cactus", "leaf", "cherry", "mushroom", "orange", "clover", "sunflower", "acorn", "lavender");
    private static final Map<String, Integer> PAIRS = Map.of("easy", 6, "normal", 8, "hard", 12);
    private final Map<UUID, Game> games = new ConcurrentHashMap<>();
    private final ScoreRepository scores;
    private final SecureRandom random = new SecureRandom();

    public GameService(ScoreRepository scores) { this.scores = scores; }

    public static int pairsFor(String difficulty) {
        Integer pairs = PAIRS.get(difficulty);
        if (pairs == null) throw bad("请选择有效的难度。");
        return pairs;
    }

    public GameView create(String difficulty) {
        int pairs = pairsFor(difficulty);
        games.entrySet().removeIf(entry -> entry.getValue().created.isBefore(Instant.now().minusSeconds(7200)));
        if (games.size() >= 5000) throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE, "花园有点忙，请稍后再试。");
        List<String> deck = new ArrayList<>(SYMBOLS.subList(0, pairs));
        deck.addAll(new ArrayList<>(deck));
        Collections.shuffle(deck, random);
        Game game = new Game(difficulty, deck);
        games.put(game.id, game);
        return game.view();
    }

    public GameView view(UUID id) {
        Game game = find(id);
        synchronized (game) { return game.view(); }
    }

    public GameView flip(UUID id, int index) {
        Game game = find(id);
        synchronized (game) {
            game.clearMismatch();
            if (!game.status.equals("playing")) throw bad("请先继续游戏，或开始新的一局。");
            if (index < 0 || index >= game.deck.size()) throw bad("这张卡牌不存在。");
            if (game.lockedUntil > System.nanoTime()) throw new ResponseStatusException(HttpStatus.CONFLICT, "请等这两张牌翻回后再试。");
            if (game.matched.contains(index) || game.open.contains(index)) throw bad("请选择另一张未配对的卡牌。");
            if (game.startedAt == 0) {
                game.startedAt = System.nanoTime();
                game.hasStarted = true;
            }
            game.open.add(index);
            if (game.open.size() == 2) {
                game.moves++;
                if (game.deck.get(game.open.getFirst()).equals(game.deck.get(game.open.getLast()))) {
                    game.matched.addAll(game.open);
                    game.open.clear();
                    if (game.matched.size() == game.deck.size()) {
                        game.elapsedBefore = game.elapsed();
                        game.startedAt = 0;
                        game.status = "completed";
                    }
                } else {
                    game.lockedUntil = System.nanoTime() + 850_000_000L;
                }
            }
            return game.view();
        }
    }

    public GameView pause(UUID id, boolean pause) {
        Game game = find(id);
        synchronized (game) {
            game.clearMismatch();
            if (game.status.equals("completed")) throw bad("这一局已完成。");
            if (pause && game.status.equals("playing")) {
                game.elapsedBefore = game.elapsed();
                game.startedAt = 0;
                game.status = "paused";
                game.mismatchRemaining = Math.max(0, game.lockedUntil - System.nanoTime());
                game.lockedUntil = 0;
            } else if (!pause && game.status.equals("paused")) {
                game.startedAt = game.hasStarted ? System.nanoTime() : 0;
                game.status = "playing";
                if (game.open.size() == 2) {
                    game.lockedUntil = System.nanoTime() + Math.max(1_000_000, game.mismatchRemaining);
                }
            }
            return game.view();
        }
    }

    public ScoreRepository.Score save(UUID id, String nickname) {
        String clean = nickname == null ? "" : nickname.strip();
        if (clean.isEmpty() || clean.codePointCount(0, clean.length()) > 16 || clean.codePoints().anyMatch(Character::isISOControl)) {
            throw bad("昵称需为 1–16 个字符，且不含控制字符。");
        }
        Game game = find(id);
        synchronized (game) {
            if (!game.status.equals("completed")) throw bad("完成这一局后才能保存成绩。");
            return scores.save(game.id.toString(), clean, game.difficulty, game.moves, game.elapsedBefore);
        }
    }

    public void abandon(UUID id) { games.remove(id); }

    private Game find(UUID id) {
        Game game = games.get(id);
        if (game == null || game.created.isBefore(Instant.now().minusSeconds(7200))) {
            games.remove(id);
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "这一局已过期或服务已重启，请开始新的一局。");
        }
        return game;
    }

    private static ResponseStatusException bad(String message) { return new ResponseStatusException(HttpStatus.BAD_REQUEST, message); }

    private static class Game {
        final UUID id = UUID.randomUUID();
        final Instant created = Instant.now();
        final String difficulty;
        final List<String> deck;
        final Set<Integer> matched = new HashSet<>();
        final List<Integer> open = new ArrayList<>();
        String status = "playing";
        int moves;
        boolean hasStarted;
        long startedAt;
        long elapsedBefore;
        long lockedUntil;
        long mismatchRemaining;

        Game(String difficulty, List<String> deck) { this.difficulty = difficulty; this.deck = deck; }

        long elapsed() { return elapsedBefore + (startedAt == 0 ? 0 : (System.nanoTime() - startedAt) / 1_000_000); }

        void clearMismatch() {
            if (lockedUntil != 0 && System.nanoTime() >= lockedUntil) {
                open.clear();
                lockedUntil = 0;
            }
        }

        GameView view() {
            clearMismatch();
            List<Card> cards = new ArrayList<>();
            for (int index = 0; index < deck.size(); index++) {
                boolean visible = status.equals("playing") && (matched.contains(index) || open.contains(index));
                if (status.equals("completed")) visible = true;
                cards.add(new Card(index, visible ? deck.get(index) : null, matched.contains(index)));
            }
            return new GameView(id, difficulty, status, moves, elapsed(), startedAt != 0, matched.size() / 2, deck.size() / 2,
                    Math.max(0, (lockedUntil - System.nanoTime()) / 1_000_000), cards);
        }
    }

    public record Card(int index, String symbol, boolean matched) {}
    public record GameView(UUID id, String difficulty, String status, int moves, long elapsedMs, boolean timerRunning,
                           int matchedPairs, int totalPairs, long lockedForMs, List<Card> cards) {}
}
