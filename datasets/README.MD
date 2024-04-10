### setup commands
```
~docker_db$ mongodump --uri "mongodb://127.0.0.1:27017/project_cocolabhub" --archive=./initial_data.archive
~$ docker cp project_cocolabhub_mongodb:/home/initial_data.archive ./
~$ docker cp ./initial_data.archive project_cocolabhub_jupyter_fastapi:/app/project_cocolabhub/datasets
~$ mongorestore --uri "mongodb://project_cocolabhub_mongodb:27017/project_cocolabhub" --archive=/app/project_cocolabhub/datasets/initial_data.archive
```