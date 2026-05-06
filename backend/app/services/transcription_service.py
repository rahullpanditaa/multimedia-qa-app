"""
This service handles audio/video transcription using Faster Whisper.
"""

from faster_whisper import WhisperModel


# Load Whisper model
model = WhisperModel(
    "tiny",
    compute_type="int8",
)

def transcribe_media(filepath: str):
    """
    Transcribe audio/video file.

    Returns:
        List of timestamped segments.
    """

    segments, info = model.transcribe(filepath)

    transcript_segments = []

    for segment in segments:

        transcript_segments.append(
            {
                "text": segment.text,

                # timestamps in seconds
                "start": segment.start,
                "end": segment.end,
            }
        )

    return transcript_segments