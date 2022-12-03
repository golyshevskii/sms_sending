## User Manual (docker-compose)

1. clone github repository:

````
git clone https://github.com/golyshevskii/sms_sending.git
````
2. Change .env file: ```TOKEN = 'your token'```
3. Run docker containers 
``` 
docker-compose up -d
```

***
```http://0.0.0.0:8000/api/``` - api

```http://0.0.0.0:8000/api/clients/``` - clients

```http://0.0.0.0:8000/api/sending_messages/``` - sending messages

```http://0.0.0.0:8000/api/sending_messages/fullinfo/``` - general statistics for all sending messages

```http://0.0.0.0:8000/api/sending_messages/<pk>/info/``` - detailed statistics for a specific sending message list

```http://0.0.0.0:8000/api/messages/``` - messages

```http://0.0.0.0:8000/docs/``` - docs

```http://0.0.0.0:5555``` - celery flower

***

4. Stop docker
```
docker-compose down
```