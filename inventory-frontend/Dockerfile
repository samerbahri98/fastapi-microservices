FROM node:20-bullseye-slim as frontend-build

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

RUN npm build

FROM nginx:1.24-bullseye as frontend

COPY --from=frontend-build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]