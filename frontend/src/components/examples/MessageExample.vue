<template>
  <div class="p-8 space-y-4 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">{{ t('MESSAGE_COMPONENT_EXAMPLE') }}</h1>

    <div class="space-y-4 border rounded-lg p-4 bg-background">
      <!-- User Message -->
      <Message
        role="user"
        content="Hello! I have some questions about cancer prevention."
        :is-last-message="false"
        :timestamp="new Date(Date.now() - 300000).toISOString()"
      />

      <!-- Assistant Message -->
      <Message
        role="assistant"
        content="Hello! I'd be happy to help you with information about cancer prevention. What specific aspects would you like to know more about?"
        :is-last-message="false"
        :timestamp="new Date(Date.now() - 240000).toISOString()"
      />

      <!-- User Message with longer content -->
      <Message
        role="user"
        content="I'm particularly interested in dietary recommendations and lifestyle changes that can help reduce cancer risk. Can you provide some evidence-based suggestions?"
        :is-last-message="false"
        :timestamp="new Date(Date.now() - 180000).toISOString()"
      />

      <!-- Assistant Message with detailed response -->
      <Message
        role="assistant"
        content="Certainly! Here are some evidence-based recommendations for cancer prevention:

**Dietary Recommendations:**
• Eat plenty of fruits and vegetables (aim for 5+ servings daily)
• Choose whole grains over refined grains
• Limit processed and red meat consumption
• Reduce alcohol intake
• Stay hydrated with water

**Lifestyle Changes:**
• Maintain a healthy weight
• Exercise regularly (at least 150 minutes of moderate activity per week)
• Don't smoke or use tobacco products
• Protect your skin from UV radiation
• Get regular health screenings

These recommendations are based on research from major cancer organizations and can significantly reduce your risk of developing various types of cancer."
        :is-last-message="true"
        :timestamp="new Date(Date.now() - 60000).toISOString()"
      />
    </div>

    <div class="mt-8 p-4 bg-muted rounded-lg">
      <h2 class="text-lg font-semibold mb-2">{{ t('COMPONENT_FEATURES') }}</h2>
      <ul class="list-disc list-inside space-y-1 text-sm text-muted-foreground">
        <li>Different styling for user vs assistant messages</li>
        <li>Avatar icons using Lucide icons (Bot for assistant, User for user)</li>
        <li>Responsive design with proper alignment</li>
        <li>Timestamp formatting (relative time display)</li>
        <li>Support for multiline content with proper text wrapping</li>
        <li>Consistent with shadcn-vue design system</li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Message } from '@/components/ui/message'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style scoped></style>
