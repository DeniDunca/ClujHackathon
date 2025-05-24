<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useDark } from '@vueuse/core'
import { Button } from '@/components/ui/button'
import Navbar from '@/components/ui/navbar/Navbar.vue'

const darkMode = useDark()
</script>

<template>
  <Navbar />
  <div class="flex gap-2">
    <router-link to="/login"> Login </router-link>
    <router-link to="/register"> Register </router-link>
    <Button @click="darkMode = !darkMode">Toggle dark mode</Button>
  </div>

  <RouterView />
</template>

<style scoped></style>
