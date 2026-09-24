/**
 * CampusMind AI - Frontend Application Controller
 * Handles conversation flows, speech recognition/synthesis, analytics modal, and themes.
 */

// State
let sessionId = localStorage.getItem("campusmind_session_id");
if (!sessionId) {
  sessionId = "sess_" + Math.random().toString(36).substring(2, 10);
  localStorage.setItem("campusmind_session_id", sessionId);
}

let isRecording = false;
let recognition = null;
let speechSynth = window.speechSynthesis || null;

// DOM Elements
const messagesContainer = document.getElementById("chatMessages");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const voiceBtn = document.getElementById("voiceBtn");
const suggestionsArea = document.getElementById("suggestionsArea");
const themeToggleBtn = document.getElementById("themeToggleBtn");
const analyticsBtn = document.getElementById("analyticsBtn");
const newChatBtn = document.getElementById("newChatBtn");
const analyticsModal = document.getElementById("analyticsModal");
const closeModalBtn = document.getElementById("closeModalBtn");

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initSpeechRecognition();
  bindEvents();
  renderInitialGreeting();
});

function initTheme() {
  const savedTheme = localStorage.getItem("campusmind_theme") || "dark";
  document.documentElement.setAttribute("data-theme", savedTheme);
  updateThemeIcon(savedTheme);
}

function updateThemeIcon(theme) {
  if (themeToggleBtn) {
    themeToggleBtn.innerHTML = theme === "dark" ? "☀️" : "🌙";
  }
}

function bindEvents() {
  sendBtn.addEventListener("click", handleSendMessage);
  
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  });

  themeToggleBtn.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("campusmind_theme", next);
    updateThemeIcon(next);
  });

  if (voiceBtn) {
    voiceBtn.addEventListener("click", toggleVoiceDictation);
  }

  if (newChatBtn) {
    newChatBtn.addEventListener("click", startNewSession);
  }

  if (analyticsBtn) {
    analyticsBtn.addEventListener("click", openAnalyticsModal);
  }

  if (closeModalBtn) {
    closeModalBtn.addEventListener("click", () => analyticsModal.classList.remove("open"));
  }

  window.addEventListener("click", (e) => {
    if (e.target === analyticsModal) {
      analyticsModal.classList.remove("open");
    }
  });

  // Topic buttons in sidebar
  document.querySelectorAll(".topic-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const prompt = btn.getAttribute("data-prompt");
      if (prompt) {
        sendDirectMessage(prompt);
      }
    });
  });
}

function initSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    if (voiceBtn) voiceBtn.style.display = "none";
    return;
  }

  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = "en-US";

  recognition.onstart = () => {
    isRecording = true;
    voiceBtn.classList.add("recording");
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    chatInput.value = transcript;
    handleSendMessage();
  };

  recognition.onerror = (event) => {
    console.warn("Speech recognition error:", event.error);
    stopRecording();
  };

  recognition.onend = () => {
    stopRecording();
  };
}

function toggleVoiceDictation() {
  if (!recognition) return;
  if (isRecording) {
    recognition.stop();
    stopRecording();
  } else {
    try {
      recognition.start();
    } catch (e) {
      console.warn("Speech recognition start failed:", e);
    }
  }
}

function stopRecording() {
  isRecording = false;
  if (voiceBtn) voiceBtn.classList.remove("recording");
}

function renderInitialGreeting() {
  const initialBotMessage = (
    "Hello! 👋 I'm **CampusMind AI**, your comprehensive college and academic assistant. " +
    "I can help you review **course syllabi**, check **exam schedules**, explain **CGPA and grading policies**, " +
    "find **faculty contacts**, and navigate **campus services**.\n\n" +
    "What would you like to explore today?"
  );
  
  appendMessage("bot", initialBotMessage, {
    confidence: 1.0,
    intent: "welcome",
    latency: 12
  });

  renderSuggestions([
    "Show course list",
    "When are the exams?",
    "How is CGPA calculated?",
    "Library timings",
    "Syllabus for CS201"
  ]);
}

function handleSendMessage() {
  const text = chatInput.value.trim();
  if (!text) return;

  chatInput.value = "";
  sendDirectMessage(text);
}

function sendDirectMessage(message) {
  appendMessage("user", message);
  showTypingIndicator();
  clearSuggestions();

  fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: message, session_id: sessionId })
  })
    .then((res) => res.json())
    .then((data) => {
      removeTypingIndicator();
      if (data.error) {
        appendMessage("bot", "⚠️ Sorry, an error occurred while processing your request.");
        return;
      }

      appendMessage("bot", data.response, {
        confidence: data.confidence,
        intent: data.intent,
        latency: data.latency_ms,
        messageId: data.message_id
      });

      if (data.suggestions && data.suggestions.length > 0) {
        renderSuggestions(data.suggestions);
      }
    })
    .catch((err) => {
      removeTypingIndicator();
      console.error(err);
      appendMessage("bot", "⚠️ Network error connecting to CampusMind AI server.");
    });
}

function appendMessage(sender, text, meta = null) {
  const row = document.createElement("div");
  row.className = `message-row ${sender}`;

  const avatar = document.createElement("div");
  avatar.className = `avatar ${sender}`;
  avatar.textContent = sender === "bot" ? "🎓" : "👤";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = parseMarkdown(text);

  if (sender === "bot" && meta) {
    const metaContainer = document.createElement("div");
    metaContainer.className = "message-meta";

    const badge = document.createElement("span");
    badge.className = "confidence-badge";
    badge.innerHTML = `⚡ ${meta.latency || 15}ms • Intent: ${meta.intent || "general"} (${Math.round((meta.confidence || 0.9) * 100)}%)`;
    metaContainer.appendChild(badge);

    // Speak Button
    const speakBtn = document.createElement("button");
    speakBtn.className = "feedback-btn";
    speakBtn.innerHTML = "🔊";
    speakBtn.title = "Read aloud";
    speakBtn.onclick = () => speakText(text);
    metaContainer.appendChild(speakBtn);

    // Feedback Thumbs Up / Down
    const actions = document.createElement("div");
    actions.className = "feedback-actions";

    const upBtn = document.createElement("button");
    upBtn.className = "feedback-btn";
    upBtn.innerHTML = "👍";
    upBtn.title = "Helpful";
    upBtn.onclick = () => sendFeedback("positive", upBtn);

    const downBtn = document.createElement("button");
    downBtn.className = "feedback-btn";
    downBtn.innerHTML = "👎";
    downBtn.title = "Not helpful";
    downBtn.onclick = () => sendFeedback("negative", downBtn);

    actions.appendChild(upBtn);
    actions.appendChild(downBtn);
    metaContainer.appendChild(actions);

    bubble.appendChild(metaContainer);
  }

  row.appendChild(avatar);
  row.appendChild(bubble);
  messagesContainer.appendChild(row);
  scrollToBottom();
}

function showTypingIndicator() {
  const existing = document.getElementById("typingRow");
  if (existing) return;

  const row = document.createElement("div");
  row.className = "message-row bot";
  row.id = "typingRow";

  const avatar = document.createElement("div");
  avatar.className = "avatar bot";
  avatar.textContent = "🎓";

  const bubble = document.createElement("div");
  bubble.className = "bubble typing-bubble";
  bubble.innerHTML = `
    <span class="typing-dot"></span>
    <span class="typing-dot"></span>
    <span class="typing-dot"></span>
  `;

  row.appendChild(avatar);
  row.appendChild(bubble);
  messagesContainer.appendChild(row);
  scrollToBottom();
}

function removeTypingIndicator() {
  const typing = document.getElementById("typingRow");
  if (typing) typing.remove();
}

function renderSuggestions(suggestions) {
  clearSuggestions();
  suggestions.forEach((text) => {
    const chip = document.createElement("button");
    chip.className = "suggestion-chip";
    chip.innerHTML = `✨ ${text}`;
    chip.onclick = () => sendDirectMessage(text);
    suggestionsArea.appendChild(chip);
  });
}

function clearSuggestions() {
  suggestionsArea.innerHTML = "";
}

function scrollToBottom() {
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function speakText(rawText) {
  if (!speechSynth) return;
  speechSynth.cancel();
  // Strip markdown symbols
  const plainText = rawText.replace(/[#*`_•]/g, " ").replace(/\s+/g, " ");
  const utterance = new SpeechSynthesisUtterance(plainText);
  utterance.rate = 1.0;
  speechSynth.speak(utterance);
}

function sendFeedback(rating, btnElement) {
  btnElement.style.color = rating === "positive" ? "#10b981" : "#ef4444";
  btnElement.style.transform = "scale(1.2)";

  fetch("/api/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, rating: rating })
  }).catch((e) => console.warn("Feedback failed:", e));
}

function startNewSession() {
  sessionId = "sess_" + Math.random().toString(36).substring(2, 10);
  localStorage.setItem("campusmind_session_id", sessionId);
  messagesContainer.innerHTML = "";
  renderInitialGreeting();
}

function openAnalyticsModal() {
  fetch("/api/analytics")
    .then((res) => res.json())
    .then((data) => {
      const runtime = data.runtime || {};
      const db = data.database || {};
      document.getElementById("statTotalQueries").textContent = runtime.total_queries || 0;
      document.getElementById("statAvgLatency").textContent = (runtime.average_latency_ms || 18) + "ms";
      document.getElementById("statSatisfaction").textContent = (runtime.satisfaction_rate || 100) + "%";

      analyticsModal.classList.add("open");
    })
    .catch((err) => console.error(err));
}

/** Simple Markdown formatting for display */
function parseMarkdown(text) {
  if (!text) return "";
  let html = text
    .replace(/### (.*?)\n/g, "<h3>$1</h3>")
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\n\n/g, "</p><p>")
    .replace(/\n• (.*?)(?=\n|$)/g, "<li>$1</li>");

  html = html.replace(/(<li>.*?<\/li>)/g, "<ul>$1</ul>");
  return `<p>${html}</p>`;
}
