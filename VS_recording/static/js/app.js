


URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input;
var tempBlob;
//MediaStreamAudioSourceNode we'll be recording
// var recordButtonText="Record";
// document.getElementById("recordButton").innerHTML = "adfadf";
// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record
// get the sentence name
var senten = document.getElementById("sentence").innerHTML;
// document.getElementById("senten").innerHTML = senten;
console.log("hello");
var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

function startRecording() {
	if(recordButton.innerHTML=="Stop"){
		stopRecording();

	}else if(recordButton.innerHTML=="Try Again"){

		window.location.reload();
	}
	else{
		console.log("recordButton clicked");

	/*
		Simple constraints object, for more advanced audio features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/

    var constraints = { audio: true, video:false }

 	/*
    	Disable the record button until we get a success or fail from getUserMedia()
	*/

	recordButton.disabled = false;
	// stopButton.disabled = false;
	// pauseButton.disabled = false

	/*
    	We're using the standard promise based getUserMedia()
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

		/*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device

		*/
		audioContext = new AudioContext({sampleRate: 96000});

		//update the format
		document.getElementById("formats").innerHTML=" channel: 1 and "+audioContext.sampleRate/1000+"kHz"

		/*  assign to gumStream for later use  */
		gumStream = stream;

		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);

		/*
			Create the Recorder object and configure to record mono sound (1 channel)
			Recording 2 channels  will double the file size
		*/
		rec = new Recorder(input,{numChannels:1})

		//start the recording process
		recordButton.innerText="Stop";
		rec.record()

		console.log("Recording started");


	}).catch(function(err) {
	  	//enable the record button if getUserMedia() fails
    	recordButton.disabled = false;
    	// stopButton.disabled = true;
    	// pauseButton.disabled = true
	});
	}

}

function pauseRecording(){
	console.log("pauseButton clicked rec.recording=",rec.recording );
	if (rec.recording){
		//pause
		rec.stop();
		pauseButton.innerHTML="Resume";
	}else{
		//resume
		rec.record()
		pauseButton.innerHTML="Pause";

	}
}

function stopRecording() {
	console.log("stopButton clicked");

	//disable the stop button, enable the record too allow for new recordings
	// stopButton.disabled = true;
				// recordButton.disabled = false;
	// pauseButton.disabled = true;

	//reset button just in case the recording is stopped while paused
	// pauseButton.innerHTML="Pause";
	recordButton.innerHTML="Try Again";
	//tell the recorder to stop the recording
	rec.stop();

	//stop microphone access
	gumStream.getAudioTracks()[0].stop();

	//create the wav blob and pass it on to createDownloadLink
	rec.exportWAV(createDownloadLink);

	// rec.exportWAV(setblob);
    // rec.exportWAV(sendData);
	// tempBlob= rec.getBuffer();
	// console.log(tempBlob)

}

// function setblob(blob){
// 	tempBlob=blob;
// }



function createDownloadLink(blob) {

	var url = URL.createObjectURL(blob);
	var au = document.createElement('audio');
	var li = document.createElement('li');
	var link = document.createElement('a');



	//name of .wav file to use during upload and download (without extendion)

	// var filename = new Date().toISOString();
	var filename = senten;
	//add controls to the <audio> element
	au.controls = true;
	au.src = url;

	//save to disk link
	link.href = url;
	// link.href = "C:\\Users\\ASUS\\PycharmProjects\\VS_recording\\files"
	link.download = filename+".wav"; //download forces the browser to donwload the file using the  filename
	link.innerHTML = "Save to disk";


	//add the new audio element to li
	li.appendChild(au);

	//add the filename to the li
	li.appendChild(document.createTextNode(filename+".wav "))

	//add the save to disk link to li
	li.appendChild(link);

	//upload link
	var upload = document.createElement('a');
	upload.href="/upload";
	upload.innerHTML = "Upload";
	upload.addEventListener("click", function(event){
		  var xhr=new XMLHttpRequest();
		  xhr.onload=function(e) {
		      if(this.readyState === 4) {
		          console.log("Server returned: ",e.target.responseText);
		      }
		  };
		  // for php server
		  var fd=new FormData();
		  fd.append("audio_data",blob, filename);
		  console.log("phpphp");
		  xhr.open("POST",`static/php/upload.php`,true);
		  xhr.send(fd);
	})
	// li.appendChild(document.createTextNode (" "))//add a space in between
	li.appendChild(upload)//add the upload link to li

	//add the li element to the ol
	recordingsList.appendChild(li);
	console.log(recordingsList);
}


function call()
{
	rec.exportWAV(sendData)
}

function sendData(blob) {
	console.log(blob);
	console.log(senten);
	var senten = document.getElementById("sentence").innerHTML;
  let fd = new FormData;
  console.log("here is a sample string");
  var filename_ = senten+'.wav';
  fd.append('ourfile', blob,filename_);
  // fd.append('filename', senten);
	// fd.append('username', 'Chris')
  let token = '{{csrf_token}}';
	console.log('Ajax calling');
  $.ajax({
    url: '/upload',
    type: 'POST',
    headers: { 'X-CSRFToken': token },
    data: fd,
	dataType: 'json',
	  success: function (res, status) {
            // alert(res);
            // alert(status);
        },
        error: function (res) {
            // alert(res.status);
        },
    cache: false,
    processData: false, // essential
    contentType: false, // essential, application/pdf doesn't work.
    enctype: 'multipart/form-data',
  });

  $(document).ajaxStop(function(){
    window.location.reload();
});
}

