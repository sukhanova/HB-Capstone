"use strict";

$(document).ready(function() {
	const userNotes = $('#userNotes');
	$('#addNoteForm').submit(function(evt) {
		evt.preventDefault();
		const formData = $(this).serializeArray()
		const payload = {
			data: { note: formData[0].value },
			method: 'POST',
			url: '/add_note',
		};
		const userNoteReq = $.ajax(payload);
		userNoteReq.then(function(res) {
			const htmlToAdd = `<div>${res.note}<button data-source="{{note.note_id}}" type="submit" class="btn btn-outline-secondary btn-sm remove"><i class="fa fa-trash fa-1" aria-hidden="true">Remove</i></button></div>`
			userNotes.append(htmlToAdd);
			$('#note').val('');
		})
	});
});
