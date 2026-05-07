import { useState } from "react";

import api from "../api/client";

import DocumentSelector from "./DocumentSelector";


function ChatBox() {

  // Component state
  // User question input
  const [question, setQuestion] =
    useState("");

  // Selected document ID
  const [selectedDocument, setSelectedDocument] = useState(null);

  // Generated answer from backend
  const [answer, setAnswer] =
    useState("");

  // Loading state
  const [isLoading, setIsLoading] =
    useState(false);

  // Send question to backend
  async function askQuestion() {
    if (!question || !selectedDocument) {
      alert(
        "Question and document ID are required."
      );

      return;
    }

    setIsLoading(true);

    // Clear previous answer
    setAnswer("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/chat/stream",

      {
    method: "POST",
    headers: {
      "Content-Type":
        "application/json",
    },

    body: JSON.stringify({
      question,
      document_id:
        selectedDocument.id,
    }),
    }
  );


  const reader = response.body.getReader();

  const decoder = new TextDecoder();


  // Clear previous answer
  setAnswer("");

  // Read streamed chunks continuously
  while (true) {
    const {
      done,
      value,
    } = await reader.read();

    // Stream finished
    if (done) {
      break;
    }

  // Decode bytes -> text
  const chunk =
    decoder.decode(value);

  // Append streamed text
  setAnswer((prev) =>
    prev + chunk
  );
}

    } catch (error) {

      console.error(error);

      if (error.response) {
        setAnswer(error.response.data.detail || "Backend request failed.");
      } else {
        setAnswer("Network error.");
      }


    } finally {

      setIsLoading(false);
    }
  }


  // Component UI
  return (
    <div>

      <h2>Chat</h2>

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
        placeholder="Ask a question..."
        value={question}
        onChange={(event) =>
          setQuestion(
            event.target.value
          )
        }
      />

      {/* Submit button */}
      <button
        onClick={askQuestion}
        disabled={isLoading}
      >
        {isLoading ? "Generating..." : "Ask"}
      </button>

      {/* Loading state */}
      {isLoading && (
        <p>Generating answer...</p>
      )}

      {/* Render answer */}
      {answer && (
        <div className="answer-box">

          <h3>Answer</h3>

          <p>{answer}</p>

        </div>
      )}

    </div>
  );
}


export default ChatBox;