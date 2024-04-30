db.comodules.find().forEach(function(doc) {
    // '/dockers'가 포함되지 않은 문서를 찾는다.
    if (!doc.docker_files_links.includes('/dockers')) {
        let originalString = doc.docker_files_links;
        // "/.env", "/Dockerfile", "/docker-compose.yml" 앞에 "/dockers" 추가
        let modifiedString = originalString
        .replace('/.env', '/dockers/.env')
        .replace('/Dockerfile', '/dockers/Dockerfile')
        .replace('/docker-compose.yml', '/dockers/docker-compose.yml');
      // 문서를 업데이트한다.
      db.comodules.updateOne({_id: doc._id}, {$set: {docker_files_links: modifiedString}});
    }
  });

  db.comodules.updateMany(
    {}, // 모든 문서 선택
    [{
      $set: {
        language_name: {
          // language_name 과 language_version 을 연결
          $concat: ["$language_name", " (", "$language_version", ")"]
        },
        framework_name: {
          // framework_name 과 framework_version 을 연결
          $concat: ["$framework_name", " (", "$framework_version", ")"]
        },
        database_name: {
          // database_name 과 database_version 을 연결
          $concat: ["$database_name", " (", "$database_version", ")"]
        }
      }
    }]
  );

  db.comodules.updateMany(
    {}, // 모든 문서를 선택합니다.
    [{
      $set: {
        language_name: {
          $cond: {
            if: { $in: ["$language_name", [null, " ()"]] },
            then: "",
            else: "$language_name"
          }
        },
        framework_name: {
          $cond: {
            if: { $in: ["$framework_name", [null, " ()"]] },
            then: "",
            else: "$framework_name"
          }
        },
        database_name: {
          $cond: {
            if: { $in: ["$database_name", [null, " ()"]] },
            then: "",
            else: "$database_name"
          }
        }
      }
    }]
  ); 
  
  db.comodules.updateMany(
    {}, // 모든 문서를 선택
    [
      { $set: { tempField: "$create_user_id" } }, // 임시 필드를 사용하여 create_user_id 값을 저장
      { $set: { create_user_id: "$create_user_name", create_user_name: "$tempField" } }, // create_user_id와 create_user_name의 값을 서로 바꾸고, 임시 필드의 값을 create_user_name에 저장
      { $unset: "tempField" } // 임시 필드 제거
    ]
  );

  db.users.updateMany(
    {},
    { $addToSet: { roles: "PARTER" } },
  );
  
  
