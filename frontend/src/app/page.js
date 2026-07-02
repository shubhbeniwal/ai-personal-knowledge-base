"use client";

import { useState, useEffect, useRef } from "react";
import axios from "axios";

export default function Home() {

  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");

  const [question, setQuestion] = useState("");

  const [chatHistory, setChatHistory] = useState([]);

  const [streamingAnswer, setStreamingAnswer] = useState("");

  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  const [documents, setDocuments] = useState([]);

  const [selectedDocuments, setSelectedDocuments] = useState([]);

  useEffect(() => {

    chatEndRef.current?.scrollIntoView({
      behavior: "smooth"
    });

  }, [chatHistory, streamingAnswer]);

  const fetchDocuments = async () => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:8000/documents"
      );

      setDocuments(
        response.data.documents
      );

    } catch (error) {

      console.error(error);

    }

  };

  const toggleDocumentSelection = (
    documentName
  ) => {

    setSelectedDocuments((prev) => {

      if (
        prev.includes(documentName)
      ) {

        return prev.filter(
          (doc) => doc !== documentName
        );

      }

      return [
        ...prev,
        documentName
      ];

    });

  };


  const deleteDocument = async (
    filename
  ) => {

    try {

      await axios.delete(
        `http://127.0.0.1:8000/documents/${filename}`
      );

      fetchDocuments();

    } catch (error) {

      console.error(error);

      alert(
        "Failed to delete document"
      );

    }

  };

  const uploadFile = async () => {

    console.log("Button clicked");
    console.log(file);

    if (!file) {
      alert("No file selected");
      return;
    }

    try {

      const formData = new FormData();

      formData.append(
        "file",
        file
      );

      const response = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      );

      setUploadStatus(
        `${response.data.message}
Chunks Stored: ${response.data.chunks_stored}`
      );

      fetchDocuments();

    } catch (error) {

      console.error(error);

      setUploadStatus(
        "Upload Failed"
      );
    }
  };

  const askQuestion = async () => {

    if (!question.trim()) return;

    setLoading(true);

    try {

      const userQuestion = question;

      setQuestion("");

      setStreamingAnswer("");

      const response = await fetch(
        "http://127.0.0.1:8000/ask-stream",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            question: userQuestion,
            selected_documents: selectedDocuments,
            chat_history: chatHistory
          })
        }
      );

      const reader =
        response.body.getReader();

      const decoder =
        new TextDecoder();

      let fullAnswer = "";

      while (true) {

        const {
          done,
          value
        } = await reader.read();

        if (done) break;

        const chunk =
          decoder.decode(value);

        fullAnswer += chunk;

        setStreamingAnswer(
          fullAnswer
        );

      }

      setChatHistory((prev) => [

        ...prev,

        {
          question: userQuestion,
          answer: fullAnswer,
          sources: []
        }

      ]);

      setStreamingAnswer("");

      setLoading(false);

    } catch (error) {

      console.error(error);

      alert("Failed to get answer");

      setLoading(false);

    }
  };

  return (
    <main className="min-h-screen bg-gray-100 p-8">

      <div className="max-w-6xl mx-auto">

        <h1 className="text-4xl font-bold mb-8">
          AI Personal Knowledge Base
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

          <div className="bg-white p-6 rounded-xl shadow">

            <h2 className="text-xl font-semibold mb-4">
              Upload Document
            </h2>

            <input
              type="file"
              onChange={(e) => {
                console.log(e.target.files[0]);
                setFile(e.target.files[0]);
              }}
              className="mb-4"
            />

            <button
              onClick={uploadFile}
              className="bg-blue-600 text-white px-4 py-2 rounded"
            >
              Upload
            </button>

            <p className="mt-4 text-green-600 whitespace-pre-line">
              {uploadStatus}
            </p>

            <div className="mt-6">

              <h3 className="font-bold mb-2">
                Uploaded Documents
              </h3>

              <ul className="list-disc ml-5">

                {documents.map(
                  (doc, index) => (

                    <li
                      key={index}
                      className="flex justify-between items-center mb-2"
                    >

                      <div className="flex items-center gap-2">

                        <input
                          type="checkbox"
                          checked={
                            selectedDocuments.includes(doc)
                          }
                          onChange={() =>
                            toggleDocumentSelection(doc)
                          }
                        />

                        <span>
                          {doc}
                        </span>

                      </div>

                      <button
                        onClick={() =>
                          deleteDocument(doc)
                        }
                        className="bg-red-500 text-white px-2 py-1 rounded text-sm"
                      >
                        Delete
                      </button>

                    </li>

                  )
                )}

              </ul>

            </div>

          </div>

          <div className="md:col-span-2 bg-white p-6 rounded-xl shadow">

            <h2 className="text-xl font-semibold mb-4">
              Ask Questions
            </h2>

            <textarea
              value={question}
              onChange={(e) =>
                setQuestion(e.target.value)
              }
              className="w-full border p-3 rounded mb-4"
              rows="4"
              placeholder="Ask a question..."
            />

            <button
              onClick={askQuestion}
              disabled={loading}
              className="bg-green-600 text-white px-4 py-2 rounded"
            >
              {loading ? "Generating..." : "Ask"}
            </button>

            <div className="mt-8 space-y-6">

              {streamingAnswer && (

                <div
                  className="
                    border
                    rounded-lg
                    p-4
                    bg-yellow-50
                  "
                >

                  <p className="font-bold text-green-700">
                    AI
                  </p>

                  <p>
                    {streamingAnswer}
                  </p>

                </div>

              )}

              {loading && (

                <div className="border rounded-lg p-4 bg-yellow-50">

                  <p className="font-bold text-green-700">
                    AI
                  </p>

                  <p>
                    Typing...
                  </p>

                </div>

              )}

              {chatHistory.map((chat, index) => (

                <div
                  key={index}
                  className="border rounded-lg p-4 bg-gray-50"
                >

                  <div className="mb-3">

                    <p className="font-bold text-blue-700">
                      You
                    </p>

                    <p>
                      {chat.question}
                    </p>

                  </div>

                  <div>

                    <p className="font-bold text-green-700">
                      AI
                    </p>

                    <p className="mb-3">
                      {chat.answer}
                    </p>

                    <div>

                      {chat.sources?.length > 0 && (

                        <div className="mt-3">

                          <p className="font-semibold mb-2">
                            Sources
                          </p>

                          <ul className="space-y-1">

                            {chat.sources.map(
                              (source, i) => (

                                <li
                                  key={i}
                                  className="text-sm text-gray-700"
                                >
                                  📄 {source}
                                </li>

                              )
                            )}

                          </ul>

                        </div>

                      )}

                    </div>

                  </div>

                </div>

              ))}

              <div ref={chatEndRef}></div>

            </div>

          </div>

        </div>

      </div>

    </main>
  );
}