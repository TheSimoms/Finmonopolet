# Dev server
FROM node AS dev

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

COPY gulpfile.js gulpfile.js
COPY src/ src/

CMD ["npm", "run", "dev"]


# Build the app
FROM dev as build

ARG API_HOST
ENV API_HOST=${API_HOST}

RUN ["npm", "run", "build"]


# Prod server
FROM nginx:alpine as prod

COPY nginx.conf /etc/nginx/nginx.conf

# Add the app
COPY --from=build /app/dist/ /usr/share/nginx/html/

CMD ["nginx", "-g", "daemon off;"]
