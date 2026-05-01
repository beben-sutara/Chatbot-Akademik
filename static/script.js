/* ============================================================
   Chatbot Akademik – client-side script
   ============================================================ */

(function () {
  "use strict";

  const messagesEl = document.getElementById("chatMessages");
  const inputEl = document.getElementById("userInput");
  const sendBtn = document.getElementById("sendBtn");
  const quickActions = document.getElementById("quickActions");

  // Set timestamp on initial bot message
  document.getElementById("initTime").textContent = formatTime(new Date());

  /* ---- Helpers ---- */

  function formatTime(date) {
    return date.toLocaleTimeString("id-ID", {
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  function escapeHtml(text) {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  /**
   * Convert simple markdown-like syntax to HTML.
   * Supports **bold** and newlines.
   */
  function formatMessage(text) {
    let html = escapeHtml(text);
    // Bold: **text**
    html = html.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    // Newlines
    html = html.replace(/\n/g, "<br />");
    return html;
  }

  /* ---- DOM helpers ---- */

  function appendMessage(role, text) {
    const wrapper = document.createElement("div");
    wrapper.className = `message ${role}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerHTML = formatMessage(text);

    const time = document.createElement("span");
    time.className = "time";
    time.textContent = formatTime(new Date());

    wrapper.appendChild(bubble);
    wrapper.appendChild(time);
    messagesEl.appendChild(wrapper);
    scrollToBottom();
    return wrapper;
  }

  function appendTypingIndicator() {
    const wrapper = document.createElement("div");
    wrapper.className = "message bot typing-indicator";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerHTML =
      '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';

    wrapper.appendChild(bubble);
    messagesEl.appendChild(wrapper);
    scrollToBottom();
    return wrapper;
  }

  function scrollToBottom() {
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  /* ---- Send flow ---- */

  async function sendMessage(text) {
    const message = (text || inputEl.value).trim();
    if (!message) return;

    inputEl.value = "";
    setSending(true);

    appendMessage("user", message);

    const typingEl = appendTypingIndicator();

    try {
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      const data = await res.json();

      typingEl.remove();

      if (res.ok && data.response) {
        appendMessage("bot", data.response);
      } else {
        appendMessage(
          "bot",
          "Maaf, terjadi kesalahan. Silakan coba lagi beberapa saat."
        );
      }
    } catch (err) {
      typingEl.remove();
      console.error("Chat error:", err.message || err);
      appendMessage(
        "bot",
        "Tidak dapat terhubung ke server. Periksa koneksi Anda."
      );
    } finally {
      setSending(false);
      inputEl.focus();
    }
  }

  function setSending(isSending) {
    sendBtn.disabled = isSending;
    inputEl.disabled = isSending;
  }

  /* ---- Event listeners ---- */

  sendBtn.addEventListener("click", () => sendMessage());

  inputEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Quick action buttons
  quickActions.querySelectorAll(".quick-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      sendMessage(btn.dataset.msg);
    });
  });
})();
