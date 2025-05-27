# Этап сборки
FROM node:20-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

# Сборка с автоматическим экспортом
RUN npm run build

# Этап запуска на nginx
FROM nginx:alpine

# Копируем экспортированный сайт из build-контейнера
COPY --from=build /app/out /usr/share/nginx/html

# Копируем nginx конфиг (если есть)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
