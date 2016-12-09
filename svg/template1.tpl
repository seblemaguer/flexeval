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

	<div class="jumbotron">
		<div class="container">
			<div class="col-md-6 col-md-offset-3">
				<h1>{{ name}}</h1><span><h3>Made by {{author}}</h3>
				<p class="lead">{{description}}</p>
				% for i in range(len(samples)):
				<p>Sample {{i+1}}</p>
				<audio id="player" controls>
					<source src="{{samples[i]}}">
				</audio>
				% end
				</div>
			</div>
		</div>
	</div>

	<div class="container">
		<div class="row">
			<!-- answer part -->
			<div class="col-md-6 col-md-offset-3">
				<form role="form" action="/test" method="POST">
					<input type="hidden" name="ref" value="{{index}}">
					<h3>Question </h3>
					<div class="alert alert-info" role="alert">Langage le plus naturel?</div>
					<div class="col-md-offset-2">
						<div class="radio">
							<label>
								<input type="radio" id="radioA" name="question1" value="{{systems[0]}}">
								Sample 1
							</label>
						</div>
						<div class="radio">
							<label>
								<input type="radio" id="radioB" name="question1" value="{{systems[1]}}">
								Sample 2
							</label>
						</div>
					</div>
					
					<h3>Question </h3>
					<div class="alert alert-info" role="alert">Meilleure qualité générale</div>
					<div class="col-md-offset-2">
						<div class="radio">
							<label>
								<input type="radio" id="radioA" name="question2" value="{{systems[0]}}">
								Sample 1
							</label>
						</div>
						<div class="radio">
							<label>
								<input type="radio" id="radioB" name="question2" value="{{systems[1]}}">
								Sample 2
							</label>
						</div>
					</div>

					<h3>Question </h3>
					<div class="alert alert-info" role="alert">Veuillez évaluer le sample 1</div>
					<!-- use the slider -->
					<div class="answer">
						<label>Avis : </label>
						<label id="rate3">3</label>
						<label> étoiles</label>
						<div id="slider3"></div>
						<label>Mauvais</label>
						<label style="float: right;">Excellent</label>
					</div>
					<input type="hidden" id="question3" name="question3" value="3">
					<h3>Question </h3>
					<div class="alert alert-info" role="alert">Veuillez évaluer le sample 2</div>
					<!-- use the slider -->
					<div class="answer">
						<label>Avis : </label>
						<label id="rate4">3</label>
						<label> étoiles</label>
						<div id="slider4"></div>
						<label>Mauvais</label>
						<label style="float: right;">Excellent</label>
					</div>
					<input type="hidden" id="question4" name="question4" value="3">
					<input type="submit" class="btn btn-lg btn-success btn-block pull-right" value="Next">
				</form>
			</div>
		</div>
	</div>
	<br><br><br>
	<script>
		$( function() {
			$( "#slider3" ).slider({
				range: "min",
				value:3,
				min: 0,
				max: 6,
				step: 1,
				slide: function( event, ui ) {
					$( "#rate3" ).html(ui.value );
					$("#question3").attr("value",ui.value);
				}
			});
		} );
		$( function() {
			$( "#slider4" ).slider({
				range: "min",
				value:3,
				min: 0,
				max: 6,
				step: 1,
				slide: function( event, ui ) {
					$( "#rate4" ).html(ui.value );
					$("#question4").attr("value",ui.value);
				}
			});
		} );
	</script>


<!-- Bootstrap Core JavaScript -->
<!-- <script src="/js/bootstrap.min.js"></script> -->

	</body>

</html>