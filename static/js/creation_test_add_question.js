function choix_binaire(id) {
	return "<div id="+id+">\
				<h4>Choix Binaire <a href='#'><span class='removeQuestion glyphicon glyphicon-remove' style='color:black'></span></a></h4>\
				Question :\
				<textarea class='form-control' rows='2'></textarea>\
				Réponse A :\
				<input class='form-control'></input>\
				Réponse B :\
				<input class='form-control'></input>\
			</div>";
}

function note(id) {
	return "<div id="+id+">\
				<h4>Note <a href='#'><span class='removeQuestion glyphicon glyphicon-remove' style='color:black'></span></a></h4>\
				Question :\
				<textarea class='form-control' rows='2'></textarea>\
			</div>";
}


$(function(){
	$("#dropdown-menu_choice li a").on('click', function(){
		$("#dropdown_choice:first-child").html($(this).text()+" <span class='caret'></span>");
		$("#dropdown_choice:first-child").val($(this).text());
	});
});

var id = 0
$(function(){
	$(".container").on('click', "#add", function(){
		id++
		if($("#dropdown_choice").text() === "Note ")
			$("#questions").append(note(id));
		else if($("#dropdown_choice").text() === "Choix binaire ")
			$("#questions").append(choix_binaire(id));
	});
});

$(function(){
	$(".container").on('click', ".removeQuestion", function(){
		$("#"+this.parentElement.parentElement.parentElement.id).remove()
	});
});