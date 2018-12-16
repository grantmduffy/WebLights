function sendRequest(data){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        document.getElementById("response").innerHTML = this.responseText;
    }
    request.open('POST', 'state.json', true)
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.send(JSON.stringify(data))
}

function updateColor(){
    r = document.getElementById("red").value;
    g = document.getElementById("green").value;
    b = document.getElementById("blue").value;
    sendRequest({
        'r': r,
        'g': b,
        'b': b
    })
    color = "rgb(" + r.toString(16) + ", " + g.toString(15) + ", " + b.toString(15) + ")"
    return color
}

function on1(){sendRequest({'led1':1});}
function on2(){sendRequest({'led2':1});}
function off1(){sendRequest({'led1':0});}
function off2(){sendRequest({'led2':0});}

function onRed(){
    document.getElementById("sliders").style.backgroundColor = updateColor();
}
function onGreen() {
    document.getElementById("sliders").style.backgroundColor = updateColor();
}
function onBlue() {
    document.getElementById("sliders").style.backgroundColor = updateColor();
}