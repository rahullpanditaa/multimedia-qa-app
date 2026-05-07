function MediaPlayer({

  mediaUrl,

  startTime,
}) {

  // Play media from timestamp
  function handleLoadedMetadata(event) {

    const player = event.target;

    // Jump to timestamp.
    player.currentTime = startTime;

    // Start playback automatically.
    player.play();
  }

  return (

    <div>

      <h3>Media Player</h3>

      <audio
        controls

        width="100%"

        onLoadedMetadata={
          handleLoadedMetadata
        }
      >

        <source
          src={mediaUrl}
          type="audio/mpeg"
        />

      </audio>

    </div>
  );
}


export default MediaPlayer;