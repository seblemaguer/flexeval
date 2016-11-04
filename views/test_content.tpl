<!DOCTYPE html>
<html lang="en">

<head>

	<meta charset="utf-8">

	<title>Subjective tests plateform - test</title>

	<!-- Bootstrap Core CSS -->
	<link href="/css/bootstrap.min.css" rel="stylesheet">

</head>

<body>

	<div class="jumbotron">
		<div class="container">
			<div class="col-md-6 col-md-offset-3">
				<h1>Test {{code}}</h1><span><h3>Made by {{author}} (<small><a href="mailto:{{authormail}}" target="_top">{{authormail}}</a></small>)</h3>
				<p class="lead">{{description}}</p>
				<p>Sample A</p>
				<audio controls>
					<source src="{{url1}}">
					</audio>
				<p>Sample B</p>
				<audio controls>
					<source src="{{url2}}">
					</audio>
				</div>
				</div>
			</div>
			<div class="container">
				<div class="row">
					<!-- answer part -->
					<div class="col-md-6 col-md-offset-3">
						<form role="form" action="/test/{{code}}/{{step}}" method="POST">
		 
		% for question in questions :
		%	if question["type"] == "AB" :
							<h3>Question </h3>
							<div class="alert alert-info" role="alert">{{question["description"]}}</div>
							<div class="col-md-offset-2">
							<div class="radio">
								<label>
									<input type="radio" id="radioAB-A-{{question["id"]}}" name="radioAB-{{question["id"]}}" value="A"checked>
									Option A
								</label>
							</div>
							<div class="radio">
								<label>
									<input type="radio" id="radioAB-B-{{question["id"]}}" name="radioAB-{{question["id"]}}" value="B">
									Option B
								</label>
							</div>
							</div>
							
		% elif question["type"] == "MOS" : 
							<h3>Question </h3>
							<div class="alert alert-info" role="alert">{{question["description"]}}</div>
							<div class="col-md-offset-2">
							<div class="radio">
								<label>
									<input type="radio" id="radioMOS-A-{{question["id"]}}" name="radioMOS-{{question["id"]}}" value="A" checked>
									Option A
								</label>
							</div>
							<div class="radio">
								<label>
									<input type="radio" id="radioMOS-B-{{question["id"]}}" name="radioMOS-{{question["id"]}}" value="B" checked>
									Option B
								</label>
							</div>
							</div>
		% elif question["type"] == "ABX" : 
							<h3>Question </h3>
							<div class="alert alert-info" role="alert">{{question["description"]}}</div>
							<div class="col-md-offset-2">
							<div class="radio">
								<label>
									<input type="radio" id="radioABX-A-{{question["id"]}}" name="radioABX-{{question["id"]}}" value="A" checked>
									Option A
								</label>
							</div>
							<div class="radio">
								<label>
									<input type="radio" id="radioABX-B-{{question["id"]}}" name="radioABX-{{question["id"]}}" value="B">
									Option B
								</label>
							</div>
							<div class="radio">
								<label>
									<input type="radio" id="radioABX-X-{{question["id"]}}" name="radioABX-{{question["id"]}}" value="B">
									Option X
								</label>
							</div>
							</div>
		% elif question["type"] == "DMOS" : 
							<h3>Question </h3>
							<div class="alert alert-info" role="alert">{{question["description"]}}</div>
							<div class="col-md-offset-2">
							<div class="radio">
								<label>
									<input type="radio" id="radioDMOS-{{question["id"]}}" name="radioDMOS-{{question["id"]}}" value="A" checked>
									Option A
								</label>
							</div>
							<div class="radio">
								<label>
									<input type="radio" id="radioDMOS-{{question["id"]}}" name="radioDMOS-{{question["id"]}}" value="B">
									Option B
								</label>
							</div>
							<div class="radio">
								<label>
									<input type="radio" id="radioDMOS-{{question["id"]}}" name="radioDMOS-{{question["id"]}}" value="B">
									Option X
								</label>
							</div>	
							</div>						
							%	end
							% end
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
