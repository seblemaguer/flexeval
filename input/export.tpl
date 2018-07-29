<!DOCTYPE html>
<html lang="en">

<head>

	<meta charset="utf-8">

	<title>Subjective tests platform - {{config["name"]}}</title>

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
				<div class="col-md-4 col-md-offset-4">
					<h3>Please provide the token given to you at the creation of the test</h3>
					<form role="form" action="{{APP_PREFIX}}/export" method="POST">
						<fieldset>
							<div class="form-group">
								<input type="text" class="form-control" placeholder="Token" name="token" autofocus required>
							</div>
							<!-- Change this to a button or input when using this as a form -->
							<input type="submit" value="DB" name="type" class="btn btn-lg btn-success btn-block" value="Export DB">
							<input type="submit" value="CSV" name="type" class="btn btn-lg btn-success btn-block" value="Export CSV">
						</fieldset>
					</form>
					<br>
					%if defined('error') and error != "" :
					<div class="alert alert-danger">
						<p><strong>Error !</strong>  {{error}}</p>
					</div>
					%end
				</div>
			</div>
		</div>
	</div>

	<div class="container" style="padding: 0px;">
		<div class="row">
			<div class="col-sm-offset-2 col-sm-4 col-md-offset-3 col-md-3">
				<a href="http://www.irisa.fr" target="_blank">
					<img src="{{APP_PREFIX}}/static/img/logo_irisa.png" class="img-responsive center-block" alt="IRISA lab" width="50%" height="50%">
				</a>
			</div>
			<div class="col-sm-4 col-md-3">
				<a href="http://www-expression.irisa.fr" target="_blank">
					<img src="{{APP_PREFIX}}/static/img/logo_expression.png" class="img-responsive center-block" alt="Expression team" width="67%" height="67%">
				</a>
			</div>
		</div>
		<p class="text-muted text-center" style="letter-spacing: 2px; line-height: 40px;"><a href="https://gitlab.inria.fr/dlolive/PercepEval" target="_blank">Powered by PercEval.</a></p>
	</div>

	</body>

</html>
