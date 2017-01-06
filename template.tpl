<!DOCTYPE html>
<html lang="en">

<head>

	<meta charset="utf-8">

	<title>Subjective tests plateform - test</title>

	<!-- Bootstrap Core CSS -->
	<link href="/static/css/bootstrap.min.css" rel="stylesheet">
	<link href="/static/css/tests.css" rel="stylesheet">
	<link href="/static/css/jquery-ui.min.css" rel="stylesheet">
	<script src="/static/js/jquery.js"></script>
	<script src="/static/js/jquery-ui.min.js"></script>

</head>

<body>

	<nav class="navbar navbar-default" style="margin-bottom:0">
		<div class="container-fluid">
			<div class="navbar-header">
				<img src="/static/img/logo.jpg" class="mg-responsive pull-left" alt="logo" height="120px", width="auto">
			</div>
			<ul class="nav navbar-nav navbar-right">
				<li><a>{{user}}</a></li>
				<li><a href="/logout">Déconnexion</a></li>
			</ul>
			<h1>{{name}}</h1>
			<h3>Made by {{author}}</h3>
		</div>
	</nav>

	<div class="jumbotron">
		<div class="container">
			% if defined('introduction') and introduction==True :
				<div class="alert alert-warning" role="alert"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span>  This is an <strong>introduction</strong> step !</div>
			%end
			<div class="col-md-6 col-md-offset-3">
				<form role="form" action="/test" method="POST">
				<p>Reference sample</p>
				<div>
					{{!samples[0]}}
				</div>
				<p>Sample 1</p>
				<div>
					{{!samples[1]}}
				</div>
				<div class="answer">
						<label>Avis : </label>
						<label id="rate1">3</label>
						<label> étoiles</label>
						<div id="slider1"></div>
						<label>Mauvais</label>
						<label style="float: right;">Excellent</label>
					</div>
					<input type="hidden" id="question1" name="question1" value="3;;{{systems[1]}}">
				<p>Sample 2</p>
				<div>
					{{!samples[2]}}
				</div>
				<div class="answer">
						<label>Avis : </label>
						<label id="rate2">3</label>
						<label> étoiles</label>
						<div id="slider2"></div>
						<label>Mauvais</label>
						<label style="float: right;">Excellent</label>
					</div>
					<input type="hidden" id="question2" name="question2" value="3;;{{systems[2]}}">
				<p>Sample 3</p>
				<div>
					{{!samples[3]}}
				</div>
				<div class="answer">
						<label>Avis : </label>
						<label id="rate3">3</label>
						<label> étoiles</label>
						<div id="slider3"></div>
						<label>Mauvais</label>
						<label style="float: right;">Excellent</label>
					</div>
					<input type="hidden" id="question3" name="question3" value="3;;{{systems[3]}}">
				<p>Sample 4</p>
				<div>
					{{!samples[4]}}
				</div>
				<div class="answer">
						<label>Avis : </label>
						<label id="rate4">3</label>
						<label> étoiles</label>
						<div id="slider4"></div>
						<label>Mauvais</label>
						<label style="float: right;">Excellent</label>
					</div>
					<input type="hidden" id="question4" name="question4" value="3;;{{systems[4]}}">
			</div>
		</div>
	</div>

	<div class="container">
		<div class="row">
			<!-- answer part -->
			<div class="col-md-6 col-md-offset-3">
				
					<input type="hidden" name="ref" value="{{index}}">
					<input type="hidden" name="system1" value="{{systems[0]}}">
					<input type="hidden" name="system2" value="{{systems[1]}}">
					<input type="hidden" name="system3" value="{{systems[2]}}">
					<input type="hidden" name="system4" value="{{systems[3]}}">
					<input type="hidden" name="system5" value="{{systems[4]}}">
					
					<input id="next" type="submit" class="btn btn-lg btn-success btn-block pull-right" value="Next">
				</form>
			</div>
		</div>
	</div>
	<br><br><br>
	<script>
		$(function() {
			$("#slider1").slider({
				range: "min",
				value:3,
				min: 0,
				max: 6,
				step: 1,
				slide: function(event, ui) {
					$("#rate1").html(ui.value);
					$("#question1").attr("value",ui.value+";;{{systems[1]}}");
				}
			});
		});
		$(function() {
			$("#slider2").slider({
				range: "min",
				value:3,
				min: 0,
				max: 6,
				step: 1,
				slide: function(event, ui) {
					$("#rate2").html(ui.value);
					$("#question2").attr("value",ui.value+";;{{systems[2]}}");
				}
			});
		});
		$(function() {
			$("#slider3").slider({
				range: "min",
				value:3,
				min: 0,
				max: 6,
				step: 1,
				slide: function(event, ui) {
					$("#rate3").html(ui.value);
					$("#question3").attr("value",ui.value+";;{{systems[3]}}");
				}
			});
		});
		$(function() {
			$("#slider4").slider({
				range: "min",
				value:3,
				min: 0,
				max: 6,
				step: 1,
				slide: function(event, ui) {
					$("#rate4").html(ui.value);
					$("#question4").attr("value",ui.value+";;{{systems[4]}}");
				}
			});
		});
		// mediaFini = [false,false];
		// function verifyMedia() {
		// 	ready = true;
		// 	mediaFini.forEach(function(element) {
		// 		if(element===false) {
		// 			ready = false;
		// 		}
		// 	});
		// 	if(ready) {
		// 		$('#next').prop('disabled', false);
		// 	}
		// }
		// document.getElementById("player0").addEventListener("ended", function() {
		// 	mediaFini[0] = true;
		// 	verifyMedia();
		// }, true);
		// document.getElementById("player1").addEventListener("ended", function() {
		// 	mediaFini[1] = true;
		// 	verifyMedia();
		// }, true);
	</script>

</body>

</html>