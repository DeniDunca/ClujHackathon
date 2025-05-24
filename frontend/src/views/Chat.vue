<template>
  <div class="flex h-[calc(100vh-5rem)] flex-col w-full lg:max-w-2xl m-auto">
    <div ref="messagesContainer" class="flex-1 overflow-y-auto w-full">
      <TransitionGroup name="message" tag="div" appear>
        <Message
          v-for="(message, index) in allMessages"
          :key="`${message.timestamp}-${index}-${message.isLoading ? 'loading' : 'loaded'}`"
          :role="message.role"
          :content="message.content"
          :is-last-message="index === allMessages.length - 1"
          :timestamp="message.timestamp"
          :is-loading="message.isLoading"
          :is-disabled="message.isDisabled"
        />
      </TransitionGroup>
    </div>
    <form @submit="onSubmit" class="flex flex-row w-full px-2 py-2 border-t bg-background">
      <Input
        type="text"
        :placeholder="t('ENTER_YOUR_MESSAGE')"
        v-model="newMessage"
        :disabled="isWaitingForResponse"
        class="flex-1 mr-2"
        :class="{ 'opacity-50 cursor-not-allowed': isWaitingForResponse }"
      />
      <Button
        type="submit"
        :disabled="!newMessage.trim() || isWaitingForResponse"
        :class="{ 'opacity-50 cursor-not-allowed': isWaitingForResponse }"
      >
        <Loader2 v-if="isWaitingForResponse" class="h-4 w-4 animate-spin" />
        <SendHorizontal v-else class="h-4 w-4" />
      </Button>
    </form>
  </div>
</template>

<script setup lang="ts">
import {
  type Ref,
  ref,
  nextTick,
  watch,
  onMounted,
  onBeforeMount,
  computed,
  TransitionGroup,
} from 'vue'
import { Message } from '@/components/ui/message'
import { Input } from '@/components/ui/input'
import { useI18n } from 'vue-i18n'
import { Button } from '@/components/ui/button'
import { SendHorizontal, Loader2 } from 'lucide-vue-next'
import axios from 'axios'

const { t } = useI18n()

const newMessage = ref('')
const messagesContainer = ref<HTMLElement>()
const isWaitingForResponse = ref(false)

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp: number
  isLoading?: boolean
  isDisabled?: boolean
}

const messages: Ref<ChatMessage[]> = ref([])
const conversation = ref()

// Computed property that includes loading states
const allMessages = computed(() => {
  // Create new objects to avoid mutating originals
  const result = messages.value.map((message, index) => ({
    ...message,
    isDisabled:
      isWaitingForResponse.value && index === messages.value.length - 1 && message.role === 'user',
  }))

  // Add loading assistant message if waiting for response
  if (isWaitingForResponse.value) {
    result.push({
      role: 'assistant',
      content: '',
      timestamp: Date.now(),
      isLoading: true,
      isDisabled: false,
    })
  }

  return result
})

const getExistingConversation = async () => {
  const result = await axios.get('/conversations/my-conversations')
  if (Array.isArray(result.data)) {
    conversation.value = result.data[0] // Hardcoded for now as we do not support more than one conversation
  }
}

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
watch(
  allMessages,
  async () => {
    const wasAtBottom = isAtBottom()
    await nextTick()
    if (wasAtBottom) {
      scrollToBottom()
    }
  },
  { deep: true },
)

const onSubmit = (e: Event) => {
  e.preventDefault()
  if (!newMessage.value.trim()) return

  sendMessage(newMessage.value)

  newMessage.value = ''
}

onBeforeMount(async () => {
  await getExistingConversation()
  if (!conversation.value) {
    const newConversation = await axios.post('/conversations', {})
    conversation.value = newConversation.data
  }

  messages.value = conversation.value.messages.map((message: any) => ({
    role: message.patient_id ? 'user' : 'assistant',
    content: message.content,
    timestamp: message.timestamp,
  }))
})

const sendMessage = async (content: string) => {
  messages.value.push({
    role: 'user',
    content,
    timestamp: new Date().getTime(),
  })

  isWaitingForResponse.value = true

  const response = await axios.post(`/conversations/${conversation.value.id}/messages`, {
    content,
    message_type: 'text',
  })

  messages.value.push({
    role: 'assistant',
    content: response.data.content,
    timestamp: new Date().getTime(),
  })

  isWaitingForResponse.value = false
}
</script>

<style scoped>
/* Message transition animations */
.message-enter-active {
  transition: all 0.3s ease-out;
}

.message-leave-active {
  transition: all 0.2s ease-in;
}

.message-enter-from {
  opacity: 0;
  transform: translateY(15px) scale(0.95);
}

.message-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.message-move {
  transition: transform 0.3s ease;
}
</style>
