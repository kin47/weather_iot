async function getLightStatus() {
    var newLight = Math.floor(Math.random() * 1000) + 1;
    lights.shift()
    lights.push(newLight)

    var lightResult = document.querySelector("#light-result")
    lightResult.innerHTML = newLight + " lx"

    var classess = "stretch-card width-24 "
    var lightBackground = document.querySelector("#light-background")
    if (newLight >= 1000) {
        classess += "light-1000"
    }
    else if (newLight >= 750) {
        classess += "light-750"
    }
    else if (newLight >= 500) {
        classess += "light-500"
    }
    else if (newLight >= 250) {
        classess += "light-250"
    }
    else {
        classess += "light-0"
    }
    lightBackground.setAttribute("class", classess)
}