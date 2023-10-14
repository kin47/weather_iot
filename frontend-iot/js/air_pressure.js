async function getAirPressureStatus() {
    var newAirPressure = Math.floor(Math.random() * 1000) + 1;
    airPressures.shift()
    airPressures.push(newAirPressure)

    var airPressureResult = document.querySelector("#air-pressure-result")
    airPressureResult.innerHTML = newAirPressure + " hPa"

    var classess = "stretch-card width-24 "
    var airPressureBackground = document.querySelector("#air-pressure-background")
    if (newAirPressure >= 1000) {
        classess += "air-pressure-1000"
    }
    else if (newAirPressure >= 750) {
        classess += "air-pressure-750"
    }
    else if (newAirPressure >= 500) {
        classess += "air-pressure-500"
    }
    else if (newAirPressure >= 250) {
        classess += "air-pressure-250"
    }
    else {
        classess += "air-pressure-0"
    }
    airPressureBackground.setAttribute("class", classess)
}