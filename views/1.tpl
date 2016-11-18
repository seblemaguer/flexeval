<!DOCTYPE html>
<html lang="en">

<head>

	<meta charset="utf-8">

	<title>Subjective tests plateform - test</title>

	<!-- Bootstrap Core CSS -->
	<link href="/static/css/bootstrap.min.css" rel="stylesheet">
	<link href="/static/css/tests.css" rel="stylesheet">

</head>

<body>

	<div class="jumbotron">
		<div class="container">
			<div class="col-md-6 col-md-offset-3">
				<h1>Test {{test_code}}</h1><span><h3>Made by gcoulomb (<small><a href="mailto:gcoulomb@enssat.fr" target="_top">gcoulomb@enssat.fr</a></small>)</h3>
				<p class="lead">Ceci est un test d'affichage !</p>
				% for i in range(len(samples)):
				<p>Sample {{i+1}}</p>
				<audio id="player" controls>
					<source src="{{samples[i]}}">
				</audio>
				% end
			</div>
		</div>
	</div>
	<div class="container">
		<div class="col-md-6 col-md-offset-3">
			<p>The question that follows here is just an example and not generated from any script!</p>
			<p>Your role as a test maker is to edit this part!</p>
			<form role="form" action="/test/{{test_code}}" method="POST">
				<input type="hidden" name="ref" value="{{index}}">
				<h3>Question 1</h3>
				<div class="alert alert-info" role="alert">Ceci est l'intitulé de ma question</div>
				<div class="col-md-offset-2">
					<div class="radio">
						<label>
							<input type="radio" id="radioA" name="question1" value="{{systems[0]}}"checked>
							Option A
						</label>
					</div>
					<div class="radio">
						<label>
							<input type="radio" id="radioB" name="question1" value="{{systems[1]}}">
							Option B
						</label>
					</div>
				</div>
				<h3>Question 2</h3>
				<div class="alert alert-info" role="alert">Une autre question ici</div>
				<div class="col-md-offset-2">
					<div class="radio">
						<label>
							<input type="radio" id="radioA" name="question2" value="{{systems[0]}}"checked>
							Option A
						</label>
					</div>
					<div class="radio">
						<label>
							<input type="radio" id="radioB" name="question2" value="{{systems[1]}}">
							Option B
						</label>
					</div>
				</div>
				<input type="submit" class="btn btn-lg btn-success btn-block pull-right" value="Next">
			</form>
		</div>
	</div>
	<br>
	<br>

</body>

</html>
