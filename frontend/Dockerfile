# Dockerfile
FROM node:18.20-alpine3.19 AS build
WORKDIR /test
RUN apk update && apk upgrade
COPY . /test
RUN npm install
