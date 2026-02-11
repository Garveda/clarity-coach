<template>
  <!-- Toast-System global verfügbar -->
  <Toaster richColors closeButton />

  <!-- Domain Selector or Active Domain -->
  <DomainSelector
    v-if="!selectedDomain"
    @domain-selected="selectDomain"
  />

  <ClarityCoach v-else-if="selectedDomain === 'math'" @back="goBack" />
  <SelfClarityChat v-else-if="selectedDomain === 'self'" @back="goBack" />
  <BusinessClarityChat v-else-if="selectedDomain === 'business'" @back="goBack" />
</template>

<script setup>
import { ref } from 'vue'
import DomainSelector from './components/DomainSelector.vue'
import ClarityCoach from './components/ClarityCoach.vue'
import SelfClarityChat from './components/SelfClarityChat.vue'
import BusinessClarityChat from './components/BusinessClarityChat.vue'

const selectedDomain = ref(null)

function selectDomain(domainId) {
  selectedDomain.value = domainId
}

function goBack() {
  selectedDomain.value = null
}
</script>
