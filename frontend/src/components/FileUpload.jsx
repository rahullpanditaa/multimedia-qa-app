import { useState } from "react";

import api from "../api/client";


function FileUpload() {

  console.log("COMPONENT RENDER")

  // Component state

  // Stores currently selected file.
  // Initially no file selected.
  const [selectedFile, setSelectedFile] = useState(null);

  // Loading state during upload.
  const [isUploading, setIsUploading] = useState(false);

  // Success/error feedback message.
  const [message, setMessage] = useState("");


  // handle fle selection
  function handleFileChange(event) {

    // event.target.files is a FileList
    // only allow one file for now
    const file = event.target.files[0];

    setSelectedFile(file);
  }


  // need to determine backend endpoint
  function getUploadEndpoint(file) {

    // PDFs use document ingestion endpoint.
    if (file.type === "application/pdf") {
      return "/documents/upload";
    }

    // Audio/video files use media endpoint.
    if (
      file.type.startsWith("audio") ||
      file.type.startsWith("video")
    ) {
      return "/media/upload";
    }

    // Unsupported file type.
    return null;
  }


  // handle file upload
  async function handleUpload() {

    // debug logging (upload happening in backend - ui shows failed)
    console.log("HANDLE UPLOAD RUNNING NOW")

    // Basic validation.
    if (!selectedFile) {
      alert("Please select a file.");
      return;
    }

    // Determine backend route.
    const endpoint = getUploadEndpoint(selectedFile);

    // Reject unsupported file types.
    if (!endpoint) {
      alert("Unsupported file type.");
      return;
    }

    setIsUploading(true);

    // Clear previous messages.
    setMessage("");

    try {

      // create multipart form data
      const formData = new FormData();

      formData.append(
        "file",
        selectedFile
      );


      // Send upload request
      const response = await api.post(
        endpoint,
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      );

      // debugging
      console.log("Upload response:", response.data)
      // success message
      setMessage(response.data.message || "Upload successful.");

    } catch (error) {

      console.error(error);

      setMessage(
        "File upload failed."
      );

    } finally {

      setIsUploading(false);
    }
  }


  // Component ui
  return (
    <div>

      <h2>Upload File</h2>

      {/* File picker */}
      <input
        type="file"
        onChange={handleFileChange}
      />

      {/* Upload button */}
      <button type="button"
        onClick={handleUpload}
      >
        Upload
      </button>

      {/* Loading state */}
      {isUploading && (
        <p>Uploading...</p>
      )}

      {/* Response message */}
      {message && (
        <p>{message}</p>
      )}

    </div>
  );
}


export default FileUpload;