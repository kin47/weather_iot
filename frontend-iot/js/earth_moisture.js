async function getAirPressureStatus(newAirPressure) {
    // var newAirPressure = Math.floor(Math.random() * 100) + 1;
    airPressures.shift()
    airPressures.push(newAirPressure)

    // var airPressureResult = document.querySelector("#earth-moisture-result")
    // airPressureResult.innerHTML = newAirPressure + " %"

    var classess = "stretch-card width-24 "
    var airPressureBackground = document.querySelector("#earth-moisture-background")
    if (newAirPressure >= 100) {
        classess += "earth-moisture-100"
    }
    else if (newAirPressure >= 75) {
        classess += "earth-moisture-75"
    }
    else if (newAirPressure >= 50) {
        classess += "earth-moisture-50"
    }
    else if (newAirPressure >= 25) {
        classess += "earth-moisture-25"
    }
    else {
        classess += "earth-moisture-0"
    }
    airPressureBackground.setAttribute("class", classess)
}