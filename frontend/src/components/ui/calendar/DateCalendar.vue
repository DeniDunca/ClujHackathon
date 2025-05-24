<template>
  <Calendar
    :model-value="calendarDateValue"
    @update:model-value="onCalendarUpdate"
    v-bind="$attrs"
  />
</template>

<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { computed } from 'vue'
import { CalendarDate } from '@internationalized/date'
import { toDate } from 'reka-ui/date'
import { Calendar } from '.'

interface Props {
  modelValue?: Date | null
  class?: HTMLAttributes['class']
}

interface Emits {
  (e: 'update:modelValue', value: Date | null): void
}

const props = defineProps<Props>()
const emits = defineEmits<Emits>()

// Convert Date to CalendarDate for the reka-ui Calendar component
const calendarDateValue = computed(() => {
  if (!props.modelValue) return null
  
  const date = props.modelValue
  return new CalendarDate(
    date.getFullYear(),
    date.getMonth() + 1, // CalendarDate months are 1-based
    date.getDate()
  )
})

// Convert CalendarDate back to Date when the calendar value changes
const onCalendarUpdate = (calendarDate: any) => {
  if (!calendarDate) {
    emits('update:modelValue', null)
    return
  }
  
  // Convert CalendarDate to regular Date
  const jsDate = toDate(calendarDate)
  emits('update:modelValue', jsDate)
}
</script>
