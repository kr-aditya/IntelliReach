import { useRef, useState } from "react";
import {
  uploadDocument,
  askQuestion,
} from "../services/api";

function KnowledgeBase() {
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");
  const [uploadError, setUploadError] = useState("");

  const [question, setQuestion] = useState("");
  const [asking, setAsking] = useState(false);
  const [answer, setAnswer] = useState(null);
  const [askError, setAskError] = useState("");

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    setUploadMessage("");
    setUploadError("");

    if (!file) {
      setSelectedFile(null);
      return;
    }

    const fileName = file.name.toLowerCase();

    const isSupported =
      fileName.endsWith(".pdf") ||
      fileName.endsWith(".txt");

    if (!isSupported) {
      setSelectedFile(null);

      setUploadError(
        "Unsupported file type. Please select a PDF or TXT file."
      );

      event.target.value = "";
      return;
    }

    const maxFileSize = 10 * 1024 * 1024;

    if (file.size > maxFileSize) {
      setSelectedFile(null);

      setUploadError(
        "File is too large. Maximum supported size is 10 MB."
      );

      event.target.value = "";
      return;
    }

    if (file.size === 0) {
      setSelectedFile(null);

      setUploadError(
        "The selected file is empty."
      );

      event.target.value = "";
      return;
    }

    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile || uploading) {
      return;
    }

    setUploading(true);
    setUploadMessage("");
    setUploadError("");

    try {
      const data = await uploadDocument(
        selectedFile
      );

      setUploadMessage(
        `${data.filename} uploaded successfully. ${data.chunks_stored} knowledge chunks stored.`
      );

      setSelectedFile(null);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    } catch (requestError) {
      console.error(
        "Document upload failed:",
        requestError
      );

      setUploadError(
        requestError.message ||
          "Something went wrong while uploading the document."
      );
    } finally {
      setUploading(false);
    }
  };

  const handleAsk = async (event) => {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || asking) {
      return;
    }

    setAsking(true);
    setAskError("");
    setAnswer(null);

    try {
      const result = await askQuestion(
        trimmedQuestion
      );

      setAnswer(result);
    } catch (requestError) {
      console.error(
        "Question request failed:",
        requestError
      );

      setAskError(
        requestError.message ||
          "Something went wrong while answering the question."
      );
    } finally {
      setAsking(false);
    }
  };

  return (
    <section className="knowledge-section">
      <div className="knowledge-heading">
        <p className="eyebrow">
          COMPANY KNOWLEDGE BASE
        </p>

        <h2>
          Ask questions about your documents
        </h2>

        <p>
          Upload company documents to build a
          searchable knowledge base, then ask
          questions using grounded AI answers.
        </p>
      </div>

      <div className="knowledge-grid">

        {/* Upload */}
        <article className="knowledge-card">
          <div className="knowledge-card-header">
            <div>
              <div className="card-label">
                DOCUMENT INGESTION
              </div>

              <h3>Add company knowledge</h3>
            </div>

            <span className="knowledge-icon">
              ↑
            </span>
          </div>

          <label className="upload-box">
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.txt,application/pdf,text/plain"
              onChange={handleFileChange}
            />

            <span className="upload-icon">
              ↑
            </span>

            <strong>
              {selectedFile
                ? selectedFile.name
                : "Choose a PDF or TXT file"}
            </strong>

            <span>
              {selectedFile
                ? `${(
                    selectedFile.size /
                    1024 /
                    1024
                  ).toFixed(2)} MB`
                : "Maximum file size: 10 MB"}
            </span>
          </label>

          <button
            className="upload-button"
            onClick={handleUpload}
            disabled={!selectedFile || uploading}
          >
            {uploading
              ? "Uploading..."
              : "Upload Document"}
          </button>

          {uploadMessage && (
            <div className="success-message">
              ✓ {uploadMessage}
            </div>
          )}

          {uploadError && (
            <div className="upload-error">
              {uploadError}
            </div>
          )}
        </article>

        {/* Ask */}
        <article className="knowledge-card">
          <div className="knowledge-card-header">
            <div>
              <div className="card-label">
                KNOWLEDGE Q&A
              </div>

              <h3>Ask your documents</h3>
            </div>

            <span className="knowledge-icon">
              ?
            </span>
          </div>

          <form onSubmit={handleAsk}>
            <textarea
              className="question-input"
              placeholder="What does this company do?"
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
              maxLength={500}
              disabled={asking}
            />

            <div className="question-footer">
              <span>
                {question.length}/500
              </span>

              <button
                type="submit"
                className="ask-button"
                disabled={
                  !question.trim() || asking
                }
              >
                {asking
                  ? "Thinking..."
                  : "Ask Question"}

                {!asking && <span>→</span>}
              </button>
            </div>
          </form>

          {askError && (
            <div className="upload-error">
              {askError}
            </div>
          )}

          {answer && (
            <div className="answer-box">
              <div className="answer-label">
                ANSWER
              </div>

              <p>{answer.answer}</p>

              {answer.sources?.length > 0 && (
                <div className="sources">
                  <div className="answer-label">
                    SOURCES
                  </div>

                  {answer.sources.map(
                    (source, index) => (
                      <div
                        className="source-item"
                        key={index}
                      >
                        {source}
                      </div>
                    )
                  )}
                </div>
              )}
            </div>
          )}
        </article>

      </div>
    </section>
  );
}

export default KnowledgeBase;