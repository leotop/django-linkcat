$.ajaxSetup({
  data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});
	
function fire_slide(presentation, screen_number) {
	var body_width = $(window).width();
	var url = "{% url 'screen-loader' presentation_slug=presentation.slug screen_number=584358302682 screen_width=123578545895 %}";
	url = url.replace("123578545895", body_width.toString());
	url = url.replace("584358302682", screen_number.toString());
	$('#fscreen_presentation').load(url);
}