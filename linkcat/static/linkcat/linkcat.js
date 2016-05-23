function add_link(url) {
	$('#add-link').slideDown();
	$('#add-link').load(url);
	$('#add-link-btn-a').toggleClass('btn-primary btn-default');
	var new_url = "javascript:toggle_add_link('"+url+"')";
	$('#add-link-btn-a').attr('href', new_url);
}

function hide_add_link() {
	$('#add-link').hide();
}

function toggle_add_link(url) {
	$('#add-link').slideToggle();
	$('#add-link-btn-a').toggleClass('btn-default btn-primary');
	var new_url = "javascript:add_link('"+url+"')";
	$('#add-link-btn-a').attr('href', new_url);
}

function load_url(block, url) {
	$(block).load(url);
}

