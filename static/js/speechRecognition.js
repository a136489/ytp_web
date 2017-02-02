var final_transcript = '';
var recognizing = false;
var ignore_onend;
var start_timestamp;

if (!('webkitSpeechRecognition' in window)) {
	alert("JIZZ! Your browser do not have Web Recognition API. Please use Google Chrome.")
} else {
	var recognition = new webkitSpeechRecognition();

	console.log(start_timestamp+"j");

	recognition.continuous     = true;
	recognition.interimResults = true;
	recognition.lang           = "en-US";

	recognition.onstart = function() {
		recognizing = true;
		console.log('Start recognizing...');
	};

	recognition.onerror = function(event) {
		console.log("ERROR!");
		recognizing = false;
		recognition.stop();
		recognizing = true;
		recognition.start();
		if (event.error == 'no-speech') {
			console.log("NO SPEECH");
		}
		if (event.error == 'audio-capture') {
			console.log("Capture Problem");
		}
		if (event.error == 'not-allowed') {
			if (event.timeStamp - start_timestamp < 100) {
				console.log('Block');
			} else {
				console.log('Deny');
			}
		}
	};

	recognition.onend   = function() {
		console.log('End recognizing...');
		recognition.stop();
		recognizing = false;
		// recognition.start();
	};

	recognition.onresult = function(event) {
		var interim_transcript = '';
		if (typeof(event.results) == 'undefined') {
			console.log('undefined start');
			recognition.stop();
			recognizing = false;
			recognition.start()
			console.log('undefined end');
			return;
		}
		for (var i = event.resultIndex; i<event.results.length; i++) {
			if (event.results[i].isFinal) {
				final_transcript += event.results[i][0].transcript;
			} else {
				interim_transcript += event.results[i][0].transcript;
			}
		}

		console.log(event);
		console.log(interim_transcript)
		$("#show").text(final_transcript);
	};

	$(".startBtn").click(function () {
		console.log("st")
		// $(".startBtn").text("end!").addClass("endBtn").removeClass("startBtn"); 
		final_transcript = '';
		recognition.start();
		ignore_onend = false;
	});
	$(".endBtn").click(function () {
		console.log("end")
		// $(".endBtn").text("start!").addClass("startBtn").removeClass("endBtn");
		recognition.stop();
		recognizing = false;
	});
}