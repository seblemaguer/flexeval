<!DOCTYPE html>
<html lang="en">

<head>

	<meta charset="utf-8">

	<title>Subjective tests plateform - test</title>

	<!-- Bootstrap Core CSS -->
	<link href="/static/css/bootstrap.min.css" rel="stylesheet">

</head>

<body>

	<div class="jumbotron">
		<div class="container">
			<div class="col-md-6 col-md-offset-3">
				<h1>Test {{test_code}}</h1><span><h3>Made by gcoulomb (<small><a href="mailto:gcoulomb@enssat.fr" target="_top">gcoulomb@enssat.fr</a></small>)</h3>
				<p class="lead">Ceci est un test d'affichage !</p>
				% for sample in samples:
				<p>Sample A</p>
				<audio controls>
					<source src="{{sample["path"]}}">
				</audio>
				% end
			</div>
		</div>
	</div>
	<div class="container">
		<div class="col-md-6 col-md-offset-3">
			<p>The question that follows here is just an example and not generated from any script!</p>
			<form role="form" action="/test/{{test_code}}" method="POST">
				<h3>Question </h3>
				<div class="alert alert-info" role="alert">Ceci est l'intitulé de ma question</div>
				<div class="col-md-offset-2">
					<div class="radio">
						<label>
							<input type="radio" id="radioA" name="radioAB" value="A"checked>
							Option A
						</label>
					</div>
					<div class="radio">
						<label>
							<input type="radio" id="radioB" name="radioAB" value="B">
							Option B
						</label>
					</div>
				</div>
				<input type="submit" class="btn btn-lg btn-success btn-block pull-right" value="Next">
			</form>
		</div>
	</div>

<!-- Bootstrap Core JavaScript -->
<!-- <script src="/js/bootstrap.min.js"></script> -->

</body>

</html>
