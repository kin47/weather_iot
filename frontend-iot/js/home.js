callAPI('api/authen/me', 'GET', null, function() {
    if (this.readyState === 4) {
        data = JSON.parse(this.responseText);
        if (this.status == 200) {
            document.querySelector('#username span').innerText = data['username'];
            document.querySelector('#email span').innerText = data['email'];
        }
        else if (this.status == 401) {
            redirect('./error/401_unauthorized.html');
        }
    }
});
