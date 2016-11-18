%include('header.tpl', test_code=test_code, author=author, description=description, samples=samples)
<div class="col-md-6 col-md-offset-3">
	<p>The question that follows here is just an example and not generated from any script!</p>
	<p>Your role as a test maker is to edit this part!</p>
	<form role="form" action="/test/{{test_code}}" method="POST">
		<input type="hidden" name="ref" value="{{index}}">
		% for i in range(len(questions)):
			<h3>Question {{i+1}}</h3>
			<div class="alert alert-info" role="alert">{{i.description}}</div>
			<div class="col-md-offset-2">
			%if i.type=="radio":
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
			%else if i.type=="range":
				<div class="answer">
					<label>Avis : </label>
					<label id="rate">3</label>
					<label> étoiles</label>
					<div id="slider{{i.id}}"></div>
					<label>Mauvais</label>
					<label style="float: right;">Excellent</label>
				</div>
				<script>
					$(function() {
						$("#slider{{i.id}}").slider({
							range: "min",
							value:3,
							min: 0,
							max: 6,
							step: 1,
							slide: function(event, ui) {
								$("#rate").html(ui.value);
							}
						});
					} );
				</script>
			%else:
				<div>Problème...</div>
			%end
		% end
		</div>
		<input type="submit" class="btn btn-lg btn-success btn-block pull-right" value="Next">
	</form>
</div>
%include('footer.tpl')