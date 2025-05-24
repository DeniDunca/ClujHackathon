<script setup lang="ts">
import { RouterView } from 'vue-router'
// import { useDark } from '@vueuse/core'
import Navbar from '@/components/ui/navbar/Navbar.vue'

// const darkMode = useDark()
</script>

<template>
  <Navbar />
  <main>
    <RouterView />
  </main>
</template>

<style scoped></style>
