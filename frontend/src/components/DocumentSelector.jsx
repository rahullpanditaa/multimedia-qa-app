import { useEffect, useState } from "react";

import api from "../api/client";


function DocumentSelector({
  selectedDocument,
  setSelectedDocument,
}) {

  // Uploaded documents from backend
  const [documents, setDocuments] =
    useState([]);


  // fetch docs
  async function fetchDocuments() {

    try {

      const response =
        await api.get("/documents/");

      setDocuments(response.data);

    } catch (error) {

      console.error(
        "Failed to fetch documents:",
        error
      );
    }
  }


  // Load docs
  useEffect(() => {

    fetchDocuments();

  }, []);

  return (

    <div>

      <h3>Select Document</h3>

      <select
        value={selectedDocument?.id || ""}

        onChange={(event) => {
          const selectedId = Number(event.target.value);

          // Find matching doc object
          const document = documents.find((doc) => doc.id === selectedId);
        setSelectedDocument(
          document
        );
        }}
      >

        <option value="">
          -- Select Document --
        </option>

        {documents.map((document) => (

          <option
            key={document.id}
            value={document.id}
          >

            {document.filename}

          </option>
        ))}

      </select>

    </div>
  );
}


export default DocumentSelector;