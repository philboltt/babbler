$(document).ready( function() {

$.ajax({url: "/api/voices", success: function(result){
		var arrayLength = result["results"].length;
		var htmlString='';
		for (var i = 0; i < arrayLength; i++) {
			var voice = result["results"][i]
			htmlString += "<option value='"+voice["name"]+"'>"+voice["description"]+"</option>" + "\n";
		}
		$("#voices").html(htmlString);

		var selectedVoice = localStorage.getItem("selectedVoice");
		if (selectedVoice !== null){
			console.log("SelectedVoice = "+selectedVoice);
			$("#voices").val(selectedVoice);
		}

		$("#voices").on('change', function() {
			var speakerVoice = $(this).val();
			console.log("Voice changed to "+speakerVoice);
			localStorage.setItem("selectedVoice", speakerVoice);
		})

        $('#textToSpeak').on('change', function() {
			$("#icon").attr('src','static/images/loader.gif?timestamp=' + new Date().getTime());
        	var textToSpeak = $(this).val();
    		var speakerVoice = $("#voices").val();
    		$.ajax({
				type: 'POST',
    			url: "/api/speak",
    			data: JSON.stringify({ "text": textToSpeak, "voice" : speakerVoice }),
				success: function(result) {
					if (result['success'] === true) {
						$('#textToSpeak').val('');
						$("#icon").attr('src','static/images/yinyang3.png?timestamp=' + new Date().getTime());
					}
				},
    			contentType: "application/json",
    			dataType: 'json',

    		})
		});
    }});
});