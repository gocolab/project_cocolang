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
