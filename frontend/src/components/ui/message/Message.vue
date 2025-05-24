<template>
  <div
    :class="cn('flex w-full gap-3 p-2 max-w-full', role === 'user' ? 'justify-end' : 'justify-start')"
  >
    <!-- Assistant Avatar -->
    <div
      v-if="role === 'assistant'"
      :class="
        cn(
          'flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border shadow-sm',
          'bg-primary text-primary-foreground',
          isLoading && 'animate-pulse'
        )
      "
    >
      <Bot v-if="!isLoading" class="h-4 w-4" />
      <Loader2 v-else class="h-4 w-4 animate-spin" />
    </div>

    <!-- Message Content -->
    <div
      :class="
        cn('flex flex-col space-y-2 max-w-[80%]', role === 'user' ? 'items-end' : 'items-start')
      "
    >
      <!-- Message Bubble -->
      <div
        :class="
          cn(
            'rounded-lg px-3 py-2 text-sm shadow-sm transition-opacity',
            role === 'user'
              ? 'bg-primary text-primary-foreground ml-auto'
              : 'bg-muted text-muted-foreground',
            isDisabled && 'opacity-50',
            isLoading && role === 'assistant' && 'bg-muted/50'
          )
        "
      >
        <div v-if="isLoading && role === 'assistant'" class="flex items-center gap-2">
          <div class="flex space-x-1">
            <div class="w-2 h-2 bg-muted-foreground rounded-full animate-bounce [animation-delay:-0.3s]"></div>
            <div class="w-2 h-2 bg-muted-foreground rounded-full animate-bounce [animation-delay:-0.15s]"></div>
            <div class="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"></div>
          </div>
          <span class="text-xs text-muted-foreground">{{ t('THINKING') }}</span>
        </div>
        <vue-markdown v-else class="whitespace-pre-wrap break-words break-all chat-message" :source="content">
        </vue-markdown>
      </div>

      <!--      &lt;!&ndash; Timestamp &ndash;&gt;-->
      <!--      <div-->
      <!--        v-if="timestamp"-->
      <!--        :class="cn('text-xs text-muted-foreground', role === 'user' ? 'text-right' : 'text-left')"-->
      <!--      >-->
      <!--        {{ formatTimestamp(timestamp) }}-->
      <!--      </div>-->
    </div>

    <!-- User Avatar -->
    <div
      v-if="role === 'user'"
      :class="
        cn(
          'flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border shadow-sm',
          'bg-background text-foreground',
        )
      "
    >
      <User class="h-4 w-4" />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'
import { Bot, User, Loader2 } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'
import VueMarkdown from 'vue-markdown-render'

const { t } = useI18n()

const props = defineProps<{
  role: 'user' | 'assistant'
  content: string
  isLastMessage: boolean
  timestamp?: number
  class?: HTMLAttributes['class']
  isLoading?: boolean
  isDisabled?: boolean
}>()

// Format timestamp for display
const formatTimestamp = (timestamp: number): string => {
  try {
    const date = new Date(timestamp)
    const now = new Date()
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60))

    if (diffInMinutes < 1) {
      return 'Just now'
    } else if (diffInMinutes < 60) {
      return `${diffInMinutes}m ago`
    } else if (diffInMinutes < 1440) {
      const hours = Math.floor(diffInMinutes / 60)
      return `${hours}h ago`
    } else {
      return date.toLocaleDateString()
    }
  } catch {
    return timestamp.toString()
  }
}
</script>

<style scoped>
.chat-message {
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-word;
  hyphens: auto;
  max-width: 100%;
}

.chat-message * {
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-word;
  max-width: 100%;
}

/* Handle long URLs and code blocks */
.chat-message pre,
.chat-message code {
  white-space: pre-wrap;
  word-break: break-all;
  overflow-wrap: break-word;
}
</style>
