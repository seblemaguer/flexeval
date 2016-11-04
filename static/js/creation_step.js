$('.type label').click(function() {
	//alert("Value of Radion: " + $(this).prev().val()+ " Name of radio: " + $(this).prev().attr("name"));       
	$('.inner').html("<h5>"+$('#'+$(this).attr('for')).attr('value')+"</h5>");
	if($('#'+$(this).attr('for')).attr('value')=="testAB") {
		$('.inner').html("<div class=\"form-group\">\
						<label for=\"fileA\">Select file A</label>\
						<input type=\"file\" id=\"fileA\">\
					</div>\
					<div class=\"form-group\">\
						<label for=\"fileB\">Select file B</label>\
						<input type=\"file\" id=\"fileB\">\
					</div>");
	} else if($('#'+$(this).attr('for')).attr('value')=="testABX") {
    	$('.inner').html("<div class=\"form-group\">\
						<label for=\"fileX\">Select file X</label>\
						<input type=\"file\" id=\"fileX\">\
					</div>\
					<div class=\"form-group\">\
						<label for=\"fileA\">Select file A</label>\
						<input type=\"file\" id=\"fileA\">\
					</div>\
					<div class=\"form-group\">\
						<label for=\"fileB\">Select file B</label>\
						<input type=\"file\" id=\"fileB\">\
					</div>");
    } else if($('#'+$(this).attr('for')).attr('value')=="testMOS") {
    	$('.inner').html("<div class=\"form-group\">\
						<label for=\"fileA\">Select file to evaluate</label>\
						<input type=\"file\" id=\"fileA\">\
					</div>");
    } else if($('#'+$(this).attr('for')).attr('value')=="testDMOS") {
    	$('.inner').html("<div class=\"form-group\">\
						<label for=\"fileA\">Select reference file</label>\
						<input type=\"file\" id=\"fileA\">\
					</div>\
					<div class=\"form-group\">\
						<label for=\"fileB\">Select file to evaluate</label>\
						<input type=\"file\" id=\"fileB\">\
					</div>");
    } else {
    	alert("error")
    }
});