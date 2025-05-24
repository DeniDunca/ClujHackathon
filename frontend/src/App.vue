<script setup lang="ts">
import { RouterView } from 'vue-router'
// import { useDark } from '@vueuse/core'
import Navbar from '@/components/ui/navbar/Navbar.vue'
import { Toaster } from '@/components/ui/sonner'
import 'vue-sonner/style.css'

// const darkMode = useDark()
</script>

<template>
  <Navbar />
  <Toaster richColors position="top-right" />
  <main>
    <RouterView />
  </main>
</template>

<style scoped></style>
