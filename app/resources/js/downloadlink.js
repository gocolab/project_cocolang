let downloadLink = document.querySelector('#download_all');
downloadLink.addEventListener('click', function (e) {
    e.preventDefault(); // 기본 링크 동작 방지
    window.location.href = downloadLink.getAttribute('href'); // 파일 다운로드 시작
});
