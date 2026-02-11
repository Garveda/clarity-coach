<template>
  <div class="domain-selector">
    <h1 class="title">🎓 Clarity Coach</h1>
    <p class="subtitle">Wähle deinen Coaching-Bereich</p>

    <div class="domains">
      <button
        v-for="domain in domains"
        :key="domain.id"
        class="domain-card"
        :class="{ active: currentDomain === domain.id }"
        @click="selectDomain(domain.id)"
      >
        <div class="domain-icon">{{ domain.icon }}</div>
        <h3>{{ domain.name }}</h3>
        <p class="domain-desc">{{ domain.description }}</p>
        <span v-if="domain.status === 'active'" class="badge active">Aktiv</span>
        <span v-else class="badge ready">Bereit</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue'

const emit = defineEmits(['domain-selected'])

const currentDomain = ref('math')

const domains = [
  {
    id: 'math',
    name: 'Math Clarity',
    icon: '📐',
    description: 'Sokratische Mathe-Nachhilfe für Klasse 7-13. Lernen durch Entdecken, nicht Kopieren.',
    status: 'active'
  },
  {
    id: 'business',
    name: 'Business Clarity',
    icon: '💼',
    description: 'Geschäftsentscheidungen & Automatisierungsstrategie. Klarheit durch Fragen finden.',
    status: 'ready'
  },
  {
    id: 'self',
    name: 'Self Clarity',
    icon: '🧘',
    description: 'Persönlicher Reflexions-Coach. Muster über 5-10 Sessions entdecken.',
    status: 'ready'
  }
]

function selectDomain(domainId) {
  currentDomain.value = domainId
  emit('domain-selected', domainId)
}
</script>

<style scoped>
.domain-selector {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.title {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  font-size: 1.25rem;
  color: #666;
  margin-bottom: 3rem;
}

.domains {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.domain-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 1rem;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.domain-card:hover {
  border-color: #667eea;
  transform: translateY(-4px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
}

.domain-card.active {
  border-color: #667eea;
  background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
}

.domain-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.domain-card h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #1a202c;
}

.domain-desc {
  color: #4a5568;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.badge.active {
  background: #10b981;
  color: white;
}

.badge.ready {
  background: #fbbf24;
  color: #78350f;
}
</style>
