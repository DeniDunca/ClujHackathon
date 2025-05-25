<template>
  <div class="container mx-auto p-6 max-w-md display-flex justify-between">
    <div id="upload-document-form">
      <h1 class="text-2xl font-bold mb-6">{{ t('UPLOAD_DOCUMENT') }}</h1>

      <Form @submit="onSubmit" class="flex flex-col gap-4">
        <FormSummaryMessage />

        <FormField v-slot="{ componentField }" name="file">
          <FormItem>
            <FormLabel>{{ t('UPLOAD_FILE') }}</FormLabel>
            <FormControl>
              <Input
                type="file"
                accept=".pdf,.doc,.docx,.txt"
                v-bind="componentField"
                @change="handleFileChange"
                :disabled="isUploading"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <Button type="submit" class="w-full">
          {{ isUploading ? t('UPLOADING') : t('SUBMIT') }}
        </Button>
      </Form>
    </div>
    <div id="existing-documents">
      <div v-if="existingFiles === null">Null</div>
      <div v-else-if="existingFiles.length === 0">No files</div>
      <div v-else>
        <div v-for="file in existingFiles" :key="file.document_id">
          <a :href="file.original_file.url" target="_blank">{{ file.original_file.filename }}</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {onBeforeMount, ref} from 'vue'
import { useI18n } from 'vue-i18n'
import * as z from 'zod'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  FormControl,
} from '@/components/ui/form'
import FormSummaryMessage from '@/components/ui/form/FormSummaryMessage.vue'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { toast } from 'vue-sonner'
import axios from 'axios'

const { t } = useI18n()

const selectedFile = ref<File | null>(null)
const isUploading = ref(false)
const existingFiles = ref(null)

const schema = z.object({
  file: z.any().refine((file) => file instanceof File, {
    message: t('FILE_REQUIRED'),
  }),
})

const form = useForm({
  validationSchema: toTypedSchema(schema),
  name: 'upload-form',
})

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0] || null
  selectedFile.value = file

  if (file) {
    form.setFieldValue('file', file)
  }
}

const onSubmit = form.handleSubmit(async (values) => {
  if (!selectedFile.value) {
    toast.error(t('FILE_REQUIRED'))
    return
  }

  isUploading.value = true

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)

    const response = await axios.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    if (response.status === 200) {
      toast.success(t('FILE_UPLOAD_SUCCESS'))
      // Reset form
      selectedFile.value = null
      form.resetForm()
      // Reset file input
      const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement
      if (fileInput) {
        fileInput.value = ''
      }
    }
  } catch (error) {
    console.error('Upload error:', error)
    toast.error(t('FILE_UPLOAD_ERROR'))
  } finally {
    isUploading.value = false
  }
})

const getExistingFiles = async () => {
  try {
    const response = await axios.get('/upload/files')
    existingFiles.value = response.data
  } catch (error) {
    console.error('Error fetching files:', error)
  }
}

onBeforeMount(async () => {
  await getExistingFiles()
})
</script>
