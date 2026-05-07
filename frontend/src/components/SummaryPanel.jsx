import { useState } from "react";

import api from "../api/client";

import DocumentSelector
from "./DocumentSelector";


function SummaryPanel() {

  // Selected document
  const [
    selectedDocument,
    setSelectedDocument,
  ] = useState(null);

  // Generated summary
  const [summary, setSummary] =
    useState("");

  // Loading state
  const [isLoading, setIsLoading] =
    useState(false);

  // generate summary
  async function generateSummary() {
    if (!selectedDocument) {

      alert(
        "Please select a document."
      );

      return;
    }

    setIsLoading(true);

    // Clear previous summary
    setSummary("");

    try {
      const response =
        await api.post(
          `/summary/${selectedDocument.id}`
        );

      // Store generated summary
      setSummary(
        response.data.summary
      );

    } catch (error) {

      console.error(error);

      setSummary(
        "Failed to generate summary."
      );

    } finally {

      setIsLoading(false);
    }
  }

  return (

    <div>

      <h2>Document Summary</h2>

      {/* Document selector */}
      <DocumentSelector
        selectedDocument={
          selectedDocument
        }

        setSelectedDocument={
          setSelectedDocument
        }
      />

      {/* Generate button */}
      <button
        type="button"
        onClick={generateSummary}
      >
        Generate Summary
      </button>

      {/* Loading state */}
      {isLoading && (
        <p>Generating summary...</p>
      )}

      {/* Render summary */}
      {summary && (

        <div>

          <h3>Summary</h3>

          <p>{summary}</p>

        </div>
      )}

    </div>
  );
}


export default SummaryPanel;