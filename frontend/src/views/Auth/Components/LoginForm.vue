<template>
  <Card class="max-w-2xl w-full">
    <CardHeader>
      <CardTitle class="text-2xl"> Welcome back </CardTitle>
    </CardHeader>
    <CardContent class="">
      <form @submit="onSubmit" class="flex flex-col gap-4">
        <FormSummaryMessage />

        <FormField v-slot="{ componentField }" name="email">
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl>
              <Input type="email" placeholder="email@mail.com" v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="password">
          <FormItem>
            <div class="flex items-center">
              <FormLabel>Password</FormLabel>
              <router-link to="#" class="ml-auto inline-block text-sm underline"
                >Forgot your password?
              </router-link>
            </div>
            <FormControl>
              <Input type="password" v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>
        <Button type="submit"> Login </Button>
        <Button variant="outline" class="w-full"> Login with Google </Button>
        <div class="mt-4 text-center text-sm">
          Don't have an account?
          <router-link to="/register" class="underline"> Sign up </router-link>
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
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { useAuthStore } from '@/stores/auth.ts'
import FormSummaryMessage from '@/components/ui/form/FormSummaryMessage.vue'
import { useRouter } from 'vue-router'

const schema = z.object({
  email: z.string({ message: 'Email is required.' }).email('Invalid email address.'),
  password: z.string({ message: 'Password is required.' }),
})

const authStore = useAuthStore()
const router = useRouter()

const form = useForm({
  validationSchema: toTypedSchema(schema),
  name: 'login-form',
})

const onSubmit = form.handleSubmit(async (values) => {
  await authStore.login(values, form)
  await router.push({ name: 'home' })
})
</script>
