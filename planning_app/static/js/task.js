var taskCode = document.getElementById("task").getAttribute("task_code");
console.log("task code", taskCode)

var connectionString = 'ws://' + window.location.host + '/ws/task/' + taskCode + '/';
var taskSocket = new WebSocket(connectionString);

var voteChoice = document.getElementsByName("vote")

var currentChoice = document.getElementById("chosen").getAttribute("value");
console.log(currentChoice)

if (currentChoice >= 0) {
    var radioBtn = document.getElementById(`option_${currentChoice}`);
    radioBtn.checked = true
}

for (vote_radio in voteChoice) {
    voteChoice[vote_radio].onclick = function (event) {
        option = document.getElementById(event.target.id)
        newChoice = option.value
        serverData = {"task_code": taskCode, "current_choice": currentChoice, "new_choice": newChoice}
        taskSocket.send(JSON.stringify({"event" : "UPDATE", "data" : serverData}))
        voteChoice = newChoice;
        event.target.checked = true;
    }
}
    
function connect() {
    taskSocket.onopen = function open() {
        console.log('WebSockets connection created.');
        taskSocket.send(JSON.stringify({
            "event": "START",
            "data": {"task_code": taskCode}
        }));
    };

    taskSocket.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(function () {
            connect();
        }, 1000);
    };
    // Sending the info about the room
    taskSocket.onmessage = function (e) {
        let data = JSON.parse(e.data);
        console.log("data from server", data)
        count = data.count

        for (const [key, value] of Object.entries(count)) {
            var elementId = `option_${key}_count`
            label = document.getElementById(elementId)
            label.innerHTML = `vote count ${value}`
            // console.log("updated")
        }
    };

    if (taskSocket.readyState == WebSocket.OPEN) {
        taskSocket.onopen();
    }
}

connect();