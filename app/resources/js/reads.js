function initializeRead(deltaObject) {
    // Quill 에디터 설정
    let quillSettings = {
        theme: 'snow'
    };
    let quillDescription = new Quill('#description_delta', quillSettings);

    // Delta 값을 편집기에 적용
    // if (!isEmptyObject(deltaObject)){
        deltaObject = JSON.parse(deltaObject);
        quillDescription.setContents(deltaObject);
    // }
}