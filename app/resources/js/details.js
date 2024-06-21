document.addEventListener('DOMContentLoaded', function () {
    let downloadLink = document.querySelector('#download_all');
    downloadLink.addEventListener('click', function (e) {
        e.preventDefault(); // 기본 링크 동작 방지
        window.location.href = downloadLink.getAttribute('href'); // 파일 다운로드 시작
    });

    let quillDescription = new Quill('#description_delta', {
        theme: 'snow',
        readOnly: true, // 읽기 전용 모드 활성화
        modules: {
            toolbar: false // 툴바 제거
        }
    });

    let deltaObject = {{ comodule.description | tojson | safe }}; // 서버 사이드 템플릿으로부터 JSON 문자열을 받아옴
    deltaObject = JSON.parse(deltaObject);
    quillDescription.setContents(deltaObject);
});
