const port = 8000;
const domain = '192.168.1.10';
const prefixUrl = `http://${domain}:${port}/`;

function callAPI(url, method,  data=null, handler) {
    if (data instanceof FormData) {
        console.log(data.get('jsonData'));
    }
    apiUrl = `${prefixUrl}${url}`;
    accessToken = localStorage.getItem('accessToken') ? localStorage.getItem('accessToken') : 'abcxyz';

    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", handler);

    xhr.open(method, apiUrl, true);
    xhr.setRequestHeader("Authorization", `Bearer ${accessToken}`);
    xhr.send(data);
}

function redirect(url) {
    console.log(url);
    const aTag = document.createElement('a');
    aTag.href = url;
    document.querySelector('body').insertAdjacentElement('afterbegin', aTag);
    aTag.click();
}

function homePage() {
    redirect(`http://${document.domain}:${location.port}/N17-IoT/home.html`)
}

callAPI('api/authen/me', 'GET', null, function() {
    if (this.readyState === 4) {
        data = JSON.parse(this.responseText);
        if (this.status == 200) {
            homePage();
        }
        else if (this.status == 401) {
            console.log('Login please !!!');
        }
    }
});