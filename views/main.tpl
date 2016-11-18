%include('header.tpl', test_code=test_code, author=author, description=description, samples=samples)
<div class="col-md-6 col-md-offset-3">
	<p>The question that follows here is just an example and not generated from any script!</p>
	<p>Your role as a test maker is to edit this part!</p>
	<form role="form" action="/test/{{test_code}}" method="POST">
		<input type="hidden" name="ref" value="{{index}}">
		% for i in range(len(questions)):
		<h3>Question {{i+1}}</h3>
		<div class="alert alert-info" role="alert">Ceci est l'intitulé de ma question</div>
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
		% end
		<input type="submit" class="btn btn-lg btn-success btn-block pull-right" value="Next">
	</form>
</div>
%include('footer.tpl')