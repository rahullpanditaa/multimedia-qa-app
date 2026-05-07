import { useEffect, useRef } from "react";


function MediaPlayer({

  mediaUrl,

  startTime,
}) {

  // direct access to the HTML audio element
  const audioRef = useRef(null);


  // seek and play when timestamp changes
  useEffect(() => {

    // Skip if player not ready yet
    if (!audioRef.current) {
      return;
    }

    const player = audioRef.current;

    // Jump playback position
    player.currentTime = startTime;

    // Start playback automatically
    player.play();

  }, [startTime, mediaUrl]);

  return (

    <div>

      <h3>Media Player</h3>

      <audio
        ref={audioRef}

        controls

        style={{
          width: "100%",
          marginTop: "10px",
        }}
      >

        <source
          src={mediaUrl}
          type="audio/mpeg"
        />

        Your browser does not support audio playback.

      </audio>

    </div>
  );
}


export default MediaPlayer;