import { useEffect, useState } from "react";

import api from "../api/client";


function DocumentSelector({
  selectedDocumentId,
  setSelectedDocumentId,
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
        value={selectedDocumentId}

        onChange={(event) =>
          setSelectedDocumentId(
            event.target.value
          )
        }
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