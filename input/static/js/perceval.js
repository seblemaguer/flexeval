/**
 * Add the possibility to define custom events
 */
jQuery.createEventCapturing = (function () {
	var special = jQuery.event.special;
	return function (names) {
		if (!document.addEventListener) {
		return;
		}
		if (typeof names == 'string') {
		names = [names];
		}
		jQuery.each(names, function (i, name) {
		var handler = function (e) {
			e = jQuery.event.fix(e);

			return jQuery.event.dispatch.call(this, e);
		};
		special[name] = special[name] || {};
		if (special[name].setup || special[name].teardown) {
			return;
		}
		jQuery.extend(special[name], {
			setup: function () {
			this.addEventListener(name, handler, true);
			},
			teardown: function () {
			this.removeEventListener(name, handler, true);
			}
		});
		});
	};
})();

/**
 * Define the pause event (useful to detect the end of samples)
 */
jQuery.createEventCapturing(['pause']);  

/**
 * Test if all media (audio or video) samples have been played
 */
function all_played(media) {
	return jQuery(media).toArray().map(function(x) { return x.ended; } ).every(function (x) { return x });
	
};

/**
 * Highlight the select choice
 */
function highlight_selected_choice() {
	var inputName = $(this).attr("name");
	var inputValue = $(this).attr("value");
	
	var targetLine = $("." + inputName + "[id=choice" + inputValue + "]");
	$("." + inputName + "[id!=choice" + inputValue + "]").removeClass("success");
	$(targetLine).addClass("success");
}
