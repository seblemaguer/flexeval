
<!DOCTYPE html>
<html lang="en">

<head>

	<meta charset="utf-8">

	<title>Subjective tests plateform - {{config["name"]}}</title>

	<!-- Bootstrap Core CSS -->
	<link href="{{APP_PREFIX}}/static/css/bootstrap.min.css" rel="stylesheet">
	<link href="{{APP_PREFIX}}/static/css/tests.css" rel="stylesheet">
	<link href="{{APP_PREFIX}}/static/css/jquery-ui.min.css" rel="stylesheet">
	<link href="{{APP_PREFIX}}/static/css/perceval.css" rel="stylesheet">
	<script src="{{APP_PREFIX}}/static/js/jquery.js"></script>
	<script src="{{APP_PREFIX}}/static/js/jquery-ui.min.js"></script>
	<script src="{{APP_PREFIX}}/static/js/perceval.js"></script>

</head>

<body>

	<div class="container">
		<div class="row">
			<div class="col-md-4 col-md-offset-4 text-center">
			<h1>{{config["name"]}}</h1>
			<p class="lead">{{config["description"]}}</p>
			</div>
		</div>
	</div>

	<div class="jumbotron">
		<div class="container">
			<div class="row">
				<div class="col-md-6 col-md-offset-3">
					<h2 class="text-center">L'évaluation est maintenant terminée !</h2>
					<h2 class="text-center">Merci d'avoir pris le temps d'y répondre.</h2>
					<br>
					<br>
					<h4 class="text-center">Vous avez été déconnecté. Vous pouvez fermer cette page.</h4>
					<br>
				</div>

				<div class="col-md-6 col-md-offset-3">


					<div id="feedbackcompl" style="display:none">


						<div class="alert alert-success" role="alert">
						Merci d'avoir complété le formulaire de retour.
						</div>


		
					</div>

					<div id="feedback">
						<h2 class="text-center">Un commentaire ?</h2>
						<p> La complétion du formulaire suivant est optionnel. </p>

						<form  action="">
							<div class="form-group">
							    <label for="courriel">Courriel</label>
							    <input type="email" class="form-control" id="courriel" aria-describedby="emailHelp" placeholder="Courriel" />
	 						</div>

							<div class="form-group">
							    <label for="comment">Commentaire</label>
							    <textarea class="form-control" id="commentaire" rows="3"></textarea>
	 						</div>

							<div class="form-group">
							    <label for="video">Faire un commentaire vidéo</label>

								<div id="container">

								<div class="select">
								    <label for="audioSource">Audio source: </label><select id="audioSource"></select>
								  </div>

								  <div class="select">
								    <label for="videoSource">Video source: </label><select id="videoSource"></select>
								  </div>

								<video id="webplayer" mute autoplay></video>

								</div>



								<a href="#webplayer" class="btn btn-primary" style="display:none" id="stop">Stop</a>
								<a href="#webplayer" class="btn btn-primary" id="start">Start</a>


	 						</div>

							<a id="submitcomments" class="btn btn-success" href="#webplayer"> Envoyer </a>

						</form>
					</div>
				</div>

			</div>
		</div>
	</div>

	<div class="container" style="padding: 0px;">
		<div class="row">
			<div class="col-sm-offset-2 col-sm-4 col-md-offset-3 col-md-3">
				<a href="http://www.irisa.fr" target="_blank">
					<img src="{{APP_PREFIX}}/static/img/logo_irisa.png" class="img-responsive center-block" alt="IRISA lab">
				</a>
			</div>
			<div class="col-sm-4 col-md-3">
				<a href="http://www-expression.irisa.fr" target="_blank">
					<img src="{{APP_PREFIX}}/static/img/logo_expression.png" class="img-responsive center-block" alt="Expression team">
				</a>
			</div>
		</div>
		<p class="text-muted text-center" style="letter-spacing: 2px; line-height: 40px;"><a href="https://gitlab.inria.fr/dlolive/PercepEval" target="_blank">Powered by PercEval.</a></p>
	</div>


</body>

<script>

const videoElement = document.querySelector('video');
const audioSelect = document.querySelector('select#audioSource');
const videoSelect = document.querySelector('select#videoSource');

const DIVstartRecord = document.querySelector('#start');
const DIVstopRecord = document.querySelector('#stop');

var mediaRecorder;
var chunks = [];

navigator.mediaDevices.enumerateDevices()
  .then(gotDevices).then(getStream).catch(handleError);

audioSelect.onchange = getStream;
videoSelect.onchange = getStream;

function gotDevices(deviceInfos) {
  for (let i = 0; i !== deviceInfos.length; ++i) {
    const deviceInfo = deviceInfos[i];
    const option = document.createElement('option');
    option.value = deviceInfo.deviceId;
    if (deviceInfo.kind === 'audioinput') {
      option.text = deviceInfo.label ||
        'microphone ' + (audioSelect.length + 1);
      audioSelect.appendChild(option);
    } else if (deviceInfo.kind === 'videoinput') {
      option.text = deviceInfo.label || 'camera ' +
        (videoSelect.length + 1);
      videoSelect.appendChild(option);
    } else {
      console.log('Found another kind of device: ', deviceInfo);
    }
  }
}

function getStream() {
  if (window.stream) {
    window.stream.getTracks().forEach(function(track) {
      track.stop();
    });
  }

  const constraints = {
    audio: {
      deviceId: {exact: audioSelect.value}
    },
    video: {
      deviceId: {exact: videoSelect.value}
    }
  };

  navigator.mediaDevices.getUserMedia(constraints).
    then(gotStream).catch(handleError);
}

var BlobRec=null;

function gotStream(stream) {
  window.stream = stream; // make stream available to console
  videoElement.srcObject = stream;
  mediaRecorder = new MediaRecorder(window.stream);

	mediaRecorder.onstop = function(e) {
	  console.log("recorder stopped");

	  var blob = new Blob(chunks, { 'type' : 'video/webm;codecs=h264' });
	  chunks = [];
	  var videoURL = window.URL.createObjectURL(blob);
	  console.log(videoURL);
	  
          BlobRec=blob;

	}


	mediaRecorder.ondataavailable = function(e) {
	  chunks.push(e.data);
	}

}


function handleError(error) {
  console.error('Error: ', error);
}

/*
 ON S OCCUPE DE LA CAPTURE MEDIA
 /!\ On utilise l'api MediaRecorder vérifier la compatibilité des navs.
 Préciser cela lors de la transmission de ce code.
Doc:https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API/Using_the_MediaStream_Recording_API
*/


DIVstartRecord.onclick = function (e)
{
  mediaRecorder.start();
  console.log(mediaRecorder.state);
  console.log("recorder started");
  $("#start").css("display","none");
  $("#stop").css("display","block");
};

DIVstopRecord.onclick = function(e){

  mediaRecorder.stop();
  console.log(mediaRecorder.state);
  console.log("recorder stopped");
  $("#start").css("display","inline");
  $("#stop").css("display","none");

};

$("#submitcomments").click((e) =>
{

	var formData = new FormData();

	formData.append("courriel", $("#courriel").val());
	formData.append("commentaire", $("#commentaire").val()); // le numéro 123456 est converti immédiatement en chaîne "123456"

	formData.append("video", BlobRec);

	var request = new XMLHttpRequest();
	request.open("POST", "/perso/lsf/commentaires");
	request.send(formData);

	$("#feedback").css("display","none");
	$("#feedbackcompl").css("display","block");
	

});

/*
INIT
*/

/*


*/
</script>
</html>
