// Since this tends to take a while, this function is asychronous.
async function chat() {
    var input = document.getElementById("chatbox");
    var display = document.getElementById("textarea");
    var data =  JSON.parse(JSON.stringify(input.value)); 
    input.value = "";
    input.disabled = true;
    input.placeholder = "Please wait..."
    display.scrollTop += 10000;
    await new Promise(r => setTimeout(r, 1000));
    console.log("Sending " + data)
    $.post("/sendmsg", data, function(){
        $.post("/data/server", data, function(result){
        input.placeholder = "Message #" + result.substring(5,16) 
        input.disabled = false;
        getLog();
        })
    });
    return false;
}

// Button #1. Shows the user their wallet's transaction history.
function getAddress(){
    $.post("/data/address", function(result){
        window.open("https://nanocrawler.cc/explorer/account/" + String(result));
    })
}

// Button #2. When pressed, directs the user to a Nano faucet, where they can obtain a free sample amount of Nano.
function getFunds(){
    $.post("/data/address", function(result){
        alert("Please copy the following address into the next window: " + result);
        window.open("https://freenanofaucet.com/");
    })
    checkReceive()    
}

// Starts after the user has completed the above process.
// Waits for there to be transactions to confirm, and confirms them once they're there.
function checkReceive(){
    document.getElementById("chatbox").placeholder = "Receiving Nano, please wait..."
    $.post("/data/balance", function(result){
        if (String(result) == 0){
            setTimeout(checkReceive, 30000)
        }
        else {
            location.reload();
        }
    })
}

// Ensures that a user has the funds necessary to chat before allowing them to type a message.
function checkWorth() {
    $.post("/data/balance", function(result){
        var input = document.getElementById("chatbox");
        if (result == 0){
            input.value = "";
            input.disabled = true;
            input.placeholder = "You need Nano in order to begin sending messages."
        }
        else {
            $.post("/data/server", function(result){
                input.placeholder = "Message #" + result.substring(5,16) 
            });
        }
    })
}

// Initializes the window and updates the messages on the screen.
function getLog() {
    $.post("/data/log", function(result){
        var display = document.getElementById("textarea");
        var log = JSON.parse(result)
        while(display.firstChild) {
            display.removeChild(display.firstChild)
        }
        for (x in log) {
            var br = document.createElement("br");
            var name = document.createElement("span")
            name.textContent = "<" + String(log[x]).substring(5, 20) + ">"
            name.setAttribute("id","username");
            name.style.color = String(log[x]).substring(66,73)
            var text = document.createElement("span");
            text.textContent = String(log[x]).substring(74)
            display.appendChild(name);
            display.appendChild(text);
            display.appendChild(br);
            display.scrollTop += 10000;
        }
    });
    return true // prevents page from refreshing after submission
}

// Initialization functions.
window.onload = function() { 
    checkWorth();
    getLog();
};

// Updates the messages on the screen every fifteen seconds.
setInterval(function(){getLog();}, 15000);       
 