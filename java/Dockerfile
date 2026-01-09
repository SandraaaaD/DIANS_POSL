#FROM ubuntu:latest
#LABEL authors="Sandra"
#
#ENTRYPOINT ["top", "-b"]


#FROM ubuntu:latest
#LABEL authors="Sandra"
#
#ENTRYPOINT ["top", "-b"]


## 1. Основа: користиме OpenJDK 21
#FROM openjdk:21-slim
#
## 2. Работна папка во контејнерот
#WORKDIR /app
#
## 3. Копирај го pom.xml за да се инсталираат dependencies прво (Maven will cache them)
#COPY demo/pom.xml ./pom.xml
#
## 4. Инсталирај Maven (не е секогаш вклучен во slim image)
#RUN apt-get update && apt-get install -y maven && rm -rf /var/lib/apt/lists/*
#
## 5. Копирај го цел src директориумот
#COPY demo/src ./src
#
## 6. Билдај ја Java апликацијата (create executable jar)
#RUN mvn clean package -DskipTests
#
## 7. Копирај го резултатниот jar
## Во твојот случај jar ќе се наоѓа во target/demo-0.0.1-SNAPSHOT.jar
## Ако името е различно, промени го
#COPY target/demo-0.0.1-SNAPSHOT.jar app.jar
#
## 8. Команда за стартување на Spring Boot апликацијата
#ENTRYPOINT ["java","-jar","app.jar"]

# ===== BUILD STAGE =====
FROM maven:3.9-eclipse-temurin-21 AS build

WORKDIR /app

COPY demo/pom.xml .
COPY demo/src ./src

RUN mvn clean package -DskipTests

# ===== RUNTIME STAGE =====
FROM eclipse-temurin:21

WORKDIR /app

COPY --from=build /app/target/*.jar app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]
