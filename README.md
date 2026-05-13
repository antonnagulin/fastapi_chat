# Async Chat (Fastapi + MongoDB + Kafka + Telegram notification)


## Установка и запуск

1. Скопируйте `.env.example` в `.env` и измените настройки:

```bash
cp .env.example .env
```

2. Собрать и поднять контейнеры:

```bash
make all
```

- fastapi будет доступен на `http://localhost:8000`
- Документация (Swagger) на `http://localhost:8000/api/docs`
- UI Kafka на `http://127.0.0.1:8090/`
- UI mongo на `http://localhost:28081`


## Makefile команды

```bash
# Просмотр логов fast api
make app-logs  

# просмотр логов kafka
make messaging-logs

```
---
