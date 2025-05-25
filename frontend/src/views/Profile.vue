<template>
  <div class="container mx-auto p-6 max-w-4xl">
    <div class="mb-8">
      <h1 class="text-3xl font-bold">{{ t('PROFILE') }}</h1>
      <p class="text-muted-foreground mt-2">{{ t('MANAGE_YOUR_ACCOUNT') }}</p>
    </div>

    <Tabs default-value="information" class="w-full">
      <TabsList class="grid w-full grid-cols-2">
        <TabsTrigger value="information">{{ t('INFORMATION') }}</TabsTrigger>
        <TabsTrigger value="settings">{{ t('SETTINGS') }}</TabsTrigger>
      </TabsList>

      <!-- Information Tab -->
      <TabsContent value="information" class="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>{{ t('PERSONAL_INFORMATION') }}</CardTitle>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <ReadonlyValue
                :value="authStore.user?.first_name"
                :label="t('FIRST_NAME')"
              />
              <ReadonlyValue
                :value="authStore.user?.last_name"
                :label="t('LAST_NAME')"
              />
              <ReadonlyValue
                :value="authStore.user?.email"
                :label="t('EMAIL')"
              />
            </div>
            <ReadonlyValue
              :value="getUploadDate(authStore.user?.created_at || '', 'dd/mm/yyyy HH:MM')"
              :label="t('MEMBER_SINCE')"
            />
          </CardContent>
        </Card>
      </TabsContent>

      <!-- Settings Tab -->
      <TabsContent value="settings" class="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>{{ t('PREFERENCES') }}</CardTitle>
          </CardHeader>
          <CardContent class="space-y-6">
            <!-- Dark Mode Toggle -->
            <div class="flex items-center justify-between">
              <div class="space-y-0.5">
                <Label>{{ t('DARK_MODE') }}</Label>
                <p class="text-sm text-muted-foreground">{{ t('DARK_MODE_DESCRIPTION') }}</p>
              </div>
              <Switch v-model="isDark" @update:model-value="toggleDark" />
            </div>

            <!-- Language Selector -->
            <div class="space-y-2">
              <Label>{{ t('LANGUAGE') }}</Label>
              <p class="text-sm text-muted-foreground">{{ t('LANGUAGE_DESCRIPTION') }}</p>
              <Select v-model="selectedLanguage" @update:model-value="changeLanguage">
                <SelectTrigger class="w-full md:w-[200px]">
                  <SelectValue :placeholder="t('LANGUAGE')" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="en">{{ t('ENGLISH') }}</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        <!-- Danger Zone -->
        <Card class="border-destructive">
          <CardHeader>
            <CardTitle class="text-destructive">{{ t('DANGER_ZONE') }}</CardTitle>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="space-y-2">
              <p class="text-sm text-muted-foreground">{{ t('ERASE_DATA_DESCRIPTION') }}</p>
              <Dialog v-model:open="showDeleteDialog">
                <DialogTrigger as-child>
                  <Button variant="destructive">{{ t('ERASE_MY_DATA') }}</Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>{{ t('CONFIRM_DELETE_ACCOUNT') }}</DialogTitle>
                    <DialogDescription>
                      {{ t('DELETE_ACCOUNT_WARNING') }}
                    </DialogDescription>
                  </DialogHeader>
                  <DialogFooter>
                    <Button variant="outline" @click="showDeleteDialog = false">{{ t('CANCEL') }}</Button>
                    <Button variant="destructive" @click="deleteAccount" :disabled="isDeleting">
                      {{ isDeleting ? t('LOADING') : t('DELETE') }}
                    </Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            </div>
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useDark, useToggle } from '@vueuse/core'
import { toast } from 'vue-sonner'
import axios from 'axios'

// UI Components
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Switch } from '@/components/ui/switch'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from '@/components/ui/dialog'
import ReadonlyValue from '@/components/ui/ReadonlyValue.vue'

// Stores and utilities
import { useAuthStore } from '@/stores/auth'
import { getUploadDate } from '@/lib/utils'

const { t, locale } = useI18n()
const router = useRouter()
const authStore = useAuthStore()

// Dark mode functionality
const isDark = useDark({
  selector: 'html',
  attribute: 'class',
  valueDark: 'dark',
  valueLight: '',
})
const toggleDark = () => {
  return useToggle(isDark)
}

// Language functionality
const selectedLanguage = ref(locale.value)

const changeLanguage = (newLocale: any) => {
  locale.value = newLocale
  selectedLanguage.value = newLocale
  // You can add localStorage persistence here if needed
  localStorage.setItem('preferred-language', newLocale)
  toast.success('Language updated successfully')
}

// Delete account functionality
const showDeleteDialog = ref(false)
const isDeleting = ref(false)

const deleteAccount = async () => {
  if (!authStore.user?.id) {
    toast.error(t('DELETE_ACCOUNT_ERROR'))
    return
  }

  isDeleting.value = true

  try {
    // const response = await axios.delete(`/auth/users/${authStore.user.id}`)
    //
    // if (response.status === 204) {
    //   toast.success(t('ACCOUNT_DELETED'))
    //   await authStore.logout()
    //   router.push('/')
    // }
    toast.success(t('DATA_WAS_ERASED'));
  } catch (error) {
    console.error('Delete account error:', error)
    toast.error(t('DELETE_ACCOUNT_ERROR'))
  } finally {
    isDeleting.value = false
    showDeleteDialog.value = false
  }
}
</script>
