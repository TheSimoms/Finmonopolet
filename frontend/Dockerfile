FROM node:14-alpine AS dev

WORKDIR /app

COPY rollup.config.js ./
COPY tsconfig.json ./
COPY package*.json ./

RUN npm install

COPY ./src ./src
COPY ./public ./public

ARG API_HOST
ENV API_HOST=$API_HOST

EXPOSE 5000
ENV HOST=0.0.0.0

CMD [ "npm", "run", "dev" ]

FROM dev AS prod

RUN npm run build

CMD [ "npm", "start" ]
