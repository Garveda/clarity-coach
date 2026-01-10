<template>
  <!-- Toast-System global verfügbar -->
  <Toaster richColors closeButton />

  <!-- Deine eigentliche App -->
  <ClarityCoach />
</template>

<script setup>
import ClarityCoach from './components/ClarityCoach.vue'
</script>
