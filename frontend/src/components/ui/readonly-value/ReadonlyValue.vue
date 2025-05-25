
<template>
  <div
    class="block rounded-md transition-colors duration-200 w-full flex flex-col"
    :class="[
      variant === 'default' && 'bg-muted/50 border border-border',
      variant === 'ghost' && 'bg-transparent',
      variant === 'outline' && 'border border-border bg-background',
      size === 'sm' && 'px-3 py-2 text-sm',
      size === 'md' && 'px-4 py-3 text-base',
      size === 'lg' && 'px-5 py-4 text-lg',
      className
    ]"
    tabindex="0"
  >
    <div v-if="label" class="text-sm block font-medium text-muted-foreground mb-1">
      {{ label }}
    </div>
    <div class="text-foreground break-words" :class="{ 'mt-1': label }">
      <slot>
        {{ displayValue }}
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  value?: string | number | null
  label?: string
  variant?: 'default' | 'ghost' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  placeholder?: string
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  size: 'md',
  placeholder: '—'
})

const displayValue = computed(() => {
  if (props.value === null || props.value === undefined || props.value === '') {
    return props.placeholder
  }
  return props.value
})
</script>

<style scoped>
/* Focus styles for accessibility */
.readonly-value:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px hsl(var(--ring));
  border-radius: calc(var(--radius) - 2px);
}
</style>
