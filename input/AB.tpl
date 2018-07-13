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
			<h2><b>Question:</b> Between A and B, which sample do you prefer in terms of <strong>quality</strong>?</h2>
			<br>
		</div>
		
		<br>
		
		<div class="answer container">
			<div id="radio">
			<table class="table table-compact table-hover">
<!-- 			Table header -->
				<thead>
					<tr>
					<th></td>
					<th></td>
					<th class="text-center"><h4><strong>Preference</strong></h4></td>
					</tr>
				</thead>
			
				% for i in range(nfixed,len(systems)):
				
<!-- 			Sample i -->
				<tr class="answer_1" id="choice{{i+1}}">
					<td class="text-right">
						<h3>Échantillon {{str(unichr(65+i))}}</h3>
					</td>
					<td class="text-center">
						<h3><audio id="player" controls>
							<source src="{{!samples[i]["speech"]}}">
						</audio></h3>
					</td>
					<td class="text-center">
						<h3><input type=radio name="answer_1" value="{{i+1}}"><label for="{{i+1}}"></label></h3>
					</td>
				</tr>
				
				
				<input type="hidden" name="system_index_{{i+1}}" value="{{systems[i]}}">
				
				%end
				
<!-- 				No preference -->
				<tr class="answer_1" id="choiceNone">
					<td class="text-right">
					<h3>No preference</h3>
					</td>
					<td class="text-center">
					</td>
					<td class="text-center">
						<h3><input type=radio name="answer_1" value="None"><label for="None"></label></h3>
					</td>
				</tr>

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
					<input id="next" type="submit" class="btn btn-lg btn-success btn-block pull-right" value="Next" style="margin-top: 20px;" disabled>
					
<!-- 					Auto-enabling -->
					<script>
					jQuery('body').on('pause', 'audio', function(e) {
						if (all_played('audio')) {
							$('input[type="submit"]').prop("disabled", false);
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

<footer>
	<div class="container" style="padding: 0px;">
		<div class="row">
			<div class="col-md-offset-3 col-md-3">
				<a href="http://www.irisa.fr" target="_blank">
					<img src="{{APP_PREFIX}}/static/img/logo_irisa.png" class="img-responsive center-block" alt="IRISA lab" width="50%" height="50%">
				</a>
			</div>
			<div class="col-md-3">
				<a href="http://www-expression.irisa.fr" target="_blank">
					<img src="{{APP_PREFIX}}/static/img/logo_expression.png" class="img-responsive center-block" alt="Expression team" width="67%" height="67%">
				</a>
			</div>
		</div>
		<p class="text-muted text-center" style="letter-spacing: 2px; line-height: 40px;">Powered by PercEval.</p>
	</div>
</footer>

</html>
