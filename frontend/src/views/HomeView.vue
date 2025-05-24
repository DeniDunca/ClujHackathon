<template>
  <div class="min-h-[calc(100vh-10rem)] flex justify-center flex-col">
    <div class="flex flex-col gap-4 w-full max-w-2/3 lg:max-w-2xl m-auto items-center text-center">
      <h2 class="text-blue-500 font-extrabold text-3xl whitespace-pre-line">
        {{ t('HEALTH_NAVIGATOR') }}
      </h2>
      <h3 class="font-semibold text-xl">
        {{ t('HEALTH_NAVIGATOR_DESCRIPTION') }}
      </h3>
      <span class="flex gap-2">
        <router-link to="/login">
          <Button>{{t('GET_STARTED')}}</Button>
        </router-link>
        <router-link to="/documentation">
          <Button variant="outline">{{t('LEARN_MORE')}}</Button>
        </router-link>
      </span>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { Button } from '@/components/ui/button'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>
