const temperatures = [0, 0, 0, 0, 0, 0, 0];
const humidities = [0, 0, 0, 0, 0, 0, 0];
const lights = [0, 0, 0, 0, 0, 0, 0];
const airPressures = [0, 0, 0, 0, 0, 0, 0];
const graphName = "temperatureGraph"
let ledStatus = [0,0]
let timeReload = 0;
var labels = ['','','','','','','']
var myChart2;
drawGraph();

async function main(){
    setInterval(async () => {
        await getTemperature()
        await getHumidity() 
        await getLightStatus()
        await getAirPressureStatus()

        var today = new Date();
        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        labels.shift()
        labels.push(time)

        myChart2.update()
    }, 2000);
}
main()

async function fetchData(url){
    const response = await fetch(url)
    return await response.json()
}