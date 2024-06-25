function initializeForm(deltaObject) {
    // Quill 에디터 설정
    let quillSettings = {
        theme: 'snow'
    };
    let quillDescription = new Quill('#description_delta', quillSettings);

    // Delta 값을 편집기에 적용
    if (!isEmptyObject(deltaObject)){
        deltaObject = JSON.parse(deltaObject);
        quillDescription.setContents(deltaObject);
    }

    // Submit handler
    let form = document.querySelector('form');
    form.onsubmit = function (event) {
        let description_delta = document.querySelector('#description');
        description_delta.value = JSON.stringify(quillDescription.getContents());
        return true; // return false to cancel form action
    };
}