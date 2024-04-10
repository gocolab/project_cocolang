### install dockers
```
~% docker-compose --project-name project_cocolang build --no-cache
~% docker-compose --project-name project_cocolang up -d
```

### setup initial mongodb datasets commands
```
~docker_db$ mongodump --uri "mongodb://cocolabhub_mongodb:27017/project_cocolabhub" --archive=./initial_data.archive
~$ docker cp cocolabhub_mongodb:/home/initial_data.archive ./
~$ docker cp ./initial_data.archive project_cocolang-fastapi:/apps/project_cocolabhub/datasets
~$ mongorestore --uri "mongodb://cocolabhub_mongodb:27017/project_cocolabhub" --archive=/apps/project_cocolabhub/datasets/initial_data.archive
```

### real server
```
~$ cd /apps/project_cocolabhub
~$ uvicorn app.main:app --host 0.0.0.0 --port 8080
```