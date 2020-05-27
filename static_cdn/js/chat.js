var roomName = JSON.parse(document.getElementById("room-name").textContent);
// let userList = $("#user-list");

// function updateUserList() {
//   $.getJSON("api/v1/user/", function (data) {
//     userList.children(".user").remove();
//     for (let i = 0; i < data.length; i++) {
//       const userItem = `<a class="list-group-item user">${data[i]["username"]}</a>`;
//       $(userItem).appendTo("#user-list");
//     }
//     $(".user").click(function () {
//       userList.children(".active").removeClass("active");
//       let selected = event.target;
//       $(selected).addClass("active");
//       setCurrentRecipient(selected.text);
//     });
//   });
// }

var chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/chat/" + roomName + "/"
);

chatSocket.onmessage = function (e) {
  var data = JSON.parse(e.data);
  document.querySelector("#chat-log").value += data.message + "\n";
};

chatSocket.onclose = function (e) {
  console.error("Chat socket closed unexpectedly");
};

document.querySelector("#chat-message-input").focus();
document.querySelector("#chat-message-input").onkeyup = function (e) {
  if (e.keyCode === 13) {
    // enter, return
    document.querySelector("#chat-message-submit").click();
  }
};

document.querySelector("#chat-message-submit").onclick = function (e) {
  var messageInputDom = document.querySelector("#chat-message-input");
  var message = messageInputDom.value;
  chatSocket.send(
    JSON.stringify({
      message: message,
    })
  );
  messageInputDom.value = " ";
};
