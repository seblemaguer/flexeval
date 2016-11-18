<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="utf-8">
	<title>Subjective tests plateform - test</title>
	<!-- Bootstrap Core CSS -->
	<link href="/static/css/bootstrap.min.css" rel="stylesheet">
	<link href="/static/css/tests.css" rel="stylesheet">
	<script src="/static/js/jquery.js"></script>
	<script src="/static/js/jquery-ui.min.js"></script>
</head>

<body>
	<div class="jumbotron">
		<div class="container">
			<div class="col-md-6 col-md-offset-3">
				<h1>Test {{test_code}}</h1><h3>Fait par {{author}}</h3>
				<p class="lead">{{description}}</p>
				% for i in range(len(samples)):
				<p>Echantillon {{i+1}}</p>
				<audio id="player" controls>
					<source src="{{samples[i]}}">
				</audio>
				% end
			</div>
		</div>
	</div>
	<div class="container">