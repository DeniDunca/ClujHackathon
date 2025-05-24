<template>
  <div :class="cn('flex w-full gap-3 p-4', role === 'user' ? 'justify-end' : 'justify-start')">
    <!-- Assistant Avatar -->
    <div
      v-if="role === 'assistant'"
      :class="
        cn(
          'flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border shadow-sm',
          'bg-primary text-primary-foreground',
        )
      "
    >
      <Bot class="h-4 w-4" />
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
            'rounded-lg px-3 py-2 text-sm shadow-sm',
            role === 'user'
              ? 'bg-primary text-primary-foreground ml-auto'
              : 'bg-muted text-muted-foreground',
          )
        "
      >
        <p class="whitespace-pre-wrap break-words">{{ content }}</p>
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
import { Bot, User } from 'lucide-vue-next'

const props = defineProps<{
  role: 'user' | 'assistant'
  content: string
  isLastMessage: boolean
  timestamp?: number
  class?: HTMLAttributes['class']
  isLoading?: boolean
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

<style scoped></style>
