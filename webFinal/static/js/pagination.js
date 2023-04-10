window.onload = function() {
    const table = document.querySelector('.res table');
    const pagination = document.querySelector('.res .pagination');
    const rowsPerPage = 5; // 페이지당 보여줄 행 수
    let currentPage = 1;
  
    function showRows() {        
        // tbody 요소 가져오기
        const tbody = table.querySelector('tbody');
                
      // 테이블의 모든 행들을 가져와서 currentPage에 해당하는 행들만 보여줍니다.
      const rows = tbody.querySelectorAll('tr');
      const start = (currentPage - 1) * rowsPerPage;
      const end = start + rowsPerPage;
  
      rows.forEach((row, index) => {
        if (index < start || index >= end) {
          row.style.display = 'none';
        } else {
          row.style.display = '';
        }
      });
    }
  
    function createPagination() {
        // 기존 페이지 링크들을 삭제합니다.
        pagination.querySelector('ul').innerHTML = '';
      // 테이블의 총 행 수를 계산하여 페이지네이션을 생성합니다.
      const tbody = table.querySelector('tbody');
      const rows = tbody.querySelectorAll('tr');
      const totalPages = Math.ceil(rows.length / rowsPerPage);
  
      for (let i = 1; i <= totalPages; i++) {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = '#';
        a.textContent = i;
        li.appendChild(a);
        pagination.querySelector('ul').appendChild(li);
  
        a.addEventListener('click', (event) => {
          event.preventDefault();
          currentPage = i;
          showRows();
  
          const activeLink = pagination.querySelector('.active');
          if (activeLink) {
            activeLink.classList.remove('active');
          }
          li.classList.add('active');
        });
      }
    }
  
    showRows();
    createPagination();
  };
  