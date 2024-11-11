var isDroneStarted = false;

function emergency_stop() {
    console.log("Emergency stop");
    isDroneStarted = false;
    toggleOnAirText();
    // fetch("http://192.168.10.2:5000/emergency_stop")
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log(data);
    //         alert(JSON.stringify(data));
    //         toggleOnAirText();
    //     })
    //     .catch(error => console.error('Error:', error));
}

function start() {
    console.log("Starting drone sequences");
    isDroneStarted = true;
    toggleOnAirText();
    // fetch("http://192.168.10.2:5000/start")
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log(data);
    //         alert(JSON.stringify(data));
    //         toggleOnAirText();
    //     })
    //     .catch(error => console.error("Error:", error));
    
}

function land(){
    console.log("Landing drone");
    isDroneStarted = false;
    toggleOnAirText();
    // fetch("http://192.168.10.2:5000/land")
    //     .then(response => response.json())
    //     .then(data => {
    //     console.log(data);
    //     alert(JSON.stringify(data));
    //     toggleOnAirText();
    // })
    // .catch(error => console.error("Error:", error));
}

function toggleOnAirText() {
    var onAirElement = document.getElementById("onair");
    onAirElement.textContent = isDroneStarted ? "ON AIR" : "ON LAND";
}

// Configuración para acceder a la cámara del dispositivo
function setupDeviceCamera() {
    var videoElement = document.getElementById("drone_video");

    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            videoElement.srcObject = stream;
        })
        .catch((error) => {
            console.error("Error accessing device camera:", error);
            alert("No se pudo acceder a la cámara del dispositivo.");
        });
}

function setupDroneCamera() {
    var videoElement = document.getElementById("drone_video");
    
    videoElement.src = "http://192.168.10.2:5000/video_feed";
}

document.addEventListener("DOMContentLoaded", function () {
    toggleOnAirText(false);
    setupDeviceCamera();
});