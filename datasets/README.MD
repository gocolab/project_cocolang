### commons_code
- datasets\common_comodules.json : 컴퓨터 관련 분야 Langauge,	Framework, Database 분류에 대한 항목 4가지 이상 작성과 표시 순서, 설명 json로 작성. 설명은 간략한 요약 방식

```
~$ mongodump --uri "mongodb://127.0.0.1:27017/project_cocolabhub" --archive=./backup_data.archive
~$ zip backup_data.zip backup_data.archive
~~$ docker cp project_cocolabhub-fastapi-1:backup_data.zip ./datasets
~$ docker cp ./datasets/backup_data.zip project_cocolabhub-fastapi-1:/
~$ docker exec project_cocolabhub-mongodb-1 mongorestore --uri "mongodb://mongodb:27017/project_cocolabhub" --archive=./backup_data.archive
```