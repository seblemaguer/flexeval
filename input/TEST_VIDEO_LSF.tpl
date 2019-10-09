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

.dropdown {
/*  position: relative;*/
  display: inline-block;
}

.dropbtn {
  cursor: pointer;
  padding: 16px;
  font-size: 16px;

}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
/*  min-width: 160px; */
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
  
}

</style>

</head>

<body>
		

<!-- barre de navigation -->

	% if introduction:
	<nav class="navbar navbar-warning">
		<div class="container-fluid bg-warning">
			<div class="row">
				<div class="col-sm-offset-1 col-sm-8 col-md-offset-2 col-md-8 vcenter text-center">
					<h3><span class="alert-warning vcenter text-center" style="vertical-align: super;">Ceci est une étape d'introduction.</span></h3>
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
			<h1 class="text-center">Etape n°{{step}}/{{totalstep}}</h1>
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


<!-- suppression du bouton id="instructionsToggleBtn"	 		
			<a onclick="instructionsToggle()" class="btn btn-primary" id="instructionsToggleBtn">Instructions</a>
-->


<!-- suppression du script du bouton  id="instructionsToggleBtn"	 				
		<script>
			var idBtn = document.getElementById("instructionsToggleBtn");
			var idJumbo = document.getElementById("instructions");

			function show() {}
			function hide() {}
			function toggle() {} 
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
-->


<!-- le /div d'apres est en trop sans doute !!!  -->
<!--		</div> -->

		<br>
<!--	video explications partie 1
			<p>

				<video width="320" height="240" controls >
				<source src="{{config['questionTestVideo'][0]}}" type="video/mp4">
				Your browser does not support the video tag.
				</video>

 
			</p>
-->
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
							<!-- video de l'échantillon à qualifier à l'étape 'step' -->
							<video id="video_sample" width="480" height="360" controls >
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
				<video width="320" height="240" controls >
				<source src="{{config['questionTestVideo'][0]}}" type="video/mp4">
				Your browser does not support the video tag.
				</video>

					<h4>
						<strong>
<!--							<a class="test"  id="tooltip_q" data-toggle="tooltip" data-placement="right" title="{{config['instructionsDetail'][q]}}">
								<font color={{config['explanationTextColor'][q]}}>{{config['questionTitle'][q]}}</font> 
							</a>
-->
						<br><font color={{config['explanationTextColor'][q]}}>{{config['questionTitle'][q]}}</font>
						</strong>
					</h4>

<!--					<h4><br>{{config['questionDetail'][q]}} </h4>   -->
					<h4><br><font color={{config['explanationTextColor'][q]}}>{{config['questionDetail'][q]}}</font> 
</h4>

				
				</td>
				

				
				% for i in range(nfixed,len(systems)):
				<!-- Question 1 -->
					<td id="ancreq1" class="text-center">
						<h5>
							<div class="answer" style="padding-left:20px; padding-right:20px;">
								<!-- 
								<div id="slider{{iQ}}">
								<div id="rate{{iQ}}" class="ui-slider-handle">0</div>  
								<div id="rate{{iQ}}" class="ui-slider-handle">3</div>  
								</div>
								-->
								<p>
								<br> 
								<br>  
								<br> 	
								<br> 
								<br>  
								<br> 	
<!-- liste avec de noms d'animaux uniquement 
								<select id="selectAnimal" name="answer_{{iQ}}" class="custom-select">
								    <option selected>Choisir le nom de l'animal correspondant dans la liste</option>
								% for j in range(0,len(config["listeAnimaux"])):

								    <option value={{j}}>{{config['listeAnimaux'][j][0]}}</option>

								% end
								  </select>   
-->
							<div class="container">
							<div class="dropdown">
								<!--    <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">Dropdown Example  
    								<button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown" >Dropdown Example<span class="caret"></span></button>-->
    							<button id="selectAnimal" class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown" > 								<div id="valliste"></div><span class="caret"></span></button>

							<span id='Animal'></span>

    							<ul class="dropdown-menu" id="myDropdown" >

								% for j in range(0,len(config["listeAnimaux"])) :

								    <!-- <option value={{j}}>{{config['listeAnimaux'][j][0]}}</option>   -->
      								    <!--<li class="clickable" data="{{config['listeAnimaux'][j][0]}}"><img style="width: 18rem;" src="{{config['listeAnimaux'][j][1]}}" alt=" " title="{{config['listeAnimaux'][j][0]}}"/>  {{config['listeAnimaux'][j][0]}}</li>  -->
      									<li><a class="clickable" data="{{config['listeAnimaux'][j][0]}}" href="#" ><img style="width: 18rem;" src="{{config['listeAnimaux'][j][1]}}"  title="{{config['listeAnimaux'][j][0]}}" alt=" " />  {{config['listeAnimaux'][j][0]}}</a> </li>
								% end

<!--
      							<li class="clickable" data="Lion"><img style="width: 18rem;" src="/static/img/guepard.jpeg" alt=" " title="Lion"/>  Lion</a></li>
      							<li class="clickable" data="Chat" ><img style="width: 18rem;" src="/static/img/chat.jpeg" alt=" " title="Chat"/>  Chat</a></li>
      							<li class="clickable" data="Lapin" ><img style="width: 18rem;" src="/static/img/lapin.jpeg" alt=" " title="Lapin"/>  Lapin</a></li>
      							<li class="clickable" data="Renard" ><img style="width: 18rem;" src="/static/img/renard.jpeg" alt=" " title="Renard"/>  Renard</a></li>
      							<li class="clickable" data="Souris" ><img style="width: 18rem;" src="/static/img/souris.jpeg" alt=" " title="Souris"/>  Souris</a></li>
-->            
    							</ul>
  							</div>
								<br> 
								<br>  
								<br> 	
								<br> 
  								<input id="validAnimal" type="button" class="btn btn-success"  style="visibility:visible" value="Valider" disabled ></input>
								<br> 
							</div>	
								</p>

							</div>
  
<script type='text/javascript'>
$("#valliste").html("Choisir un animal dans la liste");
var ObjListe = document.getElementById('myDropdown');
var ObjAffiche = document.getElementById('Animal');
/*
$(".clickable").click((e)=>{$("#Animal").html(e.currentTarget.attributes.data.nodeValue);
$("#validAnimal").removeAttr("disabled");
$("#valliste").html("<img style='width: 18rem;' src='"+e.currentTarget.childNodes[0].src+"' />");
$("#answer_{{iQ}}").val(e.currentTarget.attributes.data.nodeValue);
//alert($("#answer_{{iQ}}").val());
});
*/

$(".clickable").click((e)=>{
	$("#Animal").html(e.currentTarget.attributes.data.nodeValue);
	$("#validAnimal").removeAttr("disabled");
	$("#valliste").html("<img style='width: 18rem;' alt='"+e.currentTarget.childNodes[0].title+"' src='"+e.currentTarget.childNodes[0].src+"' />");
	$("#answer_{{iQ}}").val(e.currentTarget.attributes.data.nodeValue);
	//alert($("#answer_{{iQ}}").val());
});


/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
/*function myFunction(e) {
	ObjAffiche.innerHTML = "       " +  e.currentTarget.attributes.data.nodeValue ;
} */
</script>

<!--							<script>

								 $("#selectAnimal").on('change', () =>
								{
									/*$("#selectAnimal").attr("disabled","");*/
									/*$("#tq2").css("visibility","visible");*/
									/*$("#tq3").css("visibility","visible");*/

									$("#validAnimal").removeAttr("disabled");
								});	

							</script>
-->
							<script>
								 $("#validAnimal").on("click", () =>
								{
									$("#selectAnimal").attr("disabled",""); 
									$("#tq2").css("visibility","visible");  
									$("#tq3").css("visibility","visible");    										$("#validAnimal").attr("disabled","");

								});	

							</script>



							<!--<input type="hidden" id ="answer_{{iQ}}" name="answer_{{iQ}}" value="3">-->
							<!-- on remplit le champ réponse de nom "value" de la question IQ avec le nom de l'animal choisi  -->

							<input type="hidden" id ="answer_{{iQ}}" name="answer_{{iQ}}" value="-1">

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

				<video width="320" height="240" controls >
				<source src="{{config['questionTestVideo'][1]}}" type="video/mp4">
				Your browser does not support the video tag.
				</video>
				

						<h4>
							<strong>
<!--								<a class="test"  id="tooltip_q" data-toggle="tooltip" data-placement="right" title="{{config['instructionsDetail'][q]}}">
									<font color={{config['explanationTextColor'][q]}}>{{config['questionTitle'][q]}}</font> 
								</a>
-->
						<br><font color={{config['explanationTextColor'][q]}}>{{config['questionTitle'][q]}}</font>

							</strong>
						</h4>
<!--						<h4><br>{{config['questionDetail'][q][0]}} "{{!samples[i]["text"]}}" <br> {{config['questionDetail'][q][1]}}</h4>   -->
					<h4><br><font color={{config['explanationTextColor'][q]}}>{{config['questionDetail'][q][0]}} "{{!samples[i]["text"]}}"</font> 
</h4>
					<h4><font color={{config['explanationTextColor'][q]}}>{{config['questionDetail'][q][1]}} </font> 
</h4>

					</td>
				

				
					% for i in range(nfixed,len(systems)):
					<!-- Question q -->
						<td class="text-center">
							<h5>
								<div class="answer" style="padding-left:20px; padding-right:20px;">
								<p>
								<br> 
								<br>  
								<br> 	
								<br> 
								<br>  
								<br> 	
								 
								<br> 
								<br>  
								<br> 	
								<br>
								<br> 
								<br>		
								</p>								
									<div id="slider{{iQ}}">
										<div id="rate{{iQ}}" class="ui-slider-handle">3</div>  
									</div>
									

<!--							<label style=" color: {{config['explanationTextColor'][q]}};margin-top:5px; margin-bottom:5px; float: left;">{{config['sliderMinValue']}}</label>
-->
							<label style=" color: {{config['explanationTextColor'][q]}};margin-top:5px; margin-bottom:5px; float: left;">non, pas du tout</label>
<!--							<label style=" color: {{config['explanationTextColor'][q]}};margin-top:5px; margin-bottom:5px; float: right;">{{config['sliderMaxValue']}}</label>
-->
							<label style=" color: {{config['explanationTextColor'][q]}};margin-top:5px; margin-bottom:5px; float: right;">Oui, tout à fait</label>

<!--
									<div>
									  <input type="radio" id="1" name="answer_{{iQ}}" value="1">
									  <label for="1">1</label>
									</div>

									<div>
									  <input type="radio" id="2" name="answer_{{iQ}}" value="2">
									  <label for="2">2</label>
									</div>

									<div>
									  <input type="radio" id="3" name="answer_{{iQ}}" value="3" checked>
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
-->

								</div>

								<input type="hidden" id ="answer_{{iQ}}" name="answer_{{iQ}}" value="3">
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

				<video width="320" height="240" controls >
				<source src="{{config['questionTestVideo'][2]}}" type="video/mp4">
				Your browser does not support the video tag.
				</video>
					

						<h4>
							<strong>
<!--
								<a class="test"  id="tooltip_q" data-toggle="tooltip" data-placement="right" title="{{config['instructionsDetail'][q]}}">
									<font color={{config['explanationTextColor'][q]}}>{{config['questionTitle'][q]}}</font> 
								</a>
-->
						<br><font color={{config['explanationTextColor'][q]}}>{{config['questionTitle'][q]}}</font>

							</strong>
						</h4>
						<!-- <h4><br>{{config['questionDetail'][q]}} </h4>  -->
						<h4><br><font color={{config['explanationTextColor'][q]}}>{{config['questionDetail'][q]}}</font> 
</h4>
					
					</td>
				

				
					% for i in range(nfixed,len(systems)):
					<!-- Question q -->
						<td class="text-center">
							<h5>
								<div class="answer" style="padding-left:20px; padding-right:20px;">
								<p>
								<br> 
								<br>  
								<br> 	
								<br> 
								<br>  
								<br> 	
								 
								<br> 
								<br>  
								<br> 	
								<br>
								<br> 
								<br>		
								</p>									  
									<div id="slider{{iQ}}">
<!--	 								<div id="rate{{iQ}}" class="ui-slider-handle">1</div>  -->
									<div id="rate{{iQ}}" class="ui-slider-handle">3</div>  
									</div>
									
<!--
									<div>
									  <input type="radio" id="1" name="answer_{{iQ}}" value="1">
									  <label for="1">1</label>
									</div>

									<div>
									  <input type="radio" id="2" name="answer_{{iQ}}" value="2">
									  <label for="2">2</label>
									</div>

									<div>
									  <input type="radio" id="3" name="answer_{{iQ}}" value="3" checked>
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

-->
							<label style=" color: {{config['explanationTextColor'][q]}};margin-top:5px; margin-bottom:5px; float: left;">non, pas du tout</label>
							<label style=" color: {{config['explanationTextColor'][q]}};margin-top:5px; margin-bottom:5px; float: right;">Oui, tout à fait</label>

	

								</div>

								<input type="hidden" id ="answer_{{iQ}}" name="answer_{{iQ}}" value="3"> 
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
					<input id="next" type="submit" class="btn btn-lg btn-success btn-block pull-right" value="Suivant" style="margin-top: 20px;" disabled>

<!-- 					Auto-enabling -->
					<script>

					$("#next").on("click", () => {	
						$("#selectAnimal").removeAttr("disabled"); 
					});


					jQuery('body').on('pause', 'video', function(e) {
//on  supprime le test de vérification suivant
//						if (all_played('video')  
//						) 
//on le remplace par le test de vérification de l'échantillon video 
						if (all_played('#video_sample')  
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
				<div class="modal-header">
        			<h3 class="modal-title text-center" id="partie1IntroModalLabel">Test LSF - Partie 1 <br> Nom d'Animaux en Signes</h3>
        			<button type="button" class="close" data-dismiss="modal" aria-label="Close">
          			<span aria-hidden="true">&times;</span>
        			</button>
      				</div>
				<div class="modal-body text-center">
					<h4><span class="alert-warning">Ceci est l'étape d'introduction.</span></h4> 
					<h4><span class="alert-warning">Les réponses correspondant à cet entraînement <strong>ne</strong> compteront <strong>pas</strong>.</span></h4><br>
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
				<div class="modal-header">
        			<h3 class="modal-title text-center" id="partie1ReelModalLabel">Test LSF - Partie 1 <br> Nom d'Animaux en Signes</h3>
        			<button type="button" class="close" data-dismiss="modal" aria-label="Close">
          			<span aria-hidden="true">&times;</span>
        			</button>
      				</div>

				<div class="modal-body text-center">
					<h4><span class="alert-info text-center">C'est maintenant le test <strong>réel</strong>, vos réponses vont être enregistrées.</span></h4>
					<br>
					<button type="button" class="btn btn-lg btn-primary" data-dismiss="modal">Allons y !</button>
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

