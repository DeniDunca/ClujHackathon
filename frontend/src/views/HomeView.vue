<template>
  <div class="min-h-[calc(100vh-10rem)] flex justify-center flex-col relative overflow-hidden">
    <!-- Background image - positioned to the right on desktop/tablet -->
    <div
      class="absolute inset-0 bg-no-repeat bg-contain md:bg-right-center bg-center opacity-20 md:opacity-30"
      :style="{ backgroundImage: 'url(/homepage_bg_image.png)' }"
    ></div>

    <!-- Content container -->
    <div class="relative z-10 flex flex-col gap-4 w-full max-w-2/3 lg:max-w-2xl mx-auto items-center text-center md:items-start md:text-left md:ml-8 lg:ml-16 xl:ml-24">
      <h2 class="text-blue-500 font-extrabold text-3xl md:text-4xl lg:text-5xl whitespace-pre-line">
        {{ t('HEALTH_NAVIGATOR') }}
      </h2>
      <h3 class="font-semibold text-xl md:text-2xl lg:text-3xl max-w-2xl">
        {{ t('HEALTH_NAVIGATOR_DESCRIPTION') }}
      </h3>
      <span class="flex gap-2 flex-col sm:flex-row">
        <router-link to="/login">
          <Button class="w-full sm:w-auto">{{ t('GET_STARTED') }}</Button>
        </router-link>
        <router-link to="/documentation">
          <Button variant="outline" class="w-full sm:w-auto">{{ t('LEARN_MORE') }}</Button>
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
