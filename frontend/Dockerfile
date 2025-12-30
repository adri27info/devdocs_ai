FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json .

RUN npm ci && npm cache clean --force

COPY . .


FROM node:18-alpine

WORKDIR /app

COPY --from=build --chown=node:node /app /app

USER node

EXPOSE 8080

CMD ["npm", "run", "dev"]