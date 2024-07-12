// currentTime.js
document.addEventListener("DOMContentLoaded", function() {
    function updateTime() {
        var now = new Date();
        var hours = now.getHours().toString().padStart(2, '0');
        var minutes = now.getMinutes().toString().padStart(2, '0');
        var seconds = now.getSeconds().toString().padStart(2, '0');
        var currentTime = hours + ':' + minutes + ':' + seconds;
        document.getElementById("current-time").textContent = currentTime;
    }

    updateTime(); // Call it once to set the time immediately
    setInterval(updateTime, 1000); // Update the time every second
});
