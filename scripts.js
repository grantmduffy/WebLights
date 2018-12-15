function sendRequest(){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        document.getElementById("response").innerHTML = this.responseText;
    }
    request.open('POST', 'state.json', true)
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.send(JSON.stringify({'led1':0, 'led2':1}))
}