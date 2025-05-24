<template>
  <Card class="max-w-2xl w-full">
    <CardHeader>
      <CardTitle class="text-2xl">{{ t('WELCOME_BACK') }}</CardTitle>
    </CardHeader>
    <CardContent class="">
      <form @submit="onSubmit" class="flex flex-col gap-4">
        <FormSummaryMessage />

        <FormField v-slot="{ componentField }" name="email">
          <FormItem>
            <FormLabel>{{ t('EMAIL') }}</FormLabel>
            <FormControl>
              <Input type="email" :placeholder="t('EMAIL_PLACEHOLDER')" v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="password">
          <FormItem>
            <div class="flex items-center">
              <FormLabel>{{ t('PASSWORD') }}</FormLabel>
              <router-link to="#" class="ml-auto inline-block text-sm underline"
                >{{ t('FORGOT_PASSWORD') }}
              </router-link>
            </div>
            <FormControl>
              <Input type="password" v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>
        <Button type="submit">{{ t('LOGIN') }}</Button>
        <div class="mt-4 text-center text-sm">
          {{ t('NO_ACCOUNT') }}
          <router-link to="/register" class="underline">{{ t('SIGN_UP') }}</router-link>
        </div>
      </form>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import { toast } from 'vue-sonner'

import { Button } from '@/components/ui/button'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useAuthStore } from '@/stores/auth.ts'
import FormSummaryMessage from '@/components/ui/form/FormSummaryMessage.vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const schema = z.object({
  email: z.string({ message: t('EMAIL_REQUIRED') }).email(t('EMAIL_INVALID')),
  password: z.string({ message: t('PASSWORD_REQUIRED') }),
})

const authStore = useAuthStore()
const router = useRouter()

const form = useForm({
  validationSchema: toTypedSchema(schema),
  name: 'login-form',
})

const onSubmit = form.handleSubmit(async (values) => {
  const success = await authStore.login(values)
  if (success) {
    await router.push({ name: 'home' })
  } else {
    toast.error(t('LOGIN_FAILED'))
  }
})
</script>
