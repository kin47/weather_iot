callAPI('api/authen/me', 'GET', null, function() {
    if (this.readyState === 4) {
        data = JSON.parse(this.responseText);
        if (this.status == 401) {
            unauthorizedPage();
        }
    }
});

const onopenHandler = (event) => {
    console.log('Connected to server ...');
}

const onerrorHandler = (event) => {
    console.error('WebSocket connection error:', error);
}

const onmessageHandler = (event) => {
    const data = JSON.parse(event.data);
    const dataShows = [
        null,
        document.querySelector('#temperature-result span'),
        document.querySelector('#humidity-result span'),
        document.querySelector('#light-result span'),
        document.querySelector('#earth-moisture-result span'),
    ];

    Object.keys(data).forEach((key, index) => {
        if (key != 'authen') {
            dataShows[index].innerText = data[key];
        }
    });
    main(data['temperature'], data['humidity'], data['lightValue'], data['earthMoisture']);
}

const oncloseHandler = (event) => {
    console.log('Disconnected to server ...');
}

connectWebsocket('esp32/websocket', onopenHandler, onmessageHandler, oncloseHandler, onerrorHandler);
