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
				<h1>{{name}}</h1><span><h3>Made by {{author}}</h3>
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
					<div class="alert alert-info" role="alert">...</div>
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
					
					<h3>Question </h3>
					<div class="alert alert-info" role="alert">...</div>
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
					<div class="alert alert-success" role="alert">If you have any pertinent thing to say here please write it below!</div>	
					<div class="form-group">
						<textarea id="comments" rows="3" class="form-control" placeholder="Comments" style="resize:vertical"></textarea>
					</div>
					<input type="submit" class="btn btn-lg btn-success btn-block pull-right" value="Next">
				</form>
				<br/>
				<br/>
			</div>
		</div>
	</div>

<!-- Bootstrap Core JavaScript -->
<!-- <script src="/js/bootstrap.min.js"></script> -->

	</body>

</html>
