<template>
  <div class="business-clarity-chat">
    <div class="chat-header">
      <button class="back-button" @click="$emit('back')">← Zurück</button>
      <div class="header-content">
        <h2>💼 Business Clarity Coach</h2>
        <p class="session-info">Session {{ sessionInfo.session_count }} | {{ sessionInfo.decisions_discussed.length }} Themen erkundet</p>
      </div>
    </div>

    <div class="chat-messages" ref="messagesContainer">
      <div class="welcome-message" v-if="messages.length === 0">
        <h3>Willkommen bei Business Clarity</h3>
        <p>Ich helfe dir, Klarheit über Geschäftsentscheidungen und Automatisierungsstrategien durch gezielte Fragen zu gewinnen.</p>
        <p>Teile deine geschäftliche Herausforderung, und ich helfe dir, systematisch durchzudenken.</p>
        <div class="topic-selector">
          <label>Themenbereich (optional):</label>
          <select v-model="currentTopic">
            <option value="general">Allgemein</option>
            <option value="automation">Automatisierung</option>
            <option value="strategy">Strategie</option>
            <option value="operations">Betrieb</option>
            <option value="growth">Wachstum</option>
          </select>
        </div>
        <div class="decisions" v-if="sessionInfo.decisions_discussed && sessionInfo.decisions_discussed.length > 0">
          <strong>Bisherige Themen:</strong>
          <span v-for="decision in sessionInfo.decisions_discussed" :key="decision" class="decision-tag">{{ decision }}</span>
        </div>
      </div>

      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.role]"
      >
        <div class="message-content">
          <div v-if="message.role === 'user'">
            <div class="topic-badge" v-if="message.topic">{{ message.topic }}</div>
            {{ message.content }}
          </div>
          <div v-else class="ai-response">
            <div class="question">{{ message.content.question }}</div>
            <div class="insight" v-if="message.content.insight">
              💡 {{ message.content.insight }}
            </div>
            <div class="next-step" v-if="message.content.next_step">
              📍 Nächster Schritt: {{ message.content.next_step }}
            </div>
          </div>
        </div>
      </div>

      <div v-if="isLoading" class="message assistant loading">
        <div class="message-content">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>

    <div class="chat-input">
      <textarea
        v-model="userInput"
        @keydown.enter.exact.prevent="sendMessage"
        placeholder="Beschreibe deine geschäftliche Herausforderung... (Enter zum Senden, Shift+Enter für neue Zeile)"
        rows="3"
      ></textarea>
      <button @click="sendMessage" :disabled="!userInput.trim() || isLoading">
        Senden
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

const emit = defineEmits(['back'])

const messages = ref([])
const userInput = ref('')
const isLoading = ref(false)
const messagesContainer = ref(null)
const currentTopic = ref('general')
const sessionInfo = ref({
  session_count: 0,
  decisions_discussed: [],
  business_context: {}
})

const userId = 'demo_user'

onMounted(async () => {
  await loadSessionInfo()
})

async function loadSessionInfo() {
  try {
    const response = await fetch(`http://127.0.0.1:8000/business-clarity/session/${userId}`)
    if (response.ok) {
      sessionInfo.value = await response.json()
    }
  } catch (error) {
    console.error('Failed to load session info:', error)
  }
}

async function sendMessage() {
  if (!userInput.value.trim() || isLoading.value) return

  const messageText = userInput.value.trim()
  const topic = currentTopic.value

  // Add user message
  messages.value.push({
    role: 'user',
    content: messageText,
    topic: topic
  })

  userInput.value = ''
  isLoading.value = true

  await nextTick()
  scrollToBottom()

  try {
    const response = await fetch('http://127.0.0.1:8000/business-clarity', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: userId,
        message: messageText,
        topic: topic
      })
    })

    if (!response.ok) {
      throw new Error('Failed to get response')
    }

    const data = await response.json()

    // Add AI response
    messages.value.push({
      role: 'assistant',
      content: {
        question: data.question,
        insight: data.insight,
        next_step: data.next_step
      }
    })

    // Update session info
    sessionInfo.value.session_count = data.session_number

    await nextTick()
    scrollToBottom()

  } catch (error) {
    console.error('Error sending message:', error)
    messages.value.push({
      role: 'assistant',
      content: {
        question: 'Entschuldigung, es ist ein Fehler aufgetreten. Bitte versuche es erneut.',
        insight: '',
        next_step: ''
      }
    })
  } finally {
    isLoading.value = false
  }
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}
</script>

<style scoped>
.business-clarity-chat {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 900px;
  margin: 0 auto;
  background: #f7fafc;
}

.chat-header {
  background: white;
  padding: 1.5rem;
  border-bottom: 2px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.back-button {
  background: #f7fafc;
  border: 1px solid #cbd5e0;
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
}

.back-button:hover {
  background: #e2e8f0;
}

.header-content {
  flex: 1;
}

.header-content h2 {
  margin: 0;
  font-size: 1.75rem;
  color: #1a202c;
}

.session-info {
  margin: 0.25rem 0 0 0;
  color: #718096;
  font-size: 0.9rem;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.welcome-message {
  background: white;
  border: 2px solid #c6f6d5;
  border-radius: 1rem;
  padding: 2rem;
  text-align: center;
}

.welcome-message h3 {
  color: #276749;
  margin: 0 0 1rem 0;
}

.welcome-message p {
  color: #4a5568;
  line-height: 1.6;
  margin: 0.5rem 0;
}

.topic-selector {
  margin: 1.5rem 0 1rem 0;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.topic-selector label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2d3748;
}

.topic-selector select {
  padding: 0.5rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
}

.decisions {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.decision-tag {
  display: inline-block;
  background: #edf2f7;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.85rem;
  margin: 0.25rem;
  color: #2d3748;
}

.message {
  display: flex;
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  justify-content: flex-end;
}

.message.assistant {
  justify-content: flex-start;
}

.message-content {
  max-width: 80%;
  padding: 1rem 1.5rem;
  border-radius: 1rem;
  line-height: 1.6;
}

.message.user .message-content {
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
  color: white;
}

.topic-badge {
  display: inline-block;
  background: rgba(255, 255, 255, 0.3);
  padding: 0.25rem 0.5rem;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  font-weight: 600;
}

.message.assistant .message-content {
  background: white;
  border: 1px solid #e2e8f0;
  color: #1a202c;
}

.ai-response .question {
  font-size: 1rem;
  margin-bottom: 0.75rem;
  font-weight: 500;
}

.ai-response .insight {
  background: #fef5e7;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  color: #744210;
  margin-top: 0.75rem;
}

.ai-response .next-step {
  background: #e6fffa;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.85rem;
  color: #234e52;
  margin-top: 0.75rem;
}

.typing-indicator {
  display: flex;
  gap: 0.5rem;
  padding: 0.5rem;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #cbd5e0;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.7;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

.chat-input {
  background: white;
  padding: 1.5rem;
  border-top: 2px solid #e2e8f0;
  display: flex;
  gap: 1rem;
}

.chat-input textarea {
  flex: 1;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 0.75rem;
  font-size: 1rem;
  font-family: inherit;
  resize: none;
  transition: border-color 0.2s;
}

.chat-input textarea:focus {
  outline: none;
  border-color: #48bb78;
}

.chat-input button {
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
  color: white;
  border: none;
  border-radius: 0.75rem;
  padding: 0.75rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.chat-input button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(72, 187, 120, 0.4);
}

.chat-input button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
