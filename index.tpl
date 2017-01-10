<!DOCTYPE html>
<html lang="en">

<head>

	<meta charset="utf-8">

	<title>Subjective tests platform - {{name}}</title>

	<!-- Bootstrap Core CSS -->
	<link href="{{APP_PREFIX}}/static/css/bootstrap.min.css" rel="stylesheet">
	<link href="{{APP_PREFIX}}/static/css/tests.css" rel="stylesheet">
	<link href="{{APP_PREFIX}}/static/css/jquery-ui.min.css" rel="stylesheet">
	<script src="{{APP_PREFIX}}/static/js/jquery.js"></script>
	<script src="{{APP_PREFIX}}/static/js/jquery-ui.min.js"></script>

</head>

<body>

	<div class="container">
		<div class="row">
			<div class="col-md-4 col-md-offset-4 text-center">
			<h1>{{name}}</h1><span>
			<p class="lead">{{description}}</p>
			</div>
		</div>
	</div>
	</div>

	<div class="jumbotron">
		<div class="container">
			<div class="row">
				<div class="col-md-4 col-md-offset-4">
						<h3>Please provide an e-mail address to identify yourself:</h3>
						<form role="form" action="{{APP_PREFIX}}/login" method="POST">
							<fieldset>
								<div class="form-group">
									<input type="email" class="form-control" placeholder="E-mail" name="email" autofocus>
								</div>
								<!-- Change this to a button or input when using this as a form -->
								<input type="submit" class="btn btn-lg btn-success btn-block" value="Start/Continue">
							</fieldset>
						</form>
						<br>
					</div>
				</div>
			</div>
		</div>
	</div>
	
	<div class="container">
		<div class="row">
			<div class="col-md-4 col-md-offset-2">
				<img src="{{APP_PREFIX}}/static/img/logo_irisa.png" class="img-responsive center-block" alt="IRISA lab">
			</div>
			<div class="col-md-4">
				<img src="{{APP_PREFIX}}/static/img/logo_expression.png" class="img-responsive center-block" alt="Expression team">
			</div>
		</div>
	</div>

	</body>

</html>