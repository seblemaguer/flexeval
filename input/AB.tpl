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
	<script src="{{APP_PREFIX}}/static/js/bootstrap.js"></script>

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


	% if step > 0:
	<script>
	$(document).ready(function () {
		$('#realStartModal').modal('show');
	});
	</script>
	
	<!-- Modal -->
	<div class="modal fade" id="realStartModal" tabindex="-1" role="dialog" aria-labelledby="realStartModalLabel">
	<div class="modal-dialog" role="document">
		<div class="modal-content">
		<div class="modal-body">
			<h3><span class="alert-info text-center">This is now the <strong>real</strong> test, not an introduction step.</span></h3>
		</div>
		<div class="modal-footer">
			<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
		</div>
		</div>
	</div>
	</div>
	%end

	% if introduction:
	<nav class="navbar navbar-warning">
		<div class="container-fluid bg-warning">
			<div class="row">
				<div class="col-md-offset-2 col-md-8 vcenter text-center">
					<h3><span class="alert-warning text-center"><strong>Warning!</strong> This is an introduction step!</span></h3>
	% else:
	<nav class="navbar navbar-default">
		<div class="container-fluid">
			<div class="row">
				<div class="col-md-offset-2 col-md-8 vcenter text-center">
					<h3></h3>
	% end
					<br>
				</div>
				<div class="col-md-1 vcenter">
					<a class="label label-danger" href="{{APP_PREFIX}}/logout">&#10060; Logout ({{user}})</a>
				</div>
			</div>
		</div>
	</nav>
	
	<form role="form" action="{{APP_PREFIX}}/test2" method="POST">
	
		{{!hidden_fields}}
		
		<div class="container">
			<h1 class="text-center">Étape {{step}}/{{totalstep}}</h1>
		</div>
		<div class="container">
			<div class="col-md-4 col-md-offset-4">
				<div class="progress" style="height: 2px">
					<div class="progress-bar" role="progressbar" aria-valuenow="{{progress}}" aria-valuemin="0" aria-valuemax="100" style="width:{{progress}}%">
					</div>
				</div>
			</div>
		</div>
		
		<br>

		<div class="jumbotron text-center">
			<h2></h2>
			<h2><b>Question :</b> Entre A et B, quel échantillon est de <strong>meilleure qualité</strong> ?</h2>
			<br>
		</div>
		
		<br>
		<div class="answer container">
			<div id="radio">
			<table class="table table-compact table-hover">
			<thead>
				<tr>
				<th></td>
				<th></td>
				<th class="text-center">Préférence</td>
				</tr>
			</thead>
				% for i in range(nfixed,len(systems)):
				
				<tr>
					<td class="text-right">
						<h3>Échantillon {{str(unichr(65+i))}}</h3>
					</td>
					<td class="text-center">
						<h3><audio id="player" controls>
							<source src="{{!samples[i]["speech"]}}">
						</audio></h3>
					</td>
					<td class="text-center">
						<h3><input type=radio name="question1" value="{{i+1}}"><label for="{{i+1}}"></label></h3>
					</td>
				</tr>
				
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
								$("#question{{i}}").attr("value",ui.value);
							}
						});
					});
				</script>
				
				<input type="hidden" name="system{{i+1}}" value="{{systems[i]}}">
				
				%end
				<tr>
					<td class="text-right">
					<h3>Aucune préférence</h3>
					</td>
					<td class="text-center">
					</td>
					<td class="text-center">
						<h3><input type=radio name="question1" value="None"><label for="None"></label></h3>
					</td>
				</tr>

			</table>
			</div>
		</div>
		
		<br>
		
		<input type="hidden" name="ref" value="{{index}}">

		<div class="container">			
			<div class="row">
				<div class="col-xs-12 col-md-6 col-lg-6 vcenter">
					
							% for i in range(nfixed,len(systems)):
							
							%end
							
						
				</div>
			</div>
				
		</div>
		
		
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
