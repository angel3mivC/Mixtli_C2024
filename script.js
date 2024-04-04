document.addEventListener("DOMContentLoaded", function () {
    var cameraContainer = document.getElementById('camera_container');

    navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
        var videoElement = document.createElement('video');
        videoElement.autoplay = true;
        videoElement.srcObject = stream;

        cameraContainer.appendChild(videoElement);
    })
    .catch(function (error) {
        console.error('Error al acceder a la cámara:', error);
    });
});
