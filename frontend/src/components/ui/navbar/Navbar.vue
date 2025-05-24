<template>
  <nav class="w-screen px-8 py-2 flex flex-row justify-between items-center">
    <div id="logo" class="font-extrabold text-2xl">Logo</div>
    <div id="auth" v-if="!authStore.isAuthenticated">
      <Button v-if="!authStore.isAuthenticated">{{ t('LOGIN') }}</Button>
    </div>
    <div v-else>
      <ul class="flex flex-row gap-4 items-center">
        <li>
          <router-link to="/documents">{{ t('DOCUMENTS') }}</router-link>
        </li>
        <li>
          <router-link to="/appointments">{{ t('APPOINTMENTS') }}</router-link>
        </li>
        <li>
          <NavbarDropdown />
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { useI18n } from 'vue-i18n'

import { useAuthStore } from '@/stores/auth.ts'
import NavbarDropdown from '@/components/ui/navbar/NavbarDropdown.vue'

const { t } = useI18n()

const authStore = useAuthStore()
</script>

<style scoped></style>
