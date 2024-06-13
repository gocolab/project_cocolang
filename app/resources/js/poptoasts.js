
document.querySelectorAll('.setupButton').forEach(button => {
    button.addEventListener('click', function (event) {
        event.preventDefault();
        popToastSetup(this);
    });
});

document.querySelectorAll('.shellButton').forEach(button => {
    button.addEventListener('click', function (event) {
        event.preventDefault();
        popToastShell(this);
    });
});

function popToastSetup(button) {
    const value = button.value.replace(/\s*\([^)]*\)/g, '').split('_').map(str => str.split('\n')[0].replace(/\s/g, '')).join('_');
    const command = `docker-compose --project-name ${value.toLowerCase()} up -d --build`;

    navigator.clipboard.writeText(command).then(() => {
        const toastEl = document.querySelector('.toast');
        toastEl.innerHTML = `<div class="toast-body">~$ ${command}</div>`;
        new bootstrap.Toast(toastEl).show();
        button.innerHTML = 'copied <i class="bi bi-clipboard-check"></i>';
    });

    document.querySelector('.toast').addEventListener('hidden.bs.toast', () => {
        button.innerHTML = 'setup <i class="bi bi-clipboard"></i>';
    });
}

function popToastShell(button) {
    const command = `wget -O docker_files.zip ${window.location.origin}${button.value}`;
    navigator.clipboard.writeText(command).then(() => {
        const toastEl = document.querySelector('.toast');
        toastEl.innerHTML = `<div class="toast-body">~$ ${command}\n~$ unzip docker_files.zip -d docker_folder</div>`;
        new bootstrap.Toast(toastEl).show();
        button.innerHTML = 'copied <i class="bi bi-braces-asterisk"></i>';
    });

    document.querySelector('.toast').addEventListener('hidden.bs.toast', () => {
        button.innerHTML = 'shell <i class="bi bi-braces"></i>';
    });
}

function popToastSetup(thisButton) {
    const buttonValue = removeAndConcat(thisButton.value.toLowerCase()); // 혹은 this.getAttribute('data-value') 등을 사용

    let toastEl = document.querySelector('.toast');

    let command = `docker-compose --project-name ${buttonValue} up -d --build`;

    // 클립보드에 명령어 복사
    navigator.clipboard.writeText(command).then(function () {
      const toastHtml = `
            <div class="toast-body">
              ~$ docker-compose build --no-cache </p>
              ~$ docker-compose --project-name ${buttonValue} up -d
            </div>
        `;

      // 알림 창 표시
      toastEl.innerHTML = toastHtml;
      let toast = new bootstrap.Toast(toastEl);

      toast.show();
      // 아이콘 변경
      thisButton.innerHTML = 'copied <i class="bi bi-clipboard-check"></i>';
    }, function (err) {
      console.error('Async: Could not copy text: ', err);
    });

    // 알림 창이 사라진 후 아이콘 원래대로 변경
    toastEl.addEventListener('hidden.bs.toast', function () {
      thisButton.innerHTML = 'setup <i class="bi bi-clipboard"></i>';
    });
  }

  function removeAndConcat(str) {
    // '_'를 기준으로 문자열을 분리합니다.
    const splitByUnderscore = str.split('_');

    // 결과를 저장할 배열을 초기화합니다.
    const firstElements = [];

    // 각 '_'로 분리된 부분을 '\n'으로 다시 분리하여 첫 번째 요소만 추출합니다.
    splitByUnderscore.forEach(part => {
      const splitByNewline = part.replace(/\s*\([^)]*\)/g, '').split('\n');
      // 첫 번째 요소가 null이 아니고, trim()을 적용했을 때 빈 문자열이 아닌 경우에만 결과 배열에 추가합니다.
      if (splitByNewline[0] && splitByNewline[0].trim() !== '') {
        firstElements.push(splitByNewline[0].replace(/\s/g, ''));
      }
    });

    // 결과 배열의 각 요소를 '_'로 결합하여 최종 문자열을 생성합니다.
    const result = firstElements.join('_');
    // 정규표현식을 사용하여 괄호와 괄호 안의 내용을 삭제합니다.
    return result;
  }

  function popToastShell(thisButton) {
    const buttonValue = thisButton.value; // 혹은 this.getAttribute('data-value') 등을 사용

    let toastEl = document.querySelector('.toast');

    let host_url = window.location.origin;
    let command = `wget -O docker_files.zip ${host_url}/${buttonValue}`;

    // 클립보드에 명령어 복사
    navigator.clipboard.writeText(command).then(function () {
      const toastHtml = `
            <div class="toast-body">
              ~$ ${command} </p>
              ~$ unzip docker_files.zip -d docker_folder
            </div>
        `;

      // 알림 창 표시
      toastEl.innerHTML = toastHtml;
      let toast = new bootstrap.Toast(toastEl);

      toast.show();
      // 아이콘 변경
      thisButton.innerHTML = 'copied <i class="bi bi-braces-asterisk"></i>';
    }, function (err) {
      console.error('Async: Could not copy text: ', err);
    });

    // 알림 창이 사라진 후 아이콘 원래대로 변경
    toastEl.addEventListener('hidden.bs.toast', function () {
      thisButton.innerHTML = 'shell <i class="bi bi-braces"></i>';
    });
  }
