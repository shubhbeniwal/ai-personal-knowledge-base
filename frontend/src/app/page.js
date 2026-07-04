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

  const [aiStatus, setAiStatus] = useState("Ready");

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
      let sources = [];

      while (true) {

        const {
          done,
          value
        } = await reader.read();

        if (done) break;

        const chunk =
          decoder.decode(value);

        fullAnswer += chunk;

        const visibleText =
          fullAnswer.split("[SOURCES]")[0];

        setStreamingAnswer(
          visibleText
        );

      }

      const parts =
        fullAnswer.split("[SOURCES]");

      const answerText =
        parts[0].trim();

      if (parts.length > 1) {

        sources = parts[1]
          .split("\n")
          .map((s) => s.trim())
          .filter(Boolean);

      }

      setChatHistory((prev) => [

        ...prev,

        {
          question: userQuestion,
          answer: answerText,
          sources: sources
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
    <>
      <div className="background-orb orb-1"></div>
      <div className="background-orb orb-2"></div>
        
      <main className="min-h-screen p-8">

        <div className="max-w-6xl mx-auto">

          <div className="mb-10">

            <h1 className="text-7xl font-extrabold gradient-text mb-3">
              MemoryOS
            </h1>

            <p className="text-gray-400 text-xl mb-6">
              Your second brain powered by AI.
            </p>

            <div className="memory-status">

              <div className="status-pill">
                🧠 Memory Engine Online
              </div>

              <div className="status-pill">
                📚 {documents.length} Memories Loaded
              </div>

              <div className="status-pill">
                ⚡ AI Ready
              </div>

            </div>

          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

            <div className="
            glass
            p-8
            rounded-3xl
            border
            border-white/10
            shadow-2xl
            ">

              <h2 className="text-2xl font-bold mb-4 text-white">
                Memory Vault
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
                className="
                px-5
                py-3
                rounded-xl
                bg-gradient-to-r
                from-blue-500
                to-purple-600
                text-white
                font-semibold
                hover:scale-105
                transition
                "
              >
                Add Memory
              </button>

              <p className="mt-4 text-green-600 whitespace-pre-line">
                {uploadStatus}
              </p>

              <div className="mt-6">

                <h3 className="font-bold mb-3 text-blue-300">
                  Your Memories
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

            <div className="
            md:col-span-2
            glass
            p-8
            rounded-3xl
            shadow-2xl
            border
            border-white/10
            ">

              <h2 className="text-2xl font-bold mb-4 text-white">
                Talk To Your AI Memory
              </h2>

              <textarea
                value={question}
                onChange={(e) =>
                  setQuestion(e.target.value)
                }
                className="
                w-full
                glass
                p-4
                rounded-2xl
                mb-4
                text-white
                placeholder-gray-400
                outline-none
                "
                rows="4"
                placeholder="Ask a question..."
              />

              <button
                onClick={askQuestion}
                disabled={loading}
                className="
                px-5
                py-3
                rounded-xl
                bg-gradient-to-r
                from-purple-600
                to-pink-600
                text-white
                font-semibold
                hover:scale-105
                transition
                "
              >
                {loading ? "Generating..." : "Recall"}
              </button>

              <div className="mt-8 space-y-6">

                {streamingAnswer && (

                  <div
                    className="
                      glass
                      rounded-2xl
                      p-5
                      border
                      border-white/10
                    "
                  >

                    <p className="font-bold text-green-700">
                      ⚡ MemoryOS
                    </p>

                    <p>
                      {streamingAnswer}
                    </p>

                  </div>

                )}

                {loading && (

                  <div className="
                  glass
                  rounded-2xl
                  p-5
                  border
                  border-white/10
                  ">

                    <p className="font-bold text-green-700">
                      AI
                    </p>

                    <p>
                      <div className="typing-dots">
                        🧠 Thinking
                        <span>.</span>
                        <span>.</span>
                        <span>.</span>
                      </div>
                    </p>

                  </div>

                )}

                {chatHistory.map((chat, index) => (

                  <div
                    key={index}
                    className="
                    glass
                    rounded-2xl
                    p-5
                    border
                    border-white/10
                    "
                  >

                    <div className="mb-3">

                      <p className="font-bold text-blue-700">
                        🧍 User
                      </p>

                      <p>
                        {chat.question}
                      </p>

                    </div>

                    <div>

                      <p className="font-bold text-green-700">
                        ⚡ MemoryOS
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
    </>
    );
}