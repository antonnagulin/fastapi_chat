# Chat (Fastapi)

## Установка и запуск

1. Скопируйте `.env.example` в `.env` и измените настройки:

```bash
cp .env.example .env
```

2. Собрать и поднять контейнеры:

```bash
make app
```

- fastapi будет доступен на `http://localhost:8000`
- Документация (Swagger) на `http://localhost:8000/api/docs`



## Makefile команды

```bash
# Просмотр логов
make app-logs 

# Запуск тестов
make test

# Остановить контейнеры:
make app-down 
```
---
