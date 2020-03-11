<!DOCTYPE html>
<html lang="en">

<head>

	<meta charset="utf-8">

	<title>Subjective tests platform - {{config["name"]}}</title>




  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
  <style>
  /* Make the image fully responsive */
  .carousel-inner img {
    width: 100%;
    height: 100%;
  }
  </style>


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
				<div class="col-1"></div>
				<div class="col-10">



	<form id="form_user" role="form" action="{{APP_PREFIX}}/login" method="POST">
    
		<div id="myCarousel" class="carousel slide" data-interval="false" data-ride="carousel">
	
	  	<!-- Indicators -->

  
	  	<!-- The slideshow -->


		<div class="carousel-inner">



		 	<div class="carousel-item active">

					<video width="320" height="240" controls >
					<source src="{{config['questionIdentificationVideo'][0]}}" type="video/mp4">

					Your browser does not support the video tag.
					</video>

	  		         <h3>Veuillez fournir une adresse e-mail pour vous identifier :</h3>

	 		             <fieldset>
	 		                 <div class="form-group">
	 		                     <input id="email" type="text" class="form-control input-lg" placeholder="E-mail" name="email">
	 		                 </div>
	 		                 <!-- Change this to a button or input when using this as a form -->

<!--  			<a  id="nextform0" href="#myCarousel"  class="btn btn-lg btn-success   col-3" disabled >Suiv  </a>  -->
	 		<br>
  			<a  id="nextform0" href="#myCarousel"  class="btn btn-lg btn-success   col-3" disabled >Démarrer/Continuer  </a>
		
	 		             </fieldset>

	 		         <br>
	 		         %if defined('error') and error != "" :
	 		         <div class="alert alert-danger">
	 		             <p><strong>Error !</strong>  {{error}}</p>
		  		</div>
		  		%end

      			</div>      

			<script>
			function isEmail(email) {
				  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
 				 return regex.test(email);
			}

			function submitevent(){ $("#form_user").trigger("submit"); }

			 $("#nextform0").on('mouseenter', () =>
			{

				if( isEmail($("#email").val()))
				{

					$.get( "{{APP_PREFIX}}/alreadyregister/email/"+$("#email").val(), function( data ) {
					  if( data == "0" )
					  {
						$("body").off( "click", "#nextform0", submitevent );
					 	$("#nextform0").attr("data-slide","next");	
					 	$("#nextform0").removeAttr("disabled");
					  }
					  else
					  {
					 	$("#nextform0").removeAttr("disabled");
						//$("#form_user").trigger("submit");
					  }
					});
				}
				else
				{
					 $("body").off( "click", "#nextform0", submitevent );
					 $("#nextform0").removeAttr("data-slide");
					 $("#nextform0").attr("disabled","");
				}
			});


			 $("#nextform0").on('click', () =>
			{

				if( isEmail($("#email").val()))
				{

					$.get( "{{APP_PREFIX}}/alreadyregister/email/"+$("#email").val(), function( data ) {
					  if( data == "0" )
					  {
					  }
					  else
					  {
						$("#form_user").trigger("submit");
					  }
					});
				}
				else
				{
				}
			});

			</script>

		<div class="carousel-item">
					<video width="320" height="240" controls >
<!--					<source src="{{config['questionIdentificationVideo'][0]}}" type="video/mp4"> -->
					<source src="/static/video/SUB_Intro.mp4" type="video/mp4">
					Your browser does not support the video tag.
					</video>
			<br>
      			<p>Cette enquête est proposée dans le cadre du projet Avatar Signeur de l'IRISA (laboratoire de recherche en informatique à Vannes).</p>

			<p>Nous allons vous présenter plusieurs vidéos sur lesquelles nous vous poserons quelques questions. Ces vidéos montrent des personnages virtuels qui réalisent des signes ou des phrases en langue des signes française (LSF).</p> 

			<p>Vous avez la possibilité de rejouer les vidéos autant de fois que vous le souhaitez.</p>

			<p>A la fin du questionnaire, vous aurez l'occasion de vous exprimer sur votre ressenti.</p>

			<p>Le recueil des résultats de ce test respectera l’anonymat de l’ensemble des participants.</p>

			<p>Si vous rencontrez des problèmes ou si vous voulez de plus amples informations sur le projet, merci de contacter Lucie NAERT à <a href="mailto:lucie.naert@univ-ubs.fr">lucie.naert@univ-ubs.fr</a> .</p>

			<p><font color="red">* Champ Obligatoire </font></p>

			<p><b>Nous vous demandons de répondre sérieusement aux questions présentées ci-après. Merci d'indiquer votre accord quant au fait de donner des réponses sincères : <font color="red">*</font></b></p>
			<br>

<!--<input type="radio" name="accord_sincere" value="ok" required > Je suis d'accord<br>  -->

	 		<div class="row">
  				<input id="jesuisdaccord" name="jesuidaccord" type="checkbox" class="col-1"> 
				<label class="col-10" for="jesuisdaccord">
  				  	  Je suis d'accord 
  				</label>
			</div>

			<br>                       
<!-- 			<a  href="#myCarousel"  class="btn btn-lg btn-secondary col-3" data-slide="prev">Préc  </a>  -->
<!--			<a  href="#myCarousel"  class="btn btn-lg btn-success   col-5" data-slide="next">Suiv  </a>   -->
  			<a  id="nextform1" href="#myCarousel"  class="btn btn-lg btn-success   col-3" disabled >Suivant</a>
  
  	  	</div>


		<script>

			 $("#nextform1").on('mouseenter', () =>
			{

				if( $("#jesuisdaccord").is(':checked'))
				{
					 $("#nextform1").attr("data-slide","next");	
					 $("#nextform1").removeAttr("disabled");
				}
				else
				{
					 $("#nextform1").removeAttr("data-slide");
					 $("#nextform1").attr("disabled","");
				}
			});
			
		</script>
    
 		<div id="LaPetiteBoite_form2" class="carousel-item">
  			<h4><strong>Questions préliminaires</strong> </h4>
					<video width="320" height="240" controls >
<!--					<source src="{{config['questionIdentificationVideo'][0]}}" type="video/mp4">  -->
					<source src="/static/video/SUB_Prelim_intro.mp4" type="video/mp4">
					Your browser does not support the video tag.
					</video>
			<br>
  			<p>Merci de bien vouloir répondre aux questions suivantes qui permettront d'établir votre profil.</p>
			
			<!-- Genre  -->
			<h5>Sexe <font color="red">*</font> </h5>

					<video width="320" height="240" controls >
<!--					<source src="{{config['questionIdentificationVideo'][0]}}" type="video/mp4">  -->
					<source src="/static/video/SUB_Prelim_Genre.mp4" type="video/mp4">
					Your browser does not support the video tag.
					</video>

			<div class="form-check">
			    <input type="radio" value="m" class="form-check-input" name="genre" required>
			  <label class="form-check-label" style="margin-left:30px;" > Masculin </label>
			</div>
			<div class="form-check">
			    <input type="radio" value="f" class="form-check-input" name="genre" >
			  <label class="form-check-label" style="margin-left:30px;" > Féminin </label>
			</div>
			<div class="form-check">
			    <input type="radio" value="o" class="form-check-input" name="genre" >
			  <label class="form-check-label" style="margin-left:30px;" > Autre </label>
			</div>

			<br>

  			<h5>Age <font color="red">*</font> </h5>
					<video width="320" height="240" controls >
<!--					<source src="{{config['questionIdentificationVideo'][0]}}" type="video/mp4">  -->
					<source src="/static/video/SUB_Prelim_age.mp4" type="video/mp4">

					Your browser does not support the video tag.
					</video>

			<div class="form-group">
			      <label for="age"></label>
			      <input type="text" name="age" class="form-control" id="age" min=0 max=100>
			</div>
       
<!--  			<a  href="#myCarousel"  class="btn btn-lg btn-secondary col-3" data-slide="prev">Préc  </a>   -->
			<br>                                            
  			<a id="nextform2" href="#myCarousel" class="btn btn-lg btn-success  col-3" disabled >Suivant  </a>

  	      </div>
		<script>

		
			$("#nextform2").on('mouseenter', () =>
			{


				if( ($('input[type=radio][name=genre]:checked').length == 1 )
					&&
				   ( (parseInt($("#age").val()) >= parseInt($("#age").attr("min"))) && (parseInt($("#age").val()) <= parseInt($("#age").attr("max") )) )

				)
				{
	
					$("#nextform2").attr("data-slide","next");	
					$("#nextform2").removeAttr("disabled");

				}
				else
				{
					$("#nextform2").removeAttr("data-slide");
					$("#nextform2").attr("disabled","");
				}


			});
			
		</script>
    

<!-- regex département Ok = dpt.français + DOM + 00(étranger) : /^0[1-9]|[1-8][0-9]|9[0-8]|2A|2B|971|972|973|974|976|00$/-->
    
    	      <div class="carousel-item">
      			<h4><strong>Questions préliminaires</strong> </h4>

				<video width="320" height="240" controls >
<!--				<source src="{{config['questionIdentificationVideo'][0]}}" type="video/mp4">  -->
				<source src="/static/video/SUB_Prelim_DepartNaiss.mp4" type="video/mp4">

				Your browser does not support the video tag.
				</video>
			<br>                                            
  			<h5>N° du département de naissance (00 si né à l'étranger) <font color="red">*</font> </h5>
			<div class="form-group">
			     <label for="DptNaiss"></label>
			     <input type="text" name="DptNaiss" class="form-control" id="DptNaiss">
			</div>
			<br>                                            
				<video width="320" height="240" controls >
<!--				<source src="{{config['questionIdentificationVideo'][0]}}" type="video/mp4">  -->
				<source src="/static/video/SUB_Prelim_DepartRes.mp4" type="video/mp4">

				Your browser does not support the video tag.
				</video>

		        <h5>N° du département de résidence (00 si résidant à l'étranger) <font color="red">*</font> </h5>


		        <div class="form-group">
		           <label for="DptRes"></label>
		           <input type="text" name="DptRes" class="form-control" id="DptRes">
		        </div>
                      
<!--  			<a  href="#myCarousel"  class="btn btn-lg btn-secondary col-3" data-slide="prev">Préc  </a>  -->
			<br>  
  			<a  id="nextform3" href="#myCarousel" class="btn btn-lg btn-success  col-3" data-slide="next">Suivant </a>
  
      	    </div>
		<script>

			function isDepartementOk(dpt) {
				  var regex = /^0[1-9]$|^[1-8][0-9]$|^9[0-8]$|^2A$|^2B$|^971$|^972$|^973$|^974$|^976$|^00$/; 

 				 return regex.test(dpt);
			}


			$("#nextform3").on('mouseenter', () =>
			{


				if( (isDepartementOk($("#DptNaiss").val()) )
					&&
				    (isDepartementOk($("#DptRes").val()) )

				)
				{
	
					$("#nextform3").attr("data-slide","next");	
					$("#nextform3").removeAttr("disabled");

				}
				else
				{
					$("#nextform3").removeAttr("data-slide");
					$("#nextform3").attr("disabled","");
				}


			});


    		</script>

   	    <div class="carousel-item">

      			<h4><strong>Questions préliminaires</strong> </h4>
			<br> 
				<video width="320" height="240" controls >
<!--				<source src="{{config['questionIdentificationVideo'][0]}}" type="video/mp4">  -->
				<source src="/static/video/SUB_Prelim_ident.mp4" type="video/mp4">

				Your browser does not support the video tag.
				</video>
			<br> 
			<h5>Comment vous identifiez-vous ? <font color="red">*</font> </h5> 
			<div class="form-check">
			    <input type="radio" class="form-check-input" name="IdentM" value="sourdnaiss">
			  <label class="form-check-label" style="margin-left:30px;" > Sourd(e) de naissance </label>
			</div>
			<div class="form-check">
			    <input type="radio" class="form-check-input" name="IdentM" value="devsourd">
			  <label class="form-check-label" style="margin-left:30px;" > Devenu(e) sourd </label>
			</div>
			<div class="form-check">
			    <input type="radio" class="form-check-input" name="IdentM" value="Malentend">
			  <label class="form-check-label" style="margin-left:30px;"  > Malentendant(e) </label>
			</div>
			<div class="form-check">
			    <input type="radio" class="form-check-input" name="IdentM" value="Entend" >
			  <label class="form-check-label" style="margin-left:30px;" value="oK" > Entendant(e) </label>
			</div>
  			<br>                       
  			<br>                       

				<video width="320" height="240" controls >
<!--				<source src="{{config['questionIdentificationVideo'][0]}}" type="video/mp4">  -->
				<source src="/static/video/SUB_Prelim_connaissanceSourd.mp4" type="video/mp4">

				Your browser does not support the video tag.
				</video>
  		       <h5>Y a t-il des personnes sourdes dans votre entourage ? <font color="red">*</font> </h5>
  
			<div class="form-check">
			    <input type="checkbox" name="entourage" class="form-check-input"  value="proche">

			    <label class="form-check-label" style="margin-left:30px;"> Famille proche </label>

			</div>

			<div class="form-check">
			    <input type="checkbox" name="entourage" class="form-check-input"  value="distante">

			    <label class="form-check-label" style="margin-left:30px;"> Famille distante </label>

			</div>

			<div class="form-check">
			    <input type="checkbox" name="entourage" class="form-check-input"  value="Ami">

			    <label class="form-check-label" style="margin-left:30px;"> Ami </label>

			</div>

			<div class="form-check">
			    <input type="checkbox" name="entourage" class="form-check-input"  value="travail">

			    <label class="form-check-label" style="margin-left:30px;"> Collègue de travail </label>

			</div>

			<div class="form-check">
			    <input type="checkbox" name="entourage" class="form-check-input"  value="Autre">

			    <label class="form-check-label" style="margin-left:30px;"> Autre </label>

			</div>

			<div class="form-check">
			    <input type="checkbox" name="entourage" class="form-check-input"  value="Non">

			    <label class="form-check-label" style="margin-left:30px;"> Non </label>

			</div>
      
   			<br>  
   			<br>                                                              
  			<a  id="nextform4" href="#myCarousel" class="btn btn-lg btn-success  col-3" data-slide="next">Suivant  </a>

   		</div>
		<script>


			$("#nextform4").on('mouseenter', () =>
			{

				if( ($('input[type=radio][name=IdentM]:checked').length == 1 )
					&&
				    ($('input[type=checkbox][name=entourage]:checked').length >= 1 )
				)
				{
					$("#nextform4").attr("data-slide","next");	
					$("#nextform4").removeAttr("disabled");
				}
				else
				{
					$("#nextform4").removeAttr("data-slide");
					$("#nextform4").attr("disabled","");
				}

			});

    		</script>
 
   	    <div class="carousel-item">
      			<h4><strong>Questions préliminaires</strong> </h4>
				<video width="320" height="240" controls >
<!--				<source src="{{config['questionIdentificationVideo'][0]}}" type="video/mp4">  -->
				<source src="/static/video/SUB_Prelim_niveauLSF.mp4" type="video/mp4">

				Your browser does not support the video tag.
				</video>
			<h5>Quel est votre niveau de connaissance de la LSF (Langue des signes Française) ?<font color="red">*</font> </h5>


			<div class="form-check">
			    <input type="radio" class="form-check-input" name="NiveauLSF" value="natif" required>
			  <label class="form-check-label" style="margin-left:30px;" > Signeur natif </label>
			</div>
			<div class="form-check">
			    <input type="radio" class="form-check-input" name="NiveauLSF" value="Interprete">
			  <label class="form-check-label" style="margin-left:30px;" > Interprète </label>
			</div>
			<div class="form-check">
			    <input type="radio" class="form-check-input" name="NiveauLSF" value="Tres bon" >
			  <label class="form-check-label" style="margin-left:30px;" > Très bon </label>
			</div>
			<div class="form-check">
			    <input type="radio" class="form-check-input" name="NiveauLSF" value="Bon">
			  <label class="form-check-label" style="margin-left:30px;" > Bon </label>
			</div>
			<div class="form-check">
			    <input type="radio" class="form-check-input" name="NiveauLSF" value="Assez Bon">
			  <label class="form-check-label" style="margin-left:30px;" > Assez Bon </label>
			</div>
			<div class="form-check">
			    <input type="radio" class="form-check-input" name="NiveauLSF" value="Débutant">
			  <label class="form-check-label" style="margin-left:30px;" > Débutant </label>
			</div>
			<div class="form-check">
			    <input type="radio" class="form-check-input" name="NiveauLSF" value="Pas de connaissance">
			  <label class="form-check-label" style="margin-left:30px;" > Pas de connaissance de la LSF </label>
			</div>
			
<!--  			<input id="Btnsubmit" type="submit"   class="btn btn-lg btn-primary  col-3" value="submit" disabled>  -->
  			<br>                       
<!--  			<input id="Btnsubmit" type="submit"   class="btn btn-lg btn-primary  col-3" value="Envoyer" disabled>  -->
<!--		bouton submit remplacé par un bouton suivant pour aller à la diapo suivante sur la présentation de la Partie 1  -->
  			<a  id="nextform5" href="#myCarousel" class="btn btn-lg btn-success  col-3" data-slide="next">Suivant  </a>

   		</div>


 		<script>
	
			$("#nextform5").on('mouseenter', () =>
			{


				if( $('input[type=radio][name=NiveauLSF]:checked').length == 1 

				)
				{
	
					<!-- $("#Btnsubmit").removeAttr("disabled"); -->
					$("#nextform5").attr("data-slide","next");	
					$("#nextform5").removeAttr("disabled");


				}
				else
				{

					<!-- $("#Btnsubmit").attr("disabled","");  -->
					$("#nextform5").removeAttr("data-slide");
					$("#nextform5").attr("disabled","");

				}


			});
			
		</script>
    
  	    <div class="carousel-item">
      			<h4><strong>Noms d'animaux en signes</strong> </h4>
				<video width="320" height="240" controls >
<!--				<source src="{{config['questionIdentificationVideo'][0]}}" type="video/mp4">  -->
				<source src="/static/video/SUB_part1_intro.mp4" type="video/mp4">

				Your browser does not support the video tag.
				</video>
     			<p>Dans cette première partie, vous allez voir 18 vidéos avec des personnages virtuels signant des noms d'animaux.</p>

				<p>Il vous sera demandé de répondre à trois questions sur chaque vidéo.</p> 

				<p>Ces personnages peuvent prendre trois apparences différentes.</p>

				<p>Et maintenant un petit entraînement pour que vous visualisiez le type de vidéo qui vous sera présentées. Les réponses correspondant à cet entraînement ne compteront pas.</p>

			
  			<br>                       
<!--  			<input id="Btnsubmit" type="submit"   class="btn btn-lg btn-primary  col-3" value="Envoyer" disabled>  -->
<!--		bouton submit actif -->

  			<input id="Btnsubmit" type="submit"   class="btn btn-lg btn-primary  col-3" value="Envoyer"  >

   		</div>

<!-- pas de script pour cette dernière diapo  :le bouton Submit est actif sans condition   -->    
    
  </div>


        
</div>

 </form>


				</div>
			</div>
		</div>
	</div>

	<div class="container" style="padding: 0px;">
		<div class="row">
			<div class="col-sm-offset-2 col-sm-4 col-md-offset-3 col-md-3">
				<a href="http://www.irisa.fr" target="_blank">
					<img src="{{APP_PREFIX}}/static/img/logo_irisa.png" class="img-responsive center-block" alt="IRISA lab">
				</a>
			</div>
			<div class="col-sm-4 col-md-3">
				<a href="http://www-expression.irisa.fr" target="_blank">
					<img src="{{APP_PREFIX}}/static/img/logo_expression.png" class="img-responsive center-block" alt="Expression team">
				</a>
			</div>
		</div>
		<p class="text-muted text-center" style="letter-spacing: 2px; line-height: 40px;"><a href="https://gitlab.inria.fr/dlolive/PercepEval" target="_blank">Powered by PercEval.</a></p>
	</div>

	</body>

</html>
