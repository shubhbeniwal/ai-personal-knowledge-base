"use client";

import { useState, useEffect, useRef } from "react";
import axios from "axios";

export default function Home() {

  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");

  const [question, setQuestion] = useState("");

  const [conversations, setConversations] = useState([]);

  const [currentConversationId, setCurrentConversationId] = useState(null);

  const [chatHistory, setChatHistory] = useState([]);

  const [streamingAnswer, setStreamingAnswer] = useState("");

  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  const [documents, setDocuments] = useState([]);

  const [selectedDocuments, setSelectedDocuments] = useState([]);

  const fileInputRef = useRef(null);

  useEffect(() => {

    const savedConversations =
      localStorage.getItem("memoryos_conversations");

    if (savedConversations) {

      const parsed =
        JSON.parse(savedConversations);

      setConversations(parsed);

      if (parsed.length > 0) {

        setCurrentConversationId(
          parsed[0].id
        );

        setChatHistory(
          parsed[0].messages
        );

      }

    }

  }, []);

  useEffect(() => {

    localStorage.setItem(
      "memoryos_conversations",
      JSON.stringify(conversations)
    );

  }, [conversations]);

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

      setTimeout(() => {

        setUploadStatus("");

      }, 3000);

      fetchDocuments();

      setFile(null);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }

      setTimeout(() => {
        setUploadStatus("");
      }, 3000);

    } catch (error) {

      console.error(error);

      setUploadStatus(
        "Upload Failed"
      );

      setTimeout(() => {

        setUploadStatus("");

      }, 3000);
    }
  };

  const askQuestion = async () => {

    if (!question.trim()) return;

    if (!currentConversationId) {

      const newConversation = {

        id: Date.now(),

        title: question.slice(0, 30),

        messages: []

      };

      setConversations((prev) => [
        newConversation,
        ...prev
      ]);

      setCurrentConversationId(
        newConversation.id
      );

    }

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

      const updatedMessages = [

        ...chatHistory,

        {
          question: userQuestion,
          answer: answerText,
          sources: sources
        }

      ];

      setChatHistory(
        updatedMessages
      );

      setConversations((prev) =>

        prev.map((conv) =>

          conv.id === currentConversationId

            ? {
                ...conv,
                messages: updatedMessages
              }

            : conv

        )

      );

      setStreamingAnswer("");

      setLoading(false);

    } catch (error) {

      console.error(error);

      alert("Failed to get answer");

      setLoading(false);

    }
  };

  const createNewChat = () => {

    const newConversation = {

      id: Date.now(),

      title: "New Chat",

      messages: []

    };

    const updatedConversations = [

      newConversation,

      ...conversations

    ];

    setConversations(
      updatedConversations
    );

    setCurrentConversationId(
      newConversation.id
    );

    setChatHistory([]);

  };

  const loadConversation = (conversation) => {

    setCurrentConversationId(
      conversation.id
    );

    setChatHistory(
      conversation.messages
    );

  };


  const deleteConversation = (id) => {

    const updated = conversations.filter(
      (conversation) =>
        conversation.id !== id
    );

    setConversations(updated);

    if (currentConversationId === id) {

      if (updated.length > 0) {

        setCurrentConversationId(
          updated[0].id
        );

        setChatHistory(
          updated[0].messages
        );

      } else {

        setCurrentConversationId(null);

        setChatHistory([]);

      }

    }

  };

  return (
    <>
      <div className="background-orb orb-1"></div>
      <div className="background-orb orb-2"></div>

      <main className="min-h-screen p-8">

        <div className="max-w-7xl mx-auto">

          {/* HEADER */}

          <div className="mb-10">

            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">

              <div>

                <h1 className="text-7xl font-black gradient-text mb-3 leading-[1.15] pb-2">
                  MemoryOS
                </h1>

                <p className="text-xl text-gray-400 max-w-3xl">
                  Your personal AI memory system.
                  Upload documents, store knowledge and retrieve information instantly.
                </p>  

              </div>

              <div className="glass rounded-3xl p-6 min-w-[260px]">

                <div className="text-sm text-gray-400 mb-3">
                  SYSTEM HEALTH
                </div>

                <div className="space-y-2">

                  <div className="flex items-center gap-2 text-green-400 font-medium">
                    <span
                      className="status-light bg-green-400"
                      style={{ animationDelay: "0s" }}
                    ></span>
                    Memory Engine Active
                  </div>

                  <div className="flex items-center gap-2 text-blue-400 font-medium">
                    <span
                      className="status-light bg-blue-400"
                      style={{ animationDelay: "0.4s" }}
                    ></span>
                    Vector Search Online
                  </div>

                  <div className="flex items-center gap-2 text-purple-400 font-medium">
                    <span
                      className="status-light bg-purple-400"
                      style={{ animationDelay: "0.8s" }}
                    ></span>
                    AI Ready
                  </div>

                </div>

              </div>

            </div>

            {/* STATUS PILLS */}

            <div className="memory-status mt-6">

              <div className="status-pill">
                🧠 {documents.length} Memories
              </div>

              <div className="status-pill">
                ⚡ AI Online
              </div>

              <div className="status-pill">
                🔍 Semantic Search
              </div>

              <div className="status-pill">
                📚 Knowledge Retrieval
              </div>

            </div>

          </div>

          {/* MAIN GRID */}

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">

            {/* LEFT PANEL */}
            <div className="lg:col-span-2 glass rounded-3xl p-5">

              <h3 className="font-bold text-xl mb-4">
                Conversations
              </h3>

              <button
                onClick={createNewChat}
                className="
                mb-6
                whitespace-nowrap
                h-fit
                px-4
                py-2
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
                + New Chat
              </button>

              <div className="space-y-2">

                {conversations.map((conversation) => (

                  <div
                    key={conversation.id}
                    className="flex items-center gap-2"
                  >

                    <button
                      onClick={() =>
                        loadConversation(conversation)
                      }
                      className={`
                        flex-1
                        text-left
                        p-3
                        rounded-xl
                        ${
                          currentConversationId === conversation.id
                            ? "bg-purple-600 text-white"
                            : "bg-white/5 hover:bg-white/10"
                        }
                      `}
                    >
                      {conversation.title}
                    </button>

                    <button
                      onClick={() =>
                        deleteConversation(
                          conversation.id
                        )
                      }
                      className="
                      w-9
                      h-9
                      rounded-xl
                      bg-red-500/20
                      hover:bg-red-500/40
                      "
                    >
                      🗑️
                    </button>

                  </div>

                ))}

              </div>

            </div>

            <div className="lg:col-span-3 glass rounded-3xl p-8">

              <h2 className="text-3xl font-bold mb-2">
                Memory Vault
              </h2>

              <p className="text-gray-400 mb-6">
                Connect documents to your AI memory.
              </p>

              {/* Upload Section */}

              <div className="mb-6">

                <label
                  className="
                    mb-6
                    cursor-pointer
                    flex
                    items-center
                    justify-center
                    rounded-2xl
                    border
                    border-white/10
                    bg-white/5
                    p-4
                    text-white
                    hover:bg-white/10
                    transition
                  "
                >

                  📄 {file ? file.name : "Choose Document"}

                  <input
                    ref={fileInputRef}
                    type="file"
                    className="hidden"
                    onChange={(e) =>
                      setFile(e.target.files[0])
                    }
                  />

                </label>

                <button
                  disabled={!file}
                  onClick={uploadFile}
                  className="
                  w-full
                  py-3
                  rounded-xl
                  bg-gradient-to-r
                  from-blue-500
                  to-purple-600
                  text-white
                  font-semibold
                  hover:scale-[1.02]
                  transition
                  "
                >
                  Add Memory
                </button>

                {uploadStatus && (

                  <div className="mt-4 text-green-400 text-sm whitespace-pre-line">
                    {uploadStatus}
                  </div>

                )}

              </div>

              {/* Documents */}

              <div>

                <h3 className="font-semibold text-blue-300 mb-4">
                  Connected Documents
                </h3>

                <div className="space-y-3">

                  {documents.map((doc, index) => (

                    <div
                      key={index}
                      className="
                      glass
                      rounded-xl
                      p-3
                      flex
                      justify-between
                      items-center
                      "
                    >

                      <div className="flex items-center gap-3">

                        <input
                          type="checkbox"
                          checked={selectedDocuments.includes(doc)}
                          onChange={() =>
                            toggleDocumentSelection(doc)
                          }
                        />

                        <span className="text-sm">
                          {doc}
                        </span>

                      </div>

                      <button
                        onClick={() =>
                          deleteDocument(doc)
                        }
                        className="
                        text-red-400
                        hover:text-red-300
                        text-sm
                        "
                      >
                        Delete
                      </button>

                    </div>

                  ))}

                </div>

              </div>

            </div>

            {/* RIGHT PANEL */}

            <div className="lg:col-span-7 glass rounded-3xl p-8">

              <div className="flex justify-between items-center mb-6">

                <div>

                  <h2 className="text-3xl font-bold">
                    AI Workspace
                  </h2>

                  <p className="text-gray-400">
                    Ask questions across your memory system.
                  </p>

                </div>

                <div className="status-pill">
                  ⚡ Context Aware
                </div>

              </div>

              {/* Input */}

              <textarea
                value={question}
                onChange={(e) =>
                  setQuestion(e.target.value)
                }

                onKeyDown={(e) => {

                if (
                  e.key === "Enter" &&
                  !e.shiftKey &&
                  question.trim()
                ) {

                  e.preventDefault();

                  askQuestion();

                }

              }}
                rows="4"
                placeholder="Ask a question..."
                className="
                w-full
                glass
                rounded-2xl
                p-4
                text-white
                placeholder-gray-500
                outline-none
                mb-4
                "
              />

              <button
                onClick={askQuestion}
                disabled={loading}
                className="
                px-6
                py-3
                rounded-xl
                bg-gradient-to-r
                from-purple-600
                to-pink-600
                text-white
                font-semibold
                hover:scale-[1.02]
                transition
                "
              >
                {loading ? "Generating..." : "Recall"}
              </button>

              {/* CHAT */}

              <div className="mt-8 space-y-5">

                {loading && (

                  <div className="glass rounded-2xl p-5">

                    <div className="typing-dots">
                      🧠 Thinking
                      <span>.</span>
                      <span>.</span>
                      <span>.</span>
                    </div>

                  </div>

                )}

                {streamingAnswer && (

                  <div className="glass rounded-2xl p-5">

                    <p className="font-bold text-purple-400 mb-2">
                      ⚡ MemoryOS
                    </p>

                    <p>
                      {streamingAnswer}
                    </p>

                  </div>

                )}

                {chatHistory.map((chat, index) => (

                  <div
                    key={index}
                    className="glass rounded-2xl p-5"
                  >

                    <div className="mb-4">

                      <p className="font-bold text-blue-400 mb-1">
                        👤 User
                      </p>

                      <p>
                        {chat.question}
                      </p>

                    </div>

                    <div>

                      <p className="font-bold text-purple-400 mb-1">
                        ⚡ MemoryOS
                      </p>

                      <p>
                        {chat.answer}
                      </p>

                    </div>

                    {chat.sources?.length > 0 && (

                      <div className="mt-4">

                        <p className="font-semibold mb-2">
                          Sources
                        </p>

                        {chat.sources.map((source, i) => (

                          <div
                            key={i}
                            className="text-sm text-gray-400"
                          >
                            📄 {source}
                          </div>

                        ))}

                      </div>

                    )}

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