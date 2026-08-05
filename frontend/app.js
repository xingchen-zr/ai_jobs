const chatForm = document.querySelector("#chatForm");
const questionInput = document.querySelector("#questionInput");
const sendButton = document.querySelector("#sendButton");
const chatMessages = document.querySelector("#chatMessages");
const apiEndpoint = document.querySelector("#apiEndpoint");
const clearChatButton = document.querySelector("#clearChat");

const STORAGE_KEY = "ai_jobs_frontend_messages";

function saveMessages() {
  const messages = [...chatMessages.querySelectorAll(".message")].map((node) => ({
    role: node.classList.contains("user") ? "user" : "assistant",
    content: node.querySelector(".bubble").innerText,
  }));
  localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
}

function restoreMessages() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return;

  try {
    const messages = JSON.parse(raw);
    if (!Array.isArray(messages) || messages.length === 0) return;

    chatMessages.innerHTML = "";
    for (const message of messages) {
      appendMessage(message.role, message.content);
    }
  } catch {
    localStorage.removeItem(STORAGE_KEY);
  }
}

function appendMessage(role, content, options = {}) {
  const article = document.createElement("article");
  article.className = `message ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "user" ? "你" : "AI";

  const bubble = document.createElement("div");
  bubble.className = options.error ? "bubble error" : "bubble";
  bubble.textContent = content;

  article.append(avatar, bubble);
  chatMessages.append(article);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  return bubble;
}

function setLoading(isLoading) {
  sendButton.disabled = isLoading;
  questionInput.disabled = isLoading;
  sendButton.textContent = isLoading ? "生成中" : "发送";
}

function autoResizeTextarea() {
  questionInput.style.height = "auto";
  questionInput.style.height = `${Math.min(questionInput.scrollHeight, 180)}px`;
}

async function askQuestion(question) {
  const endpoint = apiEndpoint.value.trim();
  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      human_question: question,
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`接口返回 ${response.status}：${text}`);
  }

  const data = await response.json();
  if (typeof data.answer === "string") {
    return data.answer;
  }

  if (typeof data === "string") {
    return data;
  }

  return JSON.stringify(data, null, 2);
}

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const question = questionInput.value.trim();
  if (!question) return;

  appendMessage("user", question);
  questionInput.value = "";
  autoResizeTextarea();
  setLoading(true);

  const loadingBubble = appendMessage("assistant", "正在检索职位并生成回答...");

  try {
    const answer = await askQuestion(question);
    loadingBubble.textContent = answer;
    saveMessages();
  } catch (error) {
    loadingBubble.classList.add("error");
    loadingBubble.textContent =
      "请求失败。请确认 FastAPI 服务已启动，并检查 Redis、Ollama、Chroma 和 DeepSeek 配置。\n\n" +
      String(error.message || error);
    saveMessages();
  } finally {
    setLoading(false);
    questionInput.focus();
  }
});

questionInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    chatForm.requestSubmit();
  }
});

questionInput.addEventListener("input", autoResizeTextarea);

document.querySelectorAll(".suggestion").forEach((button) => {
  button.addEventListener("click", () => {
    questionInput.value = button.dataset.question || "";
    autoResizeTextarea();
    questionInput.focus();
  });
});

clearChatButton.addEventListener("click", () => {
  localStorage.removeItem(STORAGE_KEY);
  chatMessages.innerHTML = "";
  appendMessage(
    "assistant",
    "你好，我可以基于本地职位向量库帮你检索和分析岗位。你可以直接问：帮我找适合 Python 和 RAG 的岗位。",
  );
});

restoreMessages();
autoResizeTextarea();
