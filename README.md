Controlify
=======

Controlify is a programm to controll your Spotify Session via Voice Commands. It uses Deepspeech moduls to translate your speech to text.

  <h3>The Commands are:</h3>

    next : for the next Song in Queue

    previous : for the previous Song in Queue

    start/play : for playing the currently selected Song

    stop/pause : for stopping the currently selected Song

    names/name : Outputs all playlists with a number from which you follow via voice output

    <number> : adds the Playlist with the number that was given to them via names/name in the Queue


  <h3>Installation:</h3>

  To install the requirements run:

    pip install -r requirements.txt

  You also need to download a Deepspeech modul. You can use these Models.

    https://github.com/mozilla/DeepSpeech/releases/download/v0.8.1/deepspeech-0.8.1-models.pbmm

    https://github.com/mozilla/DeepSpeech/releases/download/v0.8.1/deepspeech-0.8.1-models.scorer

  You also have to Connect the App with your Spotify Account. For that visit Spotify Developer.

    https://developer.spotify.com/dashboard/login

  You have to Login there with your personnal Spotify Account. Then you have to created a App. After createing an App you will find a 

    client_id 

  and a 

    clint_secret

  in the top left of the Website. Add these Keys to a "Controlify_Config" in the following design.

    {
      "client_id": "here_is_your_client_id",
      "client_secret": "here_is_your_client_secret"
    }
    

   Run:

  You can run the Programm with the following command code.

    python Controlify_Run.py --model path/to/model/deepspeech-0.8.1-models.pbmm --scorer path/to/model/deepspeech-0.8.1-models.scorer -d 1

    --model needs a .pbmm file
    --scorer needs a .scorer file
    -d needs the ID number of the Microphone oyu are using. To find out your ID you can run the WhichAudioInputDevices.py to see all devices with IDs.

