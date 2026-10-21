FROM node:24-bookworm-slim AS frontend
WORKDIR /build/frontend
COPY frontend/package*.json ./
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM maven:3.9.9-eclipse-temurin-21 AS backend
WORKDIR /build/backend
COPY backend/pom.xml ./
RUN mvn -B -ntp dependency:go-offline
COPY backend/src ./src
COPY --from=frontend /build/frontend/dist /build/frontend/dist
RUN mvn -B -ntp package

FROM eclipse-temurin:21-jre-jammy
RUN groupadd --system garden && useradd --system --gid garden --home-dir /app garden \
    && mkdir -p /app/data && chown -R garden:garden /app
WORKDIR /app
COPY --from=backend --chown=garden:garden /build/backend/target/memory-game6085.jar /app/app.jar
USER garden
ENV DATA_DIR=/app/data PORT=8080
EXPOSE 8080
ENTRYPOINT ["java", "-XX:MaxRAMPercentage=70.0", "-jar", "/app/app.jar"]
