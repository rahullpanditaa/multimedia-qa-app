import { useState } from "react";

import api from "../api/client";

import DocumentSelector from "./DocumentSelector";
import MediaPlayer from "./MediaPlayer";

function TimestampResults() {

  // Selected media doc
  const [
    selectedDocument,
    setSelectedDocument,
  ] = useState(null);

  // User query
  const [question, setQuestion] =
    useState("");

  // Retrieved timestamps
  const [timestamps, setTimestamps] =
    useState([]);

  // Loading state
  const [isLoading, setIsLoading] =
    useState(false);

  // player state
  const [mediaUrl, setMediaUrl] = useState("");
  const [startTime, setStartTime] = useState(0);

  // Format timestamps - eg 125 secs to 02:05
  function formatTimestamp(seconds) {

    const minutes = Math.floor(
      seconds / 60
    );

    const remainingSeconds =
      Math.floor(seconds % 60);

    return (
      String(minutes).padStart(2, "0")
      +
      ":"
      +
      String(
        remainingSeconds
      ).padStart(2, "0")
    );
  }

  async function fetchTimestamps() {
    if (
      !selectedDocument || !question) {

      alert(
        "Please select a document and ask a question."
      );

      return;
    }

    setIsLoading(true);

    // Clear old results
    setTimestamps([]);

    try {
      const response =
        await api.post(
          "/timestamps/",
          {
            question,

            document_id: Number(
              selectedDocument.id
            ),
          }
        );

      // Store timestamp results
      setTimestamps(
        response.data.timestamps
      );

    } catch (error) {

      console.error(error);

    } finally {

      setIsLoading(false);
    }
  }

  return (

    <div>

      <h2>Timestamp Search</h2>

      {/* Select media document */}
      <DocumentSelector
        selectedDocument={
          selectedDocument
        }

        setSelectedDocument={
          setSelectedDocument
        }
      />

      {/* User question */}
      <textarea
        placeholder="Ask about a topic in the media..."
        value={question}
        onChange={(event) =>
          setQuestion(
            event.target.value
          )
        }
      />

      {/* Search button */}
      <button
        type="button"
        onClick={fetchTimestamps}
      >
        Find Timestamps
      </button>

      {/* Loading state */}
      {isLoading && (
        <p>
          Searching timestamps...
        </p>
      )}

      {/* Timestamp results */}
      {timestamps.length > 0 && (

        <div>

          <h3>Results</h3>

          {timestamps.map(
            (timestamp, index) => (

              <div
                key={index}
                className="timestamp-card"
              >

                {/* Timestamp range */}
                <p>

                  <strong>

                    {formatTimestamp(
                      timestamp.start_time
                    )}

                    {" - "}

                    {formatTimestamp(
                      timestamp.end_time
                    )}

                  </strong>

                </p>

                {/* Transcript snippet */}
                <p>
                  {timestamp.text}
                </p>

                {/* playback button */}
                <button type="button" 
                onClick={() => {
                    setMediaUrl(
                        "http://127.0.0.1:8000/" + selectedDocument.filepath
                    );

                    setStartTime(timestamp.start_time);
                }}
                >Play From Timestamp</button>

              </div>
            )
          )}

        </div>
      )}

      {mediaUrl && (
        <MediaPlayer mediaUrl={mediaUrl} startTime={startTime}/>
      )}

    </div>
  );
}


export default TimestampResults;