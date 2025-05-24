<template>
  <div class="flex gap-4 w-full max-w-3xl m-auto">
    <Card id="card-prevention">
      <CardHeader>
        <CardTitle>
          <h3 class="font-extrabold text-2xl">
            {{ t('PREVENTION') }}
          </h3>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p>{{ t('FIND_CANCER_PREVENTION_INFORMATION') }}</p>
      </CardContent>
      <CardFooter>
        <Button>{{ t('LEARN_MORE') }}</Button>
      </CardFooter>
    </Card>
    <Card id="card-chatbot">
      <CardContent>
        <div class="flex flex-row gap-2 items-center">
          <span
            class="p-2 max-h-12 dark:bg-white/90 bg-black/10 rounded-2xl flex items-center justify-center"
          >
            <Bot color="#000" />
          </span>
          <span>
            {{ t('CHATBOT_DESCRIPTION') }}
          </span>
        </div>
      </CardContent>
      <CardFooter class="w-full">
        <div class="relative w-full items-center">
          <Input id="search" type="text" :placeholder="t('ENTER_YOUR_MESSAGE')" class="pr-10 p-6" />
          <span class="absolute end-2 inset-y-0 flex items-center justify-center px-2">
            <MoveRight class="size-6 text-muted-foreground" />
          </span>
        </div>
      </CardFooter>
    </Card>
  </div>
</template>

<script lang="ts" setup>
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Bot, MoveRight } from 'lucide-vue-next'

import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>
