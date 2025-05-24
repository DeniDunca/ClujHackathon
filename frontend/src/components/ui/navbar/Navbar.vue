<template>
  <nav class="w-screen px-8 py-2 flex flex-row justify-between">
    <div id="logo" class="font-extrabold text-2xl">Logo</div>
    <div id="navigation">
      <Button v-if="!authStore.isAuthenticated">{{ t('LOGIN') }}</Button>
      <Button v-if="authStore.isAuthenticated">{{ t('LOGOUT') }}</Button>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { useI18n } from 'vue-i18n'

import { useAuthStore } from '@/stores/auth.ts'

const { t } = useI18n()

const authStore = useAuthStore()
</script>

<style scoped></style>
