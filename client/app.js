document.addEventListener("DOMContentLoaded", function(){
    document.getElementById('speech-form').addEventListener("submit",  function(e){
      e.preventDefault()
      let file1 = document.getElementById('form-file').files[0]
      let file2 = audioBlob
      if(file1) {
        document.getElementById('results').innerHTML = `<p class='loading'>Predicting Class....</p>`;
        let formData = new FormData()
        formData.append('image', file1)
        fetch("https://ae6c9f894002.ngrok.io/file", {
            method: "POST",
            body: formData
        }).then(res => res.json()).then((result) => {
            let ele = document.getElementById('results')
            let type = result.result[2] === 'D' ? 'Dysarthric Speech' : 'Non Dysarthric Speech'
            ele.innerHTML = `
            <h3> Results </h3>
            <p><b>Time 🕒 : </b> ${result.time}</p>
            <p><b>Class : </b> ${type}</p>`;
            return;
        })
      } else if(file2) {
        document.getElementById('results').innerHTML = `<p class='loading'>Predicting Class....</p>`;
        let formData = new FormData()
        formData.append('image', file2)
        fetch("https://ae6c9f894002.ngrok.io/file", {
            method: "POST",
            body: formData
        }).then(res => res.json()).then((result) => {
            let ele = document.getElementById('results')
            let type = result.result[2] === 'D' ? 'Dysarthric Speech' : 'Non Dysarthric Speech'
            ele.innerHTML = `
            <h3> Results </h3>
            <p><b>Time 🕒 : </b> ${result.time}</p>
            <p><b>Class : </b> ${type}</p>`;
            return;
        })
      }
    })
  })



  URL = window.URL || window.webkitURL;

  var gumStream; 						//stream from getUserMedia()
  var rec; 							//Recorder.js object
  var input; 							//MediaStreamAudioSourceNode we'll be recording
  
  var audioBlob;

  // shim for AudioContext when it's not avb. 
  var AudioContext = window.AudioContext || window.webkitAudioContext;
  var audioContext //audio context to help us record
  
  var recordButton = document.getElementById("recordButton");
  var stopButton = document.getElementById("stopButton");
  var pauseButton = document.getElementById("pauseButton");
  
  //add events to those 2 buttons
  recordButton.addEventListener("click", startRecording);
  stopButton.addEventListener("click", stopRecording);
  pauseButton.addEventListener("click", pauseRecording);
  
  function startRecording() {
      console.log("recordButton clicked");
  
      /*
          Simple constraints object, for more advanced audio features see
          https://addpipe.com/blog/audio-constraints-getusermedia/
      */
      
      var constraints = { audio: true, video:false }
  
       /*
          Disable the record button until we get a success or fail from getUserMedia() 
      */
  
      recordButton.disabled = true;
      stopButton.disabled = false;
      pauseButton.disabled = false
  
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
          audioContext = new AudioContext();
  
          //update the format 
  
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
          rec.record()
  
          console.log("Recording started");
  
      }).catch(function(err) {
            //enable the record button if getUserMedia() fails
          console.log(err)
          recordButton.disabled = false;
          stopButton.disabled = true;
          pauseButton.disabled = true
      });
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
      stopButton.disabled = true;
      recordButton.disabled = false;
      pauseButton.disabled = true;
  
      //reset button just in case the recording is stopped while paused
      pauseButton.innerHTML="Pause";
      
      //tell the recorder to stop the recording
      rec.stop();
  
      //stop microphone access
      gumStream.getAudioTracks()[0].stop();
  
      //create the wav blob and pass it on to createDownloadLink
      rec.exportWAV(createDownloadLink);
  }
  
  function createDownloadLink(blob) {
      
      var url = URL.createObjectURL(blob);
      
      //name of .wav file to use during upload and download (without extendion)
      var filename = new Date().toISOString();
  
        audioBlob = blob
}