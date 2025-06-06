<template>
  <nav class="w-screen px-8 py-2 flex flex-row justify-between items-center">
    <div id="logo" class="font-extrabold text-2xl">
      <router-link to="/">
        <img src="/logo.png" alt="Logo" class="h-8 inline-block" />
      </router-link>
    </div>

    <!-- Desktop Navigation -->
    <div v-if="!isSmallScreen" class="flex items-center gap-4">
      <div id="auth" v-if="!authStore.isAuthenticated" class="flex items-center gap-4">
        <!-- Dark Mode Toggle -->
        <Button variant="outline" size="icon" @click="toggleDark" :aria-label="t('TOGGLE_DARK_MODE')">
          <Sun v-if="isDark" class="w-4 h-4" />
          <Moon v-else class="w-4 h-4" />
        </Button>

        <!-- Language Selector -->
        <Select v-model="selectedLanguage" @update:model-value="changeLanguage">
          <SelectTrigger class="w-[120px]">
            <SelectValue :placeholder="t('LANGUAGE')" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="en">{{ t('ENGLISH') }}</SelectItem>
            <SelectItem value="ro">{{ t('ROMANIAN') }}</SelectItem>
          </SelectContent>
        </Select>

        <!-- Login Button -->
        <Button as-child>
          <router-link to="/login">{{ t('LOGIN') }}</router-link>
        </Button>
      </div>
      <div v-if="authStore.isAuthenticated">
        <ul class="flex flex-row gap-4 items-center">
          <li>
            <router-link to="/chat" class="hover:text-primary transition-colors">
              {{ t('CHATBOT') }}
            </router-link>
          </li>
          <li>
            <router-link to="/documents" class="hover:text-primary transition-colors">
              {{ t('DOCUMENTS') }}
            </router-link>
          </li>
          <li>
            <router-link to="/appointments" class="hover:text-primary transition-colors">
              {{ t('APPOINTMENTS') }}
            </router-link>
          </li>
          <li>
            <NavbarDropdown />
          </li>
        </ul>
      </div>
    </div>

    <!-- Mobile Navigation -->
    <div v-if="isSmallScreen">
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button variant="outline" size="icon" :aria-label="t('OPEN_MENU')">
            <Menu class="w-4 h-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent class="w-56" align="end">
          <template v-if="!authStore.isAuthenticated">
            <!-- Dark Mode Toggle -->
            <DropdownMenuItem @click="toggleDark" class="flex items-center justify-between">
              <span>{{ t('DARK_MODE') }}</span>
              <div class="flex items-center">
                <Sun v-if="isDark" class="w-4 h-4" />
                <Moon v-else class="w-4 h-4" />
              </div>
            </DropdownMenuItem>

            <!-- Language Selector -->
            <DropdownMenuItem @click.prevent class="flex items-center justify-between">
              <span>{{ t('LANGUAGE') }}</span>
              <Select v-model="selectedLanguage" @update:model-value="changeLanguage">
                <SelectTrigger class="w-[80px] h-6">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="en">{{ t('ENGLISH') }}</SelectItem>
                </SelectContent>
              </Select>
            </DropdownMenuItem>

            <DropdownMenuSeparator />

            <DropdownMenuItem>
              <router-link to="/login" class="w-full">{{ t('LOGIN') }}</router-link>
            </DropdownMenuItem>
          </template>
          <template v-else>
            <DropdownMenuItem>
              <router-link to="/documents" class="w-full">{{ t('DOCUMENTS') }}</router-link>
            </DropdownMenuItem>
            <DropdownMenuItem>
              <router-link to="/appointments" class="w-full">{{ t('APPOINTMENTS') }}</router-link>
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuLabel>{{ t('MY_ACCOUNT') }}</DropdownMenuLabel>
            <DropdownMenuItem>
              <router-link to="/profile" class="w-full">{{ t('PROFILE') }}</router-link>
            </DropdownMenuItem>
<!--            <DropdownMenuItem>-->
<!--              <router-link to="/settings" class="w-full">{{ t('SETTINGS') }}</router-link>-->
<!--            </DropdownMenuItem>-->
            <DropdownMenuSeparator />
            <DropdownMenuItem>
              <button @click="logout" class="w-full text-left">{{ t('LOGOUT') }}</button>
            </DropdownMenuItem>
          </template>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Button } from '@/components/ui/button'
import { useI18n } from 'vue-i18n'
import { useMediaQuery, breakpointsTailwind, useDark, useToggle } from '@vueuse/core'
import { toast } from 'vue-sonner'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Menu, Sun, Moon } from 'lucide-vue-next'

import { useAuthStore } from '@/stores/auth.ts'
import NavbarDropdown from '@/components/ui/navbar/NavbarDropdown.vue'

const { t, locale } = useI18n()

const isSmallScreen = useMediaQuery(`(max-width: ${breakpointsTailwind.sm}px)`)

const authStore = useAuthStore()

// Dark mode functionality
const isDark = useDark({
  selector: 'html',
  attribute: 'class',
  valueDark: 'dark',
  valueLight: '',
})

const toggleDark = () => {
  isDark.value = !isDark.value
}

// Language functionality
const selectedLanguage = ref(locale.value)

const changeLanguage = (newLocale: string) => {
  locale.value = newLocale
  selectedLanguage.value = newLocale
  // Persist language preference
  localStorage.setItem('preferred-language', newLocale)
  toast.success(t('LANGUAGE_UPDATED'))
}

const logout = async () => {
  console.log('Logging out')
  await authStore.logout()
}
</script>

<style scoped></style>
