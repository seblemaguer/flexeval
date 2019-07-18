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


</head>

<body>
		

<!-- barre de navigation -->

	% if introduction:
	<nav class="navbar navbar-warning">
		<div class="container-fluid bg-warning">
			<div class="row">
				<div class="col-sm-offset-1 col-sm-8 col-md-offset-2 col-md-8 vcenter text-center">
					<h3><span class="alert-warning vcenter text-center" style="vertical-align: super;">This is an introduction step.</span></h3>
	% else:
	<nav class="navbar navbar-default">
		<div class="container-fluid">
			<div class="row">
				<div class="col-sm-offset-1 col-sm-8 col-md-offset-2 col-md-8 vcenter text-center">
					<h3><span class="text-center">&nbsp;</span></h3>
	% end
				</div>
				<div class="col-sm-2 col-md-1 vcenter">
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


			
			<a onclick="instructionsToggle()" class="btn btn-primary" id="instructionsToggleBtn">Instructions</a>

<!-- le /div d'apres est en trop sans doute !!!  -->
<!--		</div> -->
		
		<script>
			var idBtn = document.getElementById("instructionsToggleBtn");
			var idJumbo = document.getElementById("instructions");

			function show() {}
			function hide() {}
<!--			function toggle() {}  -->
			function instructionsToggle() {
				var idBtn = document.getElementById("instructionsToggleBtn");
				var idJumbo = document.getElementById("instructions");
				if (idJumbo.style.display === "none") {
					idJumbo.style.display = "block";
					idBtn.innerHTML = "less Instructions";
				} else {
					idJumbo.style.display = "none";
					idBtn.innerHTML = "Instructions";
				}
			}
	
		</script>

		<br>

		<div id="CarouselTest" class="carousel slide" data-interval="false" data-ride="carousel">
 

		<div class="carousel-inner">

		 	<div class="carousel-item active">
			<p>
<h2> Nom d'Animaux en Signes </2>
				<h4>Dans cette première partie, vous allez voir 18 vidéos avec des personnages virtuels signant des noms d'animaux. <br>

				Il vous sera demandé de répondre à trois questions sur chaque vidéo. 
<br>
				Ces personnages peuvent prendre trois apparences différentes. 
<br>
				Et maintenant un petit entraînement pour que vous visualisiez le type de vidéo qui vous sera présentées. Les réponses correspondant à cet entraînement ne compteront pas. 
<br>
				</h4>
			</p>
  			<a   href="#CarouselTest"  class="btn btn-lg btn-success   col-3"  >Suiv  </a>

			</div>


		 	

		</div>
		</div>
		<div class="answer container">




			<div>
			<table class="table table-compact table-hover">
<!-- 			Table header -->
				<thead>
					<tr>
					<th class="text-center"><h4><strong>   			 </strong></h4></th>
					% for i in range(nfixed,len(systems)):
					

					<th class="text-center"><h4><strong>  Apparence N° {{ step }}    </strong></h4></th>
					% end
					</tr>
					
					<tr>
					<th class="text-center"><h4><strong>Questions</strong></h4></td>  
					<!-- Sample i -->

					% for i in range(nfixed,len(systems)):
					<td class="text-center">

							<video width="480" height="360" controls >
							  <source src="{{!samples[i]["video"]}}" type="video/mp4">

							Your browser does not support the video tag.
							</video> 

					</td>
					% end

					</tr>
				</thead>


				
				% iQ = 1


<!--				% for q in range(0,int(config["nbQuestionsPerStep"]) ):  -->
				% q = 0
				<!-- Question 1 -->
				
				<tr bgcolor={{config['questionBgColor'][q]}}>
					
				<td class="text-center">

					<h4>
						<strong>
							<a class="test"  id="tooltip_q" data-toggle="tooltip" data-placement="right" title="{{config['instructionsDetail'][q]}}">
								<font color={{config['explanationTextColor'][q]}}>{{config['questionTitle'][q]}}</font> 
							</a>
						</strong>
					</h4>

					<h4><br>{{config['questionDetail'][q]}} </h4>
<!-- question vidéo -->
<!--					<video width="320" height="240" controls >
					<source src="{{config['questionVideo'][q]}}" type="video/mp4">

					Your browser does not support the video tag.
					</video>
--> 
<!-- question vidéo -->					
				</td>
				

				
				% for i in range(nfixed,len(systems)):
				<!-- Question 1 -->
					<td class="text-center">
						<h5>
							<div class="answer" style="padding-left:20px; padding-right:20px;">
								<!-- 
								<div id="slider{{iQ}}">
								<div id="rate{{iQ}}" class="ui-slider-handle">0</div>  
								<div id="rate{{iQ}}" class="ui-slider-handle">3</div>  
								</div>
								-->
								<select id="selectTruc" name="answer_{{iQ}}" class="custom-select">
								    <option selected>Choisir le nom de l'animal correspondant dans la liste</option>
								    <option value="chat">chat</option>
								    <option value="chien">chien</option>
								    <option value="lapin">lapin</option>
								  </select>

							</div>
  	

							<script>

								 $("#selectTruc").on('change', () =>
								{
									$("#selectTruc").attr("disabled","");
									$("#tq2").css("visibility","visible");
									$("#tq3").css("visibility","visible");
								});	

							</script>


<!--<input type="hidden" id ="answer_{{iQ}}" name="answer_{{iQ}}" value="3">-->
							<input type="hidden" id="question_index_{{iQ}}" name="question_index_{{iQ}}" value="{{q + 1}}">
							<input type="hidden" name="system_index_{{iQ}}" value="{{systems[i]}}">
						</h5>
					</td>
					
				<style>
					#rate{{iQ}} {
						width: 3em;
						height: 1.6em;
						top: 50%;
						font-weight: bold;
						margin-top: -.8em;
						text-align: center;
						line-height: 1.6em;
						border-color: {{config['explanationTextColor'][q]}};
						color: {{config['explanationTextColor'][q]}};
					}
				</style>
				
				<style>
				/* Tooltip */
				.test + .tooltip > .tooltip-inner {
					background-color: {{config['explanationTextColor'][q]}}; 
					color: #FFFFFF; 
					border: 1px solid green; 
					padding: 15px;
					font-size: 20px;
				}

				/* Tooltip on right */
				.test + .tooltip.right > .tooltip-arrow {
				border-right: 5px solid black;
				}
				</style>
				
				<script>
					$(document).ready(function(){
						$('[data-toggle="tooltip"]').tooltip();   
					});
				</script>

				<script>
					$(function() {
						$("#slider{{iQ}}").slider({
							range: "min",
							value:3,
							
							min: 1, 
							max: 5, 

							step: 1,
							slide: function(event, ui) {
								$("#rate{{iQ}}").html(ui.value);
								$("#answer_{{iQ}}").attr("value",ui.value);
								
							}
						});
					});
				</script>
				% iQ = iQ + 1
				% end
				</tr>
<!--				%end   -->
					% q = q + 1
					<!-- Question 2 -->

					<tr id="tq2" style="visibility:hidden" bgcolor={{config['questionBgColor'][q]}}>
					
					<td class="text-center" >
						<h4>
							<strong>
								<a class="test"  id="tooltip_q" data-toggle="tooltip" data-placement="right" title="{{config['instructionsDetail'][q]}}">
									<font color={{config['explanationTextColor'][q]}}>{{config['questionTitle'][q]}}</font> 
								</a>
							</strong>
						</h4>
						<h4><br>{{config['questionDetail'][q][0]}} "{{!samples[i]["text"]}}" <br> {{config['questionDetail'][q][1]}}</h4>

						

	<!-- question vidéo -->
	<!--					<video width="320" height="240" controls >
						<source src="{{config['questionVideo'][q]}}" type="video/mp4">

						Your browser does not support the video tag.
						</video> 
	-->
	<!-- question vidéo -->					
					</td>
				

				
					% for i in range(nfixed,len(systems)):
					<!-- Question q -->
						<td class="text-center">
							<h5>
								<div class="answer" style="padding-left:20px; padding-right:20px;">
									<!-- 
									<div id="slider{{iQ}}">
	 								<div id="rate{{iQ}}" class="ui-slider-handle">0</div>
									<div id="rate{{iQ}}" class="ui-slider-handle">3</div>  
									</div>
									-->

									<div>
									  <input type="radio" id="1" name="answer_{{iQ}}" value="1">
									  <label for="1">1</label>
									</div>

									<div>
									  <input type="radio" id="2" name="answer_{{iQ}}" value="2">
									  <label for="2">2</label>
									</div>

									<div>
									  <input type="radio" id="3" name="answer_{{iQ}}" value="3">
									  <label for="3">3</label>
									</div>

									<div>
									  <input type="radio" id="4" name="answer_{{iQ}}" value="4">
									  <label for="4">4</label>
									</div>

									<div>
									  <input type="radio" id="5" name="answer_{{iQ}}" value="5">
									  <label for="5">5</label>
									</div>


								</div>

								<!--<input type="hidden" id ="answer_{{iQ}}" name="answer_{{iQ}}" value="3">-->
								<input type="hidden" id="question_index_{{iQ}}" name="question_index_{{iQ}}" value="{{q + 1}}">
								<input type="hidden" name="system_index_{{iQ}}" value="{{systems[i]}}">
							</h5>
						</td>
					
					<style>
						#rate{{iQ}} {
							width: 3em;
							height: 1.6em;
							top: 50%;
							font-weight: bold;
							margin-top: -.8em;
							text-align: center;
							line-height: 1.6em;
							border-color: {{config['explanationTextColor'][q]}};
							color: {{config['explanationTextColor'][q]}};
						}
					</style>
				
					<style>
					/* Tooltip */
					.test + .tooltip > .tooltip-inner {
						background-color: {{config['explanationTextColor'][q]}}; 
						color: #FFFFFF; 
						border: 1px solid green; 
						padding: 15px;
						font-size: 20px;
					}

					/* Tooltip on right */
					.test + .tooltip.right > .tooltip-arrow {
					border-right: 5px solid black;
					}
					</style>
				
					<script>
						$(document).ready(function(){
							$('[data-toggle="tooltip"]').tooltip();   
						});
					</script>

					<script>
						$(function() {
							$("#slider{{iQ}}").slider({
								range: "min",
								value:3,
							
								min: 1, 
								max: 5, 

								step: 1,
								slide: function(event, ui) {
									$("#rate{{iQ}}").html(ui.value);
									$("#answer_{{iQ}}").attr("value",ui.value);
								
								}
							});
						});
					</script>
					% iQ = iQ + 1
					% end
					</tr>

					% q = q + 1
					<!-- Question 3 -->
				
					<tr id="tq3" style="visibility:hidden" bgcolor={{config['questionBgColor'][q]}}>
					
					<td class="text-center">
						<h4>
							<strong>
								<a class="test"  id="tooltip_q" data-toggle="tooltip" data-placement="right" title="{{config['instructionsDetail'][q]}}">
									<font color={{config['explanationTextColor'][q]}}>{{config['questionTitle'][q]}}</font> 
								</a>
							</strong>
						</h4>
						<h4><br>{{config['questionDetail'][q]}} </h4>
	<!-- question vidéo -->
	<!--					<video width="320" height="240" controls >
						<source src="{{config['questionVideo'][q]}}" type="video/mp4">

						Your browser does not support the video tag.
						</video> 
	-->
	<!-- question vidéo -->					
					</td>
				

				
					% for i in range(nfixed,len(systems)):
					<!-- Question q -->
						<td class="text-center">
							<h5>
								<div class="answer" style="padding-left:20px; padding-right:20px;">
									<!--  
									<div id="slider{{iQ}}">
	 								<div id="rate{{iQ}}" class="ui-slider-handle">0</div>  
									<div id="rate{{iQ}}" class="ui-slider-handle">3</div>  
									</div>
									-->

									<div>
									  <input type="radio" id="1" name="answer_{{iQ}}" value="1">
									  <label for="1">1</label>
									</div>

									<div>
									  <input type="radio" id="2" name="answer_{{iQ}}" value="2">
									  <label for="2">2</label>
									</div>

									<div>
									  <input type="radio" id="3" name="answer_{{iQ}}" value="3">
									  <label for="3">3</label>
									</div>

									<div>
									  <input type="radio" id="4" name="answer_{{iQ}}" value="4">
									  <label for="4">4</label>
									</div>

									<div>
									  <input type="radio" id="5" name="answer_{{iQ}}" value="5">
									  <label for="5">5</label>
									</div>



	<!--						
								<label style=" margin-top:5px; margin-bottom:5px; float: left;">very prepared</label>
								<label style=" margin-top:5px; margin-bottom:5px; float: right;">very spontaneous</label>
	-->

								</div>

								<!--<input type="hidden" id ="answer_{{iQ}}" name="answer_{{iQ}}" value="3"> -->
								<input type="hidden" id="question_index_{{iQ}}" name="question_index_{{iQ}}" value="{{q + 1}}">
								<input type="hidden" name="system_index_{{iQ}}" value="{{systems[i]}}">
							</h5>
						</td>
					
					<style>
						#rate{{iQ}} {
							width: 3em;
							height: 1.6em;
							top: 50%;
							font-weight: bold;
							margin-top: -.8em;
							text-align: center;
							line-height: 1.6em;
							border-color: {{config['explanationTextColor'][q]}};
							color: {{config['explanationTextColor'][q]}};
						}
					</style>
				
					<style>
					/* Tooltip */
					.test + .tooltip > .tooltip-inner {
						background-color: {{config['explanationTextColor'][q]}}; 
						color: #FFFFFF; 
						border: 1px solid green; 
						padding: 15px;
						font-size: 20px;
					}

					/* Tooltip on right */
					.test + .tooltip.right > .tooltip-arrow {
					border-right: 5px solid black;
					}
					</style>
				
					<script>
						$(document).ready(function(){
							$('[data-toggle="tooltip"]').tooltip();   
						});
					</script>

					<script>
						$(function() {
							$("#slider{{iQ}}").slider({
								range: "min",
								value:3,
							
								min: 1, 
								max: 5, 

								step: 1,
								slide: function(event, ui) {
									$("#rate{{iQ}}").html(ui.value);
									$("#answer_{{iQ}}").attr("value",ui.value);
								
								}
							});
						});
					</script>
					% iQ = iQ + 1
					% end

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
				<div class="col-sm-6 col-sm-offset-3 col-md-6 col-md-offset-3">
<!-- 					Submit button -->
					<input id="next" type="submit" class="btn btn-lg btn-success btn-block pull-right" value="Next" style="margin-top: 20px;" disabled>

<!-- 					Auto-enabling -->
					<script>

					$("#next").on("click", () => {	
						$("#selectTruc").removeAttr("disabled"); 
					});


					jQuery('body').on('pause', 'video', function(e) {
						if ((all_played('video'))
						&&
						   ($('input[type=radio][name=answer_2]:checked').length == 1 )
						&&
						   ($('input[type=radio][name=answer_3]:checked').length == 1 )
						)
						{						 
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
	
		<script type="text/javascript">
		$(document).ready(function(){
			document.getElementById("instructions").style.display="block";
			document.getElementById("instructionsToggleBtn").innerHTML = "less Instructions";
		});
		</script>

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
</footer>

</html>

