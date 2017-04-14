<!DOCTYPE html>
<html lang="en">

<head>

	<meta charset="utf-8">

	<title>Perceptual test platform - IRISA/Expression</title>

	<!-- Bootstrap Core CSS -->
	<link href="{{APP_PREFIX}}/static/css/bootstrap.min.css" rel="stylesheet">
	<link href="{{APP_PREFIX}}/static/css/jquery-ui.min.css" rel="stylesheet">
	<link href="{{APP_PREFIX}}/static/css/perceval.css" rel="stylesheet">
	<script src="{{APP_PREFIX}}/static/js/jquery.js"></script>
	<script src="{{APP_PREFIX}}/static/js/jquery-ui.min.js"></script>
	<script src="{{APP_PREFIX}}/static/js/bootstrap.js"></script>
	<script src="{{APP_PREFIX}}/static/js/perceval.js"></script>

	<style>

		
	</style>
	
</head>

<body>

	% if introduction:
	<nav class="navbar navbar-warning">
		<div class="container-fluid bg-warning">
			<div class="row">
				<div class="col-md-offset-2 col-md-8 vcenter text-center">
					<h3><span class="alert-warning vcenter text-center" style="vertical-align: super;">This is an introduction step.</span></h3>
	% else:
	<nav class="navbar navbar-default">
		<div class="container-fluid">
			<div class="row">
				<div class="col-md-offset-2 col-md-8 vcenter text-center">
					<h3><span class="text-center">&nbsp;</span></h3>
	% end
				</div>
				<div class="col-md-1 vcenter">
					<a class="label label-danger" href="{{APP_PREFIX}}/logout">&#10060; Logout ({{user}})</a>
				</div>
			</div>
		</div>
	</nav>
	
	<form role="form" action="{{APP_PREFIX}}/answer" method="POST">
	
		{{!hidden_fields}}
		
		<div class="container">
			<h1 class="text-center">Step {{step}}/{{totalstep}}</h1>
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

		% q = 1
		
		<div class="jumbotron text-center">
			<h2></h2>
			<h2><b>Question :</b> Between 1 and 5, how do you judge the <strong>quality</strong> of the following samples?</h2>
			<br>
		</div>
		
		<br>
		
		<div class="answer container">
			<div>
			<table class="table table-compact table-hover">
<!-- 			Table header -->
				<thead>
					<tr>
					<th class="text-center"><h4><strong>Sample</strong></h4></td>
					<th class="text-center"><h4><strong>Rate</strong></h4></td>
					</tr>
				</thead>
			
				% for i in range(nfixed,len(systems)):
				
<!-- 			Sample i -->
				<tr>
					<td class="text-center">
						<h3><audio id="player" controls>
							<source src="{{!samples[i]["speech"]}}">
						</audio></h3>
					</td>
					<td class="text-center">
						<h4>
							<div class="answer">
								<div id="slider{{q}}">
									<div id="rate{{q}}" class="ui-slider-handle">3</div>
								</div>
								<label style="color: red; margin-top:5px; margin-bottom:5px; float: left;">1: Bad</label>
								<label style="color: green; margin-top:5px; margin-bottom:5px; float: right;">5: Excellent</label>
							</div>
							<input type="hidden" id="question{{q}}" name="question{{q}}" value="3">
							<input type="hidden" id="target_question{{q}}" name="target_question{{q}}" value="{{systems[i]}}">
							<input type="hidden" name="system{{i+1}}" value="{{systems[i]}}">
						</h4>
					</td>
				</tr>
				
				
				
				<style>
					#rate{{q}} {
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
						$("#slider{{q}}").slider({
							range: "min",
							value:3,
							min: 1,
							max: 5,
							step: 1,
							slide: function(event, ui) {
								$("#rate{{q}}").html(ui.value);
								$("#question{{q}}").attr("value",ui.value);
							}
						});
					});
				</script>

				%end

			</table>
			</div>
		</div>
		
		<script type="text/javascript">
		$(document).ready(function(){
			$('input[type="radio"]').click(highlight_selected_choice);
		});
		</script>
		
		<br>
		
		<input type="hidden" name="ref" value="{{index}}">

		
		<br>
		<div class="container">
			<div class="row">
				<div class="col-md-6 col-md-offset-3">
<!-- 					Submit button -->
					<input id="next" type="submit" class="btn btn-lg btn-success btn-block pull-right disabled" value="Next" style="margin-top: 20px;">
					
<!-- 					Auto-enabling -->
					<script>
					jQuery('body').on('pause', 'audio', function(e) {
						if (all_played('audio')) {
							$('input[type="submit"]').removeClass("disabled");
						}
					});
					</script>
				</div>
			</div>
		</div>
	
	</form>

	<br><br><br>

	
	
<!-- ============= Modals ============= -->


% if step == 1:

	%if introduction:
	<!-- Introduction modal -->
	<div class="modal fade" id="introductionModal" tabindex="-1" role="dialog" aria-labelledby="introductionModalLabel">
		<div class="modal-dialog" role="document">
			<div class="modal-content" style="background-color: #fcf8e3;">
				<div class="modal-body text-center">
					<h3><span class="alert-warning">This is the <strong>introduction</strong>.</span></h3>
					<h3><span class="alert-warning">Your answers will <strong>not</strong> be recorded for now.</span></h3>
					<br>
					<button type="button" class="btn btn-lg btn-warning" data-dismiss="modal">OK</button>
				</div>
			</div>
		</div>
	</div>

	<script>
	$(document).ready(function () {
		$('#introductionModal').modal('show');
	});
	</script>

	%else:

	<!-- Real start modal -->
	<div class="modal fade" id="realStartModal" tabindex="-1" role="dialog" aria-labelledby="realStartModalLabel">
		<div class="modal-dialog" role="document">
			<div class="modal-content" style="background-color: #d9edf7;">
				<div class="modal-body text-center">
					<h3><span class="alert-info text-center">This is now the <strong>real</strong> test, not an introduction step.</span></h3>
					<br>
					<button type="button" class="btn btn-lg btn-primary" data-dismiss="modal">Let's go!</button>
				</div>
			</div>
		</div>
	</div>

	<script>
	$(document).ready(function () {
		$('#realStartModal').modal('show');
	});
	</script>

	%end

%end

</body>

<footer class="footer">
	<div class="container" style="padding: 0px;">
		<div class="row">
			<div class="col-md-offset-3 col-md-3">
				<img src="{{APP_PREFIX}}/static/img/logo_irisa.png" class="img-responsive center-block" alt="IRISA lab" width="50%" height="50%">
			</div>
			<div class="col-md-3">
				<img src="{{APP_PREFIX}}/static/img/logo_expression.png" class="img-responsive center-block" alt="Expression team" width="67%" height="67%">
			</div>
		</div>
				<p class="text-muted" style="letter-spacing: 2px;">Powered by PercEval.</p>
	</div>
</footer>

</html>
