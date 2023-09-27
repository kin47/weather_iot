async function getLightStatus(){
    var newLight = Math.floor(Math.random() * 1000)  + 1;
    lights.shift()
    lights.push(newLight)

    var lightResult = document.querySelector("#light-result")
    lightResult.innerHTML = newLight + ""

    var classess = "stretch-card width-33 "
    var lightBackground = document.querySelector("#light-background")
    if(newLight >= 70){
        classess += "light-70"
    }
    else if(newLight >= 50){
        classess += "light-50"
    }
    else if(newLight >= 30){
        classess += "light-30"
    }
    else{
        classess += "light-0"
    }
    lightBackground.setAttribute("class", classess)
}