"use client";

import { useState } from "react";
import axios from "axios";

export default function Home() {

  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");

  const [sources, setSources] = useState([]);

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

    } catch (error) {

      console.error(error);

      setUploadStatus(
        "Upload Failed"
      );
    }
  };

  const askQuestion = async () => {

  const response = await axios.post(
    "http://127.0.0.1:8000/ask",
    {
      question
    }
  );

  setAnswer(
    response.data.answer
  );

  setSources(
    response.data.sources
  );
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
              className="bg-green-600 text-white px-4 py-2 rounded"
            >
              Ask
            </button>
            
            
            <div className="mt-6">

              <h3 className="font-bold mb-2">
                Answer
              </h3>

              <p className="mb-4">
                {answer}
              </p>

              <h3 className="font-bold mb-2">
                Sources
              </h3>

              <ul>
                {
                  (sources || []).map(
                    (source, index) => (
                      <li key={index}>
                        {source}
                      </li>
                    )
                  )
                }
              </ul>

            </div>
            
          </div>

        </div>

      </div>

    </main>
  );
}