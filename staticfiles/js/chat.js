document.addEventListener("DOMContentLoaded", function () {
    const chatBody = document.getElementById("chatBody");
    if (chatBody) {
        chatBody.scrollTop = chatBody.scrollHeight;
    }
});

