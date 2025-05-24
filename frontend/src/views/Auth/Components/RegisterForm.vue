<template>
  <Card class="max-w-2xl w-full">
    <CardHeader>
      <CardTitle class="text-2xl">{{ t('SIGN_UP') }}</CardTitle>
    </CardHeader>
    <CardContent class="">
      <form @submit="onSubmit" class="flex flex-col gap-4">
        <FormSummaryMessage />

        <div class="grid sm:grid-cols-2 gap-2 w-full items-start">
          <FormField v-slot="{ componentField }" name="firstName" class="w-full">
            <FormItem>
              <FormLabel>{{ t('FIRST_NAME') }}</FormLabel>
              <FormControl>
                <Input
                  type="text"
                  :placeholder="t('FIRST_NAME_PLACEHOLDER')"
                  v-bind="componentField"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
          <FormField v-slot="{ componentField }" name="lastName" class="w-full">
            <FormItem>
              <FormLabel>{{ t('LAST_NAME') }}</FormLabel>
              <FormControl>
                <Input
                  type="text"
                  :placeholder="t('LAST_NAME_PLACEHOLDER')"
                  v-bind="componentField"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
        </div>
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
            <FormLabel>{{ t('PASSWORD') }}</FormLabel>
            <FormControl>
              <Input type="password" v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="confirmPassword">
          <FormItem>
            <FormLabel>{{ t('CONFIRM_PASSWORD') }}</FormLabel>
            <FormControl>
              <Input type="password" v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>
        <Button type="submit">{{ t('SIGN_UP') }}</Button>
        <Button variant="outline" class="w-full">{{ t('SIGN_UP_WITH_GOOGLE') }}</Button>
        <div class="mt-4 text-center text-sm">
          {{ t('HAVE_ACCOUNT') }}
          <router-link to="/login" class="underline">{{ t('LOGIN') }}</router-link>
        </div>
      </form>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import { Button } from '@/components/ui/button'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useAuthStore } from '@/stores/auth.ts'
import FormSummaryMessage from '@/components/ui/form/FormSummaryMessage.vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const SPECIAL_CHARS = '!@#$%^&*()_+-=[]{}|;:,.<>?'
const MIN_PASSWORD_LENGTH = 8

const schema = z
  .object({
    email: z.string({ message: t('EMAIL_REQUIRED') }).email(t('EMAIL_INVALID')),
    password: z.string({ message: t('PASSWORD_REQUIRED') }).refine(
      (password) => {
        const hasMinLength = password.length >= MIN_PASSWORD_LENGTH
        const hasUppercase = /[A-Z]/.test(password)
        const hasLowercase = /[a-z]/.test(password)
        const hasNumber = /\d/.test(password)
        const hasSpecialChar = [...SPECIAL_CHARS].some((char) => password.includes(char))

        return hasMinLength && hasUppercase && hasLowercase && hasNumber && hasSpecialChar
      },
      {
        message: t('PASSWORD_REQUIREMENTS', { min: MIN_PASSWORD_LENGTH, special: SPECIAL_CHARS }),
      },
    ),
    confirmPassword: z.string({ message: t('CONFIRM_PASSWORD_REQUIRED') }),
    firstName: z
      .string({ message: t('FIRST_NAME_REQUIRED') })
      .min(3, t('FIRST_NAME_MIN'))
      .max(100, t('FIRST_NAME_MAX')),
    lastName: z
      .string({ message: t('LAST_NAME_REQUIRED') })
      .min(3, t('LAST_NAME_MIN'))
      .max(100, t('LAST_NAME_MAX')),
  })
  .superRefine((values, ctx) => {
    // Custom validation to check if passwords match
    if (values.confirmPassword !== values.password) {
      ctx.addIssue({
        path: ['confirmPassword'],
        message: t('PASSWORDS_MUST_MATCH'),
        code: z.ZodIssueCode.custom,
      })
    }
  })

type FormValues = z.infer<typeof schema>

const form = useForm({
  validationSchema: toTypedSchema(schema),
  name: 'login-form',
})

const authStore = useAuthStore()

const onSubmit = form.handleSubmit((values) => {
  authStore.register(values)
})
</script>
