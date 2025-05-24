<template>
  <div class="flex min-h-screen w-full items-center justify-center">
    <Card class="max-w-2xl w-full">
      <CardHeader>
        <CardTitle class="text-2xl">{{ t('BOOK_APPOINTMENT') }}</CardTitle>
        <CardDescription>{{ t('APPOINTMENT_DESCRIPTION') }}</CardDescription>
      </CardHeader>
      <CardContent class="">
        <form @submit="onSubmit" class="flex flex-col gap-4">
          <FormSummaryMessage />

          <FormField v-slot="{ componentField }" name="fullName">
            <FormItem>
              <FormLabel>{{ t('FULL_NAME') }}</FormLabel>
              <FormControl>
                <Input
                  type="text"
                  :placeholder="t('FULL_NAME_PLACEHOLDER')"
                  v-bind="componentField"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
          <FormField v-slot="{ componentField }" name="email">
            <FormItem>
              <FormLabel>{{ t('EMAIL') }}</FormLabel>
              <FormControl>
                <Input type="email" :placeholder="t('EMAIL_PLACEHOLDER')" v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
          <FormField v-slot="{ componentField }" name="preferredDate">
            <FormItem>
              <FormLabel>{{ t('PREFERRED_DATE') }}</FormLabel>
              <FormControl>
                <Input type="date" v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
          <Button type="submit">{{ t('SUBMIT') }}</Button>
        </form>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import { Button } from '@/components/ui/button'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import FormSummaryMessage from '@/components/ui/form/FormSummaryMessage.vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth.ts'
import { computed } from 'vue'

const { t } = useI18n()
const authStore = useAuthStore()

const loggedInUserFullName = computed(() => {
  return authStore.user ? authStore.user?.first_name + ' ' + authStore.user?.last_name : undefined
})

const schema = z.object({
  fullName: z.string({ message: t('FULL_NAME_REQUIRED') }),
  email: z.string({ message: t('EMAIL_REQUIRED') }).email(t('EMAIL_INVALID')),
  preferredDate: z.coerce.date({ message: t('PREFERRED_DATE_REQUIRED') }),
})

const form = useForm({
  validationSchema: toTypedSchema(schema),
  name: 'create-appointment-form',
  initialValues: {
    fullName: loggedInUserFullName.value,
    email: authStore.user?.email,
  },
})

const onSubmit = form.handleSubmit(async (data) => {
  console.log(data)
})
</script>
