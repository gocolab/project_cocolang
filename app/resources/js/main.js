// main.js

function fetchComoduleDetails(comoduleId) {
    fetch(`/comodules/v1/${comoduleId}`)
      .then(response => response.json())
      .then(data => {
        updateComoduleDetails(data);
      })
      .catch(error => console.error('Error fetching comodule details:', error));
  }
  
  function updateComoduleDetails(data = null) {
    const referComodulesButton = document.querySelector('#refer_comodules_button');
    if (referComodulesButton) {
      referComodulesButton.disabled = true; // 버튼을 활성화합니다.
    }
  
    const cardBody = document.querySelector('#detail');
    let newContent = '';
  
    if (data) {
      newContent = `
          <div class="row">
            <div class="col-5 fw-bold">visibility / Level</div>
            <div class="col-7">${data.visibility} / lv.${data.level}</div>
            <div class="col-5 fw-bold">Main Service</div>
            <div class="col-7">${data.title}</div>
            <div class="col-5 fw-bold">Language</div>
            <div class="col-7">${data.language_name}</div>
            <div class="col-5 fw-bold">Framework</div>
            <div class="col-7">${data.framework_name}</div>
            <div class="col-5 fw-bold">Database</div>
            <div class="col-7">${data.database_name}</div>
            <div class="col-5 fw-bold">Docker Files</div>
            <div class="col-7">
              <div>
                <a href="/comodules/download/${data._id ? data._id : data.id}" class="btn btn-sm btn-info" id="download_all">
                  zip <i class="bi bi-cloud-download"></i>
                </a>
                <button class="btn btn-sm btn-info setupButton my-1"
                value="${data.language_name}_${data.framework_name}_${data.database_name}">
                setup <i class="bi bi-clipboard"></i>
              </button>
              <button class="btn btn-sm btn-info shellButton"
                value="comodules/r/download/${ data.id }">
                shell <i class="bi bi-braces"></i>
              </button>
              </div>
            </div>
            <div class="col-5 fw-bold">Owner</div>
            <div class="col-7">
              ${data.create_user_name ? data.create_user_name : ""}
            </div>
          </div>`;
  
      const refer_comodules_id = document.querySelector('#refer_comodules_id');
      const visibility = document.querySelector('#visibility');
      if (refer_comodules_id) {
        if (data.id) {
          refer_comodules_id.value = data.id;
        } else {
          refer_comodules_id.value = data._id;
        }
        visibility.value = data.visibility;
        referComodulesButton.disabled = false; // 버튼을 활성화합니다.        
      }
    }
  
    cardBody.innerHTML = newContent;
  
    document.querySelector('.setupButton').addEventListener('click', function (event) {
      event.preventDefault();
      const self = this;
      popToastSetup(self);
    });
  
    document.querySelector('.shellButton').addEventListener('click', function (event) {
      event.preventDefault();
      const self = this;
      popToastShell(self);
    });
  }
  
  function fetchComodulesData(pageNum = 1) {
    const activeLanguages = Array.from(document.querySelectorAll('.btn.language.btn-primary')).map(btn => btn.textContent.trim());
    const activeFrameworks = Array.from(document.querySelectorAll('.btn.framework.btn-primary')).map(btn => btn.textContent.trim());
    const activeDatabase = Array.from(document.querySelectorAll('.btn.database.btn-primary')).map(btn => btn.textContent.trim());
    const searchQuery = document.querySelector('#search_input').value.trim();
  
    const queryParams = new URLSearchParams({
      search_word: searchQuery,
      page_number: pageNum,
      language: activeLanguages.join(','),
      framework: activeFrameworks.join(','),
      database: activeDatabase.join(',')
    });
  
    fetch(`/comodules/v1/list/main?${queryParams}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        updateComodulesList(data);
        updatePagination(data.pagination);
        let comodule = null
        if (data.comodules.length > 0) {
          comodule = data.comodules[0];
        }
        updateComoduleDetails(comodule);
  
        const total_records = document.querySelector('#total_records');
        total_records.innerHTML = data.total_records;
      })
      .catch(error => console.error('Error fetching the list:', error));
  }
  
  function updateComodulesList(data) {
    const listGroup = document.querySelector('.list-group');
    listGroup.innerHTML = '';
    data.comodules.forEach(function (comodule) {
      const listItem = document.createElement('li');
      listItem.className = 'list-group-item lh-sm';
      listItem.setAttribute('data-id', comodule.id);
      listItem.innerHTML = `
            <div class="">
                <h6 class="my-0">${comodule.title}</h6>
                <div class="text-body-secondary small">
                    ${comodule.language_name} ${comodule.framework_name} ${comodule.database_name}
                </div>
            </div>
        `;
      listGroup.appendChild(listItem);
    });
  }
  
  function updatePagination(pagination) {
    const paginationContainer = document.querySelector('#comodules_list_pagination');
    const ul = paginationContainer.querySelector('.pagination');
    ul.innerHTML = '';
  
    const prevLi = document.createElement('li');
    prevLi.className = `page-item ${pagination.has_previous_page ? '' : 'disabled'}`;
    prevLi.innerHTML = `<button type="submit" class="page-link" value="${pagination.previous_page}">Prev</button>`;
    ul.appendChild(prevLi);
  
    pagination.current_page_range.forEach(function (pageNum) {
      const li = document.createElement('li');
      li.className = `page-item ${pageNum === pagination.current_page ? 'active' : ''}`;
      li.innerHTML = `<button type="submit" class="page-link" value="${pageNum}">${pageNum}</button>`;
      ul.appendChild(li);
    });
  
    const nextLi = document.createElement('li');
    nextLi.className = `page-item ${pagination.has_next_page ? '' : 'disabled'}`;
    nextLi.innerHTML = `<button type="submit" class="page-link" value="${pagination.next_page}">Next</button>`;
    ul.appendChild(nextLi);
  
    ul.querySelectorAll('.page-item').forEach(function (item) {
      item.addEventListener('click', function (event) {
        if (!item.classList.contains('disabled') && !item.classList.contains('active')) {
          const pageNum = item.querySelector('button').value;
          fetchComodulesData(pageNum);
        }
      });
    });
  }
  
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelector('.list-group').addEventListener('click', function (event) {
      let target = event.target;
      while (target != this && !target.matches('.list-group-item')) {
        target = target.parentNode;
      }
      if (target.matches('.list-group-item')) {
        const comoduleId = target.getAttribute('data-id');
        fetchComoduleDetails(comoduleId);
      }
    });
  
    document.querySelector('#button-search').addEventListener('click', function (event) {
      event.preventDefault();
      fetchComodulesData();
    });
  
    document.querySelector('#comodules_list_pagination').addEventListener('click', function (event) {
      const target = event.target;
      if (target.tagName === 'BUTTON' && target.type === 'submit') {
        event.preventDefault();
        const pageNum = target.value;
        fetchComodulesData(pageNum);
      }
    });
  
    let buttons = document.querySelectorAll("#interactiveTable button");
  
    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        const buttonType = button.className.includes('language') ? 'language' :
          button.className.includes('framework') ? 'framework' : 'database';
        button.classList.toggle("btn-light");
        button.classList.toggle("btn-primary");
        fetchComodulesData();
      });
    });
  
    document.querySelector('#search_input').addEventListener('keydown', function (event) {
      if (event.key === 'Enter') {
        event.preventDefault();
        fetchComodulesData();
      }
    });
  
    fetchComodulesData();
  });
  