$(document).ready( function() {

$.ajax({url: "/api/voices", success: function(result){
		var arrayLength = result["results"].length;
		var htmlString='';
		for (var i = 0; i < arrayLength; i++) {
			var voice = result["results"][i]
			htmlString += "<option value='"+voice["name"]+"'>"+voice["description"]+"</option>" + "\n";
		}
		//console.log(htmlString);
        $("#voices").html(htmlString);

        $('#textToSpeak').on('change', function() {
        	var textToSpeak = $(this).val();
    		var speakerVoice = $("#voices").val();
    		$.post({
    			url: "/api/speak",
    			data: JSON.stringify({ "text": textToSpeak, "voice" : speakerVoice }),
    			contentType: "application/json",
    			dataType: 'json',

    		})
		});
    }});
});