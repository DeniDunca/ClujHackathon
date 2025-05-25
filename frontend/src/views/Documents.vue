<template>
  <div class="container mx-auto p-6 max-w-2xl justify-between flex flex-col lg:flex-row gap-4">
    <div id="upload-document-form" class="min-w-xs">
      <h1 class="text-2xl font-bold mb-6">{{ t('UPLOAD_DOCUMENT') }}</h1>

      <Form @submit="onSubmit" class="flex flex-col gap-4">
        <FormSummaryMessage />

        <FormField v-slot="{ componentField }" name="file">
          <FormItem>
            <FormLabel>{{ t('UPLOAD_FILE') }}</FormLabel>
            <FormControl>
              <Input
                type="file"
                accept=".pdf"
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
      <h1 class="text-xl font-semibold mb-6" v-if="existingFiles?.length !== 0">{{t('EXISTING_DOCUMENTS')}}</h1>
      <div v-if="existingFiles === null">{{t('LOADING')}}</div>
      <div v-else-if="existingFiles.length === 0">{{t('NO_DOCUMENTS')}}</div>
      <div v-else>
        <div v-for="file in existingFiles" :key="file.document_id">
          <div class="flex flex-col gap-2 p-3 border rounded-lg hover:bg-muted/50 transition-colors mb-2">
            <div class="flex gap-2 justify-start items-start">
              <FileIcon class="h-4 w-4 mt-1 text-muted-foreground"/>
              <div class="flex flex-col gap-1">
                <span class="font-medium">
                  {{ getOriginalFilename(file) }}
                </span>
                <span class="text-sm text-muted-foreground">
                  {{ t('UPLOADED_ON') }}: {{ getUploadDate(file.created_at) }}
                </span>
              </div>
            </div>
          </div>
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
import {File as FileIcon} from 'lucide-vue-next'
import { getUploadDate } from '@/lib/utils'

type FileInfo = {
  document_id: string
  original_file: {
    filename: string
    url: string
  }
  text_file: {
    filename: string
    url: string
  }
  created_at: string
  last_accessed_at: string
}

const { t } = useI18n()

const selectedFile = ref<File | null>(null)
const isUploading = ref(false)
const existingFiles = ref<FileInfo[] | null>(null)

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
      await getExistingFiles()
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

const getOriginalFilename = (file: FileInfo) => {
  return file.original_file.filename.split('/').pop()
}
</script>
