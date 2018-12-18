function sendRequest(data){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        document.getElementById("response").innerHTML = this.responseText;
    }
    request.open('POST', '/state.json', false)
    request.send(JSON.stringify(data))
}

function updateColor(){
    r = document.getElementById("red").value;
    g = document.getElementById("green").value;
    b = document.getElementById("blue").value;
    sendRequest({
        'r': r,
        'g': g,
        'b': b
    })
    color = "rgb(" + r + ", " + g + ", " + b + ")"
    return color
}

function onRed(){
    updateColor();
}
function onGreen() {
    updateColor();
}
function onBlue() {
    updateColor();
}