function sendRequest(data){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        document.getElementById("response").innerHTML = this.responseText;
    }
    request.open('POST', 'state.json', true)
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.send(JSON.stringify(data))
}

function on1(){sendRequest({'led1':1})}
function on2(){sendRequest({'led2':1})}
function off1(){sendRequest({'led1':0})}
function off2(){sendRequest({'led2':0})}
