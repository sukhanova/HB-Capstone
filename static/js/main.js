"use strict";

$(document).ready(function() {
	const userNotes = $('#userNotes');
	$('#addNoteForm').submit(function(evt) {
		evt.preventDefault();
		const formData = $(this).serializeArray()
		const payload = {
			data: { note: formData[0].value },
			method: 'POST',
			url: '/add_note'
		};
		const userNoteReq = $.ajax(payload);
		userNoteReq.then(function(res) {
			const htmlToAdd = `<p>${res.note}</p>` 
			userNotes.append(htmlToAdd);
			$('#note').val('');
		})
	});
});
