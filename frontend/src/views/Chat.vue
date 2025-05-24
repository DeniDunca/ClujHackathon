<template>
  <div class="flex h-[calc(100vh-5rem)] flex-col w-full lg:max-w-2xl m-auto">
    <div
      ref="messagesContainer"
      class="flex-1 overflow-y-auto w-full"
    >
      <Message
        v-for="(message, index) in messages"
        :key="`${message.timestamp}-${index}`"
        :role="message.role"
        :content="message.content"
        :is-last-message="index === messages.length - 1"
        :timestamp="message.timestamp"
      />
    </div>
    <form @submit="onSubmit" class="flex flex-row w-full px-2 py-2 border-t bg-background">
      <Input
        type="text"
        :placeholder="t('ENTER_YOUR_MESSAGE')"
        v-model="newMessage"
        class="flex-1 mr-2"
      />
      <Button type="submit" :disabled="!newMessage.trim()">
        <SendHorizontal class="h-4 w-4"/>
      </Button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { type Ref, ref, nextTick, watch } from 'vue'
import { Message } from '@/components/ui/message'
import { Input } from '@/components/ui/input'
import { useI18n } from 'vue-i18n'
import { Button } from '@/components/ui/button'
import { SendHorizontal } from 'lucide-vue-next'

const { t } = useI18n()

const newMessage = ref('')
const messagesContainer = ref<HTMLElement>()

const messages: Ref<{ role: 'user' | 'assistant'; content: string; timestamp: number }[]> = ref([
  {
    role: 'user',
    content: 'Hello',
    timestamp: new Date().getTime(),
  },
  {
    role: 'assistant',
    content: 'Hello',
    timestamp: new Date().getTime(),
  },
])

// Check if user is at bottom of scroll
const isAtBottom = (): boolean => {
  if (!messagesContainer.value) return true
  const { scrollTop, scrollHeight, clientHeight } = messagesContainer.value
  return scrollTop + clientHeight >= scrollHeight - 10 // 10px threshold
}

// Scroll to bottom
const scrollToBottom = () => {
  if (!messagesContainer.value) return
  messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
}

// Watch for new messages and auto-scroll if at bottom
watch(messages, async () => {
  const wasAtBottom = isAtBottom()
  await nextTick()
  if (wasAtBottom) {
    scrollToBottom()
  }
}, { deep: true })

const onSubmit = (e: Event) => {
  e.preventDefault()
  if (!newMessage.value.trim()) return

  messages.value.push({
    role: messages.value.length % 2 === 0 ? 'user' : 'assistant',
    content: newMessage.value,
    timestamp: new Date().getTime(),
  })

  newMessage.value = ''
}
</script>

<style scoped></style>
