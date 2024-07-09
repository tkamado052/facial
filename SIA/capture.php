<?php
$user_id = $_GET['user_id'];
$username = $_GET['username'];
?>

<!DOCTYPE html>
<html>
<head>
  <title>Capture Face</title>
</head>
<body>
  <h1>Capture Face for <?php echo $username; ?></h1>
  <video id="video" width="640" height="480" autoplay></video>
  <button id="capture">Capture Face</button>
  <script>
    var video = document.getElementById('video');

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
          video.srcObject = stream;
          video.play();
        })
        .catch(function(error) {
          console.error('Error accessing webcam:', error);
        });
    } else {
      console.error('getUserMedia not supported');
    }

    document.getElementById('capture').addEventListener('click', function() {
      console.log('Capture button clicked');
      var canvas = document.createElement('canvas');
      canvas.width = 640;
      canvas.height = 480;
      var context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, 640, 480);
      var dataUrl = canvas.toDataURL('image/jpeg');
      console.log('Captured image:', dataUrl);

      // Temporary CORS workaround for development (replace with proper CORS setup)
      fetch('http://localhost:5000/capture', {
        method: 'POST',
        body: JSON.stringify({ user_id: <?php echo $user_id; ?>, image: dataUrl }),
        headers: {
          'Content-Type': 'application/json'
        },
        // **Remove this line for production**

      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert('Face captured successfully');
        } else {
          console.error('Face capture failed:', data.error);
          alert('Face capture failed. See console for details.');
        }
      })
      .catch(error => {
        console.error('Error sending capture request:', error);
        alert('Error sending capture request. See console for details.');
      });
    });
  </script>
</body>
</html>
