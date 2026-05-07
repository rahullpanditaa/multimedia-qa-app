import { useState } from "react";

import api from "../api/client";

import DocumentSelector
from "./DocumentSelector";


function TimestampResults() {

  // Selected media doc
  const [
    selectedDocumentId,
    setSelectedDocumentId,
  ] = useState("");

  // User query
  const [question, setQuestion] =
    useState("");

  // Retrieved timestamps
  const [timestamps, setTimestamps] =
    useState([]);

  // Loading state
  const [isLoading, setIsLoading] =
    useState(false);

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
      !selectedDocumentId ||
      !question
    ) {

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
              selectedDocumentId
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
        selectedDocumentId={
          selectedDocumentId
        }

        setSelectedDocumentId={
          setSelectedDocumentId
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
                style={{
                  border:
                    "1px solid gray",

                  padding: "10px",

                  marginBottom: "10px",
                }}
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

              </div>
            )
          )}

        </div>
      )}

    </div>
  );
}


export default TimestampResults;