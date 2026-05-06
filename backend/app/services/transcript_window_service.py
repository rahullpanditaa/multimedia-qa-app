"""
Creates rolling transcript windows.

Very small transcript segments often:
- lack semantic meaning
- retrieve poorly
- create noisy matches

Instead of embedding tiny segments individually,
create overlapping transcript windows.

Example:
window 1:
segments 1-3

window 2:
segments 2-4

window 3:
segments 3-5

This creates richer semantic context.
"""


def create_transcript_windows(segments: list[dict], window_size: int = 3):
    """
    Create rolling transcript windows.

    Args:
        segments:
            Whisper transcript segments

        window_size:
            Number of neighboring segments
            to combine together

    Returns:
        Windowed transcript chunks
    """

    windows = []

    # create overlapping windows
    for i in range(len(segments)):

        # Select neighboring segments
        window_segments = segments[i : i + window_size]

        # Stop if window becomes empty
        if not window_segments:
            continue

        # Combine transcript text
        combined_text = " ".join(
            segment["text"]
            for segment in window_segments
        )

        # Window timestamps
        # Start: first segment start
        # End: last segment end
        start_time = window_segments[0]["start"]

        end_time = window_segments[-1]["end"]

        windows.append(
            {
                "text": combined_text,
                "start_time": start_time,
                "end_time": end_time,
            }
        )

    return windows