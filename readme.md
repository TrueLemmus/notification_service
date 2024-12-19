### Запуск основного приложения 
```bash
uvicorn app.main:app --reload
```
### Запуск RabbitMQ
```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
### Панель управления RabbitMQ
В браузере по адресу http://localhost:15672/ зайдите в панель управления (логин/пароль: guest/guest).