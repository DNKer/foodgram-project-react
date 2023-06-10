# build env
FROM node:18.16.0-alpine as build
RUN addgroup app && adduser -S -G app app
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
USER app
RUN npm run build
CMD cp -r build result_build
