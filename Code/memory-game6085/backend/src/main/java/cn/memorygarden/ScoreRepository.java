package cn.memorygarden;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Repository;

import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.*;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@Repository
public class ScoreRepository {
    private final String url;

    public ScoreRepository(@Value("${garden.data-dir}") String directory) throws Exception {
        Path root = Path.of(directory).toAbsolutePath().normalize();
        Files.createDirectories(root);
        url = "jdbc:sqlite:" + root.resolve("garden.db");
        try (Connection connection = connect(); Statement sql = connection.createStatement()) {
            sql.execute("PRAGMA journal_mode=WAL");
            sql.execute("""
                CREATE TABLE IF NOT EXISTS scores (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  game_id TEXT NOT NULL UNIQUE,
                  nickname TEXT NOT NULL,
                  difficulty TEXT NOT NULL,
                  moves INTEGER NOT NULL CHECK(moves > 0),
                  duration_ms INTEGER NOT NULL CHECK(duration_ms >= 0),
                  created_at TEXT NOT NULL
                )
                """);
            sql.execute("CREATE INDEX IF NOT EXISTS scores_ranking ON scores(difficulty, moves, duration_ms, id)");
        }
    }

    private Connection connect() throws SQLException {
        Connection connection = DriverManager.getConnection(url);
        try (Statement statement = connection.createStatement()) {
            statement.execute("PRAGMA busy_timeout=5000");
        } catch (SQLException error) {
            connection.close();
            throw error;
        }
        return connection;
    }

    public Score save(String gameId, String nickname, String difficulty, int moves, long durationMs) {
        try (Connection connection = connect(); PreparedStatement insert = connection.prepareStatement("""
            INSERT INTO scores(game_id,nickname,difficulty,moves,duration_ms,created_at)
            VALUES(?,?,?,?,?,?) ON CONFLICT(game_id) DO NOTHING
            """)) {
            insert.setString(1, gameId);
            insert.setString(2, nickname);
            insert.setString(3, difficulty);
            insert.setInt(4, moves);
            insert.setLong(5, durationMs);
            insert.setString(6, Instant.now().toString());
            insert.executeUpdate();
            try (PreparedStatement query = connection.prepareStatement("SELECT * FROM scores WHERE game_id=?")) {
                query.setString(1, gameId);
                try (ResultSet row = query.executeQuery()) {
                    if (!row.next()) throw new SQLException("Score was not saved");
                    return read(row);
                }
            }
        } catch (SQLException error) {
            throw new IllegalStateException("成绩暂时未能保存，请稍后重试。", error);
        }
    }

    public Ranking ranking(String difficulty) {
        try (Connection connection = connect()) {
            List<Score> scores = new ArrayList<>();
            try (PreparedStatement query = connection.prepareStatement("""
                SELECT * FROM scores WHERE difficulty=? ORDER BY moves ASC,duration_ms ASC,id ASC LIMIT 10
                """)) {
                query.setString(1, difficulty);
                try (ResultSet rows = query.executeQuery()) {
                    while (rows.next()) scores.add(read(rows));
                }
            }
            try (PreparedStatement query = connection.prepareStatement("""
                SELECT COUNT(*) AS total,MIN(duration_ms) AS best FROM scores WHERE difficulty=?
                """)) {
                query.setString(1, difficulty);
                try (ResultSet row = query.executeQuery()) {
                    row.next();
                    long best = row.getLong("best");
                    boolean noBest = row.wasNull();
                    return new Ranking(scores, row.getLong("total"), noBest ? null : best);
                }
            }
        } catch (SQLException error) {
            throw new IllegalStateException("排行榜暂时不可用，请稍后重试。", error);
        }
    }

    private Score read(ResultSet row) throws SQLException {
        return new Score(row.getLong("id"), row.getString("nickname"), row.getString("difficulty"),
                row.getInt("moves"), row.getLong("duration_ms"), row.getString("created_at"));
    }

    public record Score(long id, String nickname, String difficulty, int moves, long durationMs, String createdAt) {}
    public record Ranking(List<Score> scores, long total, Long bestDurationMs) {}
}
