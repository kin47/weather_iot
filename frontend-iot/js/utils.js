port = 8000;
prefixUrl = `http://${document.domain}:${port}/`;

function redirect(url) {
    console.log(url);
    const aTag = document.createElement('a');
    aTag.href = url;
    document.querySelector('body').insertAdjacentElement('afterbegin', aTag);
    aTag.click();
}

async function callAPI(url, method,  data=null, handler) {
    apiUrl = `${prefixUrl}${url}`;
    accessToken = localStorage.getItem('accessToken') ? localStorage.getItem('accessToken') : 'abcxyz';

    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", handler);

    xhr.open(method, apiUrl, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Authorization", `Bearer ${accessToken}`);
    xhr.send(data);
}

function unauthorizedPage() {
    redirect(`http://${document.domain}:${location.port}/N17-IoT/error/401_unauthorized.html`);
}

function badGetWay() {
    redirect(`http://${document.domain}:${location.port}/N17-IoT/error/502_badgetway.html`);
}
