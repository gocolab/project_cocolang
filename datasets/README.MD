### commons_code
- datasets\common_comodules.json : 컴퓨터 관련 분야 Langauge,	Framework, Database 분류에 대한 항목 4가지 이상 작성과 표시 순서, 설명 json로 작성. 설명은 간략한 요약 방식

```
~$ docker exec project_cocolabhub-mongodb-1 mongodump --uri "mongodb://127.0.0.1:27017/project_cocolabhub" --out=/data/dump/
~$ docker cp project_cocolabhub-fastapi-1:/data/dump/ .
~$ docker cp ./dump project_cocolabhub-mongodb-1:/
~$ docker exec project_cocolabhub-mongodb-1 mongorestore --uri "mongodb://mongodb:27017/project_cocolabhub" /dump/project_cocolabhub


```