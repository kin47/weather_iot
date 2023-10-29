callAPI('api/authen/me', 'GET', '', function() {
    if (this.readyState === 4) {
        if (this.status == 401) {
            unauthorizedPage();
        }
    }
});

const piwv = 5;
const iip = 10;

function renderTable(response, currentPage) {
    const panelNoData = document.querySelector('#panel-no-data');
    const phanTrang = document.querySelector('.phanTrang');
    const btnPaginations = document.querySelector('.phanTrang ul');
    const tbody = document.querySelector('tbody');
    let htmlTable = '';
    const data = response['dataOfPage'];
    for (item of data) {
        htmlTable = htmlTable + `
            <tr>
                <td>${item.STT}</td>
                <td>${item.sentAt}</td>
                <td>${item.nhietDo}°C</td>
                <td>${item.doAmKhongKhi}%</td>
                <td>${item.anhSang} lx</td>
                <td>${item.doAmDat}%</td>
            </tr>`;
    }
    
    tbody.innerHTML = htmlTable;
    panelNoData.style.display = 'none';
    phanTrang.style.display = 'block';

    const startPage = response['startPage'];
    const endPage = response['endPage'];
    const totalPages = response['totalPages'];

    let htmlPagination = currentPage == 1 ? '' :
    `<li class="numb item-${currentPage - 1} nutPaginate" style="color: white">
        <span><i class="fas fa-angle-left"></i></span>
    </li>`;
 
    for (let i = startPage; i <= endPage; i++) {
        if (i != currentPage) {
            htmlPagination = htmlPagination +
            `<li class="numb item-${i} inactive"><span>${i}</span></li>`;
        }
        else {
            htmlPagination = htmlPagination +
            `<li class="numb item-${i} active"><span>${i}</span></li>`;
        }
    }

    htmlPagination =
    `<span class="soTrang">
        ${htmlPagination}
    </span>`;

    htmlPagination = htmlPagination + (
        currentPage == totalPages ? '' :
        `<li class="numb item-${currentPage + 1} nutPaginate" style="color: white">
            <span><i class="fas fa-angle-right"></i></span>
        </li>`
    );

    btnPaginations.innerHTML = htmlPagination;
    console.log(currentPage);

    document.querySelectorAll('.numb').forEach(record => {
        const index = parseInt(record.classList[1].split('-')[1]);
        record.onclick = () => {
            let url = `api/esp32/data?piwv=${piwv}&iip=${iip}&page=${index}`;
            const startDate = document.querySelector('#start-date').value;
            const endDate = document.querySelector('#end-date').value;

            if (startDate) {
                url = url + `&startDate=${startDate}`;
            }

            if (endDate) {
                url = url + `&endDate=${endDate}`;
            }

            callAPI(url, 'GET', '', function() {
                if (this.readyState === 4) {
                    let data = JSON.parse(this.responseText);
                    if (this.status == 200) {
                        console.log(data);
                        renderTable(data, index);
                    }
                    else if (this.status == 400) {
                        alert(data['message']);
                    }
                    else if (this.status == 401) {
                        unauthorizedPage();
                    }
                }
            });
        }
    });
}

document.querySelector('#btn-loc-du-lieu').onclick = () => {
    let url = `api/esp32/data?piwv=${piwv}&iip=${iip}&&page=1`;
    const startDate = document.querySelector('#start-date').value;
    const endDate = document.querySelector('#end-date').value;

    if (startDate) {
        url = url + `&startDate=${startDate}`;
    }

    if (endDate) {
        url = url + `&endDate=${endDate}`;
    }
    callAPI(url, 'GET', '', function() {
        if (this.readyState === 4) {
            let data = JSON.parse(this.responseText);
            if (this.status == 200) {
                console.log(data);
                renderTable(data, 1);
            }
            else if (this.status == 400) {
                alert(data['message']);
            }
            else if (this.status == 401) {
                unauthorizedPage();
            }
        }
    });
}
