# Stage 1: build. This image has Maven and a full JDK - everything needed
# to compile and package the jar, none of which the running service needs.
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /build

# Copy the pom first and download dependencies as their own layer - Docker
# caches this layer and skips re-downloading the entire dependency tree
# every time only the source code changes (Sprint 1's caching idea, applied
# to a Dockerfile instead of a CI pipeline).
COPY pom.xml .
RUN mvn -B dependency:go-offline

COPY src ./src
RUN mvn -B clean package -DskipTests

# Stage 2: run. A JRE (no compiler, no Maven, no build tools) - smaller
# image, smaller attack surface. Only the built jar crosses the boundary
# between stages; the Maven layer above never ships.
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

## Copy the built jar (use wildcard so the exact artifact name doesn't matter)
COPY --from=build /build/target/*.jar app.jar

# Default environment variables (can be overridden at `docker run`)
# Maps to Spring property `jwt.shared-secret` via relaxed binding (JWT_SHARED_SECRET).
ENV JWT_SHARED_SECRET=mission-control-shared-secret-key-32-bytes-minimum
ENV JAVA_OPTS=""

EXPOSE 8080
# Allow passing JVM options via JAVA_OPTS when running the container
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
