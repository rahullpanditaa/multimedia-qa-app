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

      // send chat request
      const response = await api.post(
        "/chat/",
        {
          question: question,

          // Convert string input -> int
          document_id: Number(selectedDocument.id)
        }
      );


      // Store response
      setAnswer(
        response.data.answer
      );

    } catch (error) {

      console.error(error);

      setAnswer(
        "Failed to generate answer."
      );

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
      >
        Ask
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