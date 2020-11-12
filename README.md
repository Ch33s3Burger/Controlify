# Controlify

Controlify is a programm to controll your Spotify Session via Voice Commands. It uses Deepspeech moduls to translate your speech to text.

The Commands are:

  next : for the next Song in Queue
  
  previous : for the previous Song in Queue
  
  start/play : for playing the currently selected Song
  
  stop/pause : for stopping the currently selected Song
  
  names/name : Outputs all playlists with a number from which you follow via voice output
  
  <number> : adds the Playlist with the number that was given to them via names/name in the Queue
  
  
Installation:

  To install the requirements run:
  
    pip install -r requirements.txt
    
  You also need to download a Deepspeech modul. You can use these Models.
  
    https://github.com/mozilla/DeepSpeech/releases/download/v0.8.1/deepspeech-0.8.1-models.pbmm
    
    https://github.com/mozilla/DeepSpeech/releases/download/v0.8.1/deepspeech-0.8.1-models.scorer
    
 Run:
 
  You can run the Programm with the following command code.
  
    python Controlify_Run.py --model path/to/model/deepspeech-0.8.1-models.pbmm --scorer path/to/model/deepspeech-0.8.1-models.scorer -d 1
    
    --model needs a .pbmm file
    --scorer needs a .scorer file
    -d needs the ID number of the Microphone oyu are using. To find out your ID you can run the WhichAudioInputDevices.py to see all devices with IDs.
