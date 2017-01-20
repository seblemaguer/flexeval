<!DOCTYPE html>
<html lang="en">

<head>

	<meta charset="utf-8">

	<title>Perceptual test platform - IRISA/Expression</title>

	<!-- Bootstrap Core CSS -->
	<link href="{{APP_PREFIX}}/static/css/bootstrap.min.css" rel="stylesheet">
	<link href="{{APP_PREFIX}}/static/css/tests.css" rel="stylesheet">
	<link href="{{APP_PREFIX}}/static/css/jquery-ui.min.css" rel="stylesheet">
	<script src="{{APP_PREFIX}}/static/js/jquery.js"></script>
	<script src="{{APP_PREFIX}}/static/js/jquery-ui.min.js"></script>

	<style>
		.rate {
			width: 3em;
			height: 1.6em;
			top: 50%;
			font-weight: bold;
			margin-top: -.8em;
			text-align: center;
			line-height: 1.6em;
		}
		
		.vcenter {
			display: inline-block;
			vertical-align: middle;
			float: none;
		}
	</style>
	
</head>

<body>

	<nav class="navbar navbar-default" style="margin-bottom:0">
		<div class="container-fluid">
			<ul class="nav navbar-nav navbar-right">
				<li><a>{{user}}</a></li>
				<li><a href="{{APP_PREFIX}}/logout">Logout</a></li>
			</ul>
		</div>
	</nav>
	
	<form role="form" action="{{APP_PREFIX}}/test" method="POST">
	
		<div class="jumbotron text-center">
		<h2><b>Context:</b> Imagine someone tells the text below during a spontaneous conversation.</h2>
		<h2><b>Question:</b> How likely do you judge the spoken propositions?</h2>
		<br>
		<h4><i>Remark: Some propositions may be identical, some may differ only very slightly.</i></h4>
		</div>
		% if introduction :
		<div class="alert alert-danger"><strong>Warning!</strong> This is an introduction step!</div>
		% end 
		<input type="hidden" name="ref" value="{{index}}">
		<input type="hidden" name="system1" value="{{systems[0]}}">
		<div class="container">
			<h1 class="text-center">Text {{step}}/{{totalstep}}</h1>
		</div>
		<div class="container">
			<div class="col-md-4 col-md-offset-4">
			<div class="progress" style="height: 2px">
				<div class="progress-bar" role="progressbar" aria-valuenow="{{progress}}" aria-valuemin="0" aria-valuemax="100" style="width:{{progress}}%">
				</div>
			</div>
			</div>
		</div>
		<div class="container">
			<center>
				<samp class="lead text-center">
					{{!samples[0]['text']}}
				</samp>
				<audio id="player" controls>
					<source src="{{samples[0]["path"]}}">
				</audio>
			</center>
		</div>


		<br>
		
		% for i in range(nfixed,len(systems)):
		
		<input type="hidden" name="system{{i+1}}" value="{{systems[i]}}">

		<div class="container">
		
			<h2>Proposition {{i}}</h2>
			
			<div class="row">
				<div class="col-xs-12 col-md-7 col-lg-7 vcenter">
					<blockquote>
					<samp class="text-justify">
						{{!samples[i]['text']}}
					</samp>
					</blockquote>
				</div>
				<div class="col-xs-12 col-md-4 col-lg-4 vcenter">
					<div class="answer">
						<div id="slider{{i}}">
							<div id="rate{{i}}" class="ui-slider-handle">5</div>
						</div>
						<label style="color: red; margin-top:5px; margin-bottom:5px;">0: impossible</label>
						<label style="color: green; margin-top:5px; margin-bottom:5px; float: right;">10: perfectly possible</label>
					</div>
					<input type="hidden" id="question{{i}}" name="question{{i}}" value="5;;{{systems[i]}}">
				</div>
				<div class="col-xs-12 col-md-7 col-lg-7 vcenter">
					<blockquote>
					<audio id="player" controls>
						<source src="{{samples[i]["path"]}}">
					</audio>
					</blockquote>
				</div>
				<div class="col-xs-12 col-md-7 col-lg-7 vcenter">
					<blockquote>
					<img src="{{samples[i]["image"]}}" alt="Mountain View" style="width:304px;height:228px;">
					</blockquote>
				</div>
				<div class="col-xs-12 col-md-7 col-lg-7 vcenter">
					<blockquote>
					 <video width="500" height="345" src="{{samples[i]["video"]}}" controls/>
					</blockquote>
				</div>
			</div>
				
		</div>
		
		<style>
			#rate{{i}} {
				width: 3em;
				height: 1.6em;
				top: 50%;
				font-weight: bold;
				margin-top: -.8em;
				text-align: center;
				line-height: 1.6em;
			}
		</style>
		
		<script>
			$(function() {
				$("#slider{{i}}").slider({
					range: "min",
					value:5,
					min: 0,
					max: 10,
					step: 1,
					slide: function(event, ui) {
						$("#rate{{i}}").html(ui.value);
						$("#question{{i}}").attr("value",ui.value+";;{{systems[i]}}");
					}
				});
			});
		</script>
		
		% end

		
		
	<div class="container">
		<div class="row">
			<!-- answer part -->
			<div class="col-md-6 col-md-offset-3">
					<input id="next" type="submit" class="btn btn-lg btn-success btn-block pull-right" value="Next" style="margin-top: 20px;">
			</div>
		</div>
	</div>
	
	</form>

	<br><br><br>

</body>

</html>
