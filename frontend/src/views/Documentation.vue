<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <!-- Main Title -->
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold text-foreground mb-4">
        {{ t('BREAST_CANCER_TITLE') }}
      </h1>
    </div>

    <!-- Prevention Section -->
    <Card class="mb-8">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Shield class="h-5 w-5 text-primary" />
          1. {{ t('PREVENTION_SECTION_TITLE') }}
        </CardTitle>
        <CardDescription>
          {{ t('PREVENTION_SECTION_DESCRIPTION') }}
        </CardDescription>
      </CardHeader>
      <CardContent class="space-y-6">
        <!-- Lifestyle & Diet -->
        <div>
          <h3 class="text-lg font-semibold mb-3 flex items-center gap-2">
            <Apple class="h-4 w-4 text-green-600" />
            {{ t('LIFESTYLE_DIET_TITLE') }}
          </h3>
          <ul class="space-y-2">
            <li class="flex items-start gap-2">
              <CheckCircle class="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm">{{ t('LIFESTYLE_DIET_WEIGHT') }}</span>
            </li>
            <li class="flex items-start gap-2">
              <CheckCircle class="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm">{{ t('LIFESTYLE_DIET_MEDITERRANEAN') }}</span>
            </li>
            <li class="flex items-start gap-2">
              <CheckCircle class="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm">{{ t('LIFESTYLE_DIET_ALCOHOL') }}</span>
            </li>
            <li class="flex items-start gap-2">
              <CheckCircle class="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm">{{ t('LIFESTYLE_DIET_SMOKING') }}</span>
            </li>
          </ul>
        </div>

        <!-- Physical Activity -->
        <div>
          <h3 class="text-lg font-semibold mb-3 flex items-center gap-2">
            <Activity class="h-4 w-4 text-blue-600" />
            {{ t('PHYSICAL_ACTIVITY_TITLE') }}
          </h3>
          <ul class="space-y-2">
            <li class="flex items-start gap-2">
              <CheckCircle class="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm">{{ t('PHYSICAL_ACTIVITY_AEROBIC') }}</span>
            </li>
            <li class="flex items-start gap-2">
              <CheckCircle class="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm">{{ t('PHYSICAL_ACTIVITY_STRENGTH') }}</span>
            </li>
          </ul>
        </div>

        <!-- Family History & Genetics -->
        <div>
          <h3 class="text-lg font-semibold mb-3 flex items-center gap-2">
            <Users class="h-4 w-4 text-purple-600" />
            {{ t('FAMILY_HISTORY_TITLE') }}
          </h3>
          <ul class="space-y-2">
            <li class="flex items-start gap-2">
              <CheckCircle class="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm">{{ t('FAMILY_HISTORY_COUNSELING') }}</span>
            </li>
            <li class="flex items-start gap-2">
              <CheckCircle class="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm">{{ t('FAMILY_HISTORY_HIGH_RISK') }}</span>
            </li>
          </ul>
        </div>
      </CardContent>
    </Card>

    <!-- Early Signs Section -->
    <Card class="mb-8">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Eye class="h-5 w-5 text-primary" />
          2. {{ t('EARLY_SIGNS_SECTION_TITLE') }}
        </CardTitle>
      </CardHeader>
      <CardContent class="space-y-6">
        <div>
          <h3 class="text-lg font-semibold mb-3">{{ t('EARLY_SIGNS_SUBTITLE') }}</h3>
          <ul class="space-y-2">
            <li class="flex items-start gap-2">
              <AlertCircle class="h-4 w-4 text-orange-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm font-medium">{{ t('EARLY_SIGNS_LUMP') }}</span>
            </li>
            <li class="flex items-start gap-2">
              <AlertCircle class="h-4 w-4 text-orange-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm font-medium">{{ t('EARLY_SIGNS_SWELLING') }}</span>
            </li>
            <li class="flex items-start gap-2">
              <AlertCircle class="h-4 w-4 text-orange-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm font-medium">{{ t('EARLY_SIGNS_DIMPLING') }}</span>
            </li>
            <li class="flex items-start gap-2">
              <AlertCircle class="h-4 w-4 text-orange-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm font-medium">{{ t('EARLY_SIGNS_PAIN') }}</span>
            </li>
            <li class="flex items-start gap-2">
              <AlertCircle class="h-4 w-4 text-orange-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm font-medium">{{ t('EARLY_SIGNS_NIPPLE') }}</span>
            </li>
            <li class="flex items-start gap-2">
              <AlertCircle class="h-4 w-4 text-orange-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm font-medium">{{ t('EARLY_SIGNS_SKIN') }}</span>
            </li>
          </ul>
        </div>

        <!-- Important Note -->
        <div
          class="bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4"
        >
          <div class="flex items-start gap-2">
            <Info class="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
            <p class="text-sm text-blue-800 dark:text-blue-200 font-medium">
              {{ t('EARLY_SIGNS_NOTE') }}
            </p>
          </div>
        </div>

        <!-- Educational Video -->
        <div>
          <h3 class="text-lg font-semibold mb-3 flex items-center gap-2">
            <Play class="h-4 w-4 text-red-600" />
            {{ t('EDUCATIONAL_VIDEO_TITLE') }}
          </h3>
          <Button variant="outline" class="flex items-center gap-2" @click="openVideo">
            <Play class="h-4 w-4" />
            {{ t('WATCH_VIDEO') }}
          </Button>
        </div>
      </CardContent>
    </Card>

    <!-- When to See a Doctor Section -->
    <Card class="mb-8">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Stethoscope class="h-5 w-5 text-primary" />
          3. {{ t('WHEN_TO_SEE_DOCTOR_TITLE') }}
        </CardTitle>
      </CardHeader>
      <CardContent class="space-y-6">
        <div>
          <h3 class="text-lg font-semibold mb-3 text-red-600">
            {{ t('WHEN_TO_SEE_DOCTOR_SUBTITLE') }}
          </h3>
          <ul class="space-y-2">
            <li class="flex items-start gap-2">
              <AlertTriangle class="h-4 w-4 text-red-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm font-medium">{{ t('WHEN_TO_SEE_DOCTOR_LUMP') }}</span>
            </li>
            <li class="flex items-start gap-2">
              <AlertTriangle class="h-4 w-4 text-red-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm font-medium">{{ t('WHEN_TO_SEE_DOCTOR_DISCOMFORT') }}</span>
            </li>
            <li class="flex items-start gap-2">
              <AlertTriangle class="h-4 w-4 text-red-600 mt-0.5 flex-shrink-0" />
              <span class="text-sm font-medium">{{ t('WHEN_TO_SEE_DOCTOR_MAMMOGRAM') }}</span>
            </li>
          </ul>
        </div>

        <!-- Routine Screening Table -->
        <div>
          <h3 class="text-lg font-semibold mb-3 flex items-center gap-2">
            <Calendar class="h-4 w-4 text-blue-600" />
            {{ t('ROUTINE_SCREENING_TITLE') }}
          </h3>
          <div class="overflow-x-auto">
            <table class="w-full border-collapse border border-border rounded-lg">
              <thead>
                <tr class="bg-muted">
                  <th class="border border-border px-4 py-2 text-left font-semibold">
                    {{ t('AGE_GROUP') }}
                  </th>
                  <th class="border border-border px-4 py-2 text-left font-semibold">
                    {{ t('SCREENING_RECOMMENDATION') }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="border border-border px-4 py-2 font-medium">{{ t('AGE_25_39') }}</td>
                  <td class="border border-border px-4 py-2">{{ t('SCREENING_25_39') }}</td>
                </tr>
                <tr class="bg-muted/50">
                  <td class="border border-border px-4 py-2 font-medium">{{ t('AGE_40_49') }}</td>
                  <td class="border border-border px-4 py-2">{{ t('SCREENING_40_49') }}</td>
                </tr>
                <tr>
                  <td class="border border-border px-4 py-2 font-medium">{{ t('AGE_50_74') }}</td>
                  <td class="border border-border px-4 py-2">{{ t('SCREENING_50_74') }}</td>
                </tr>
                <tr class="bg-muted/50">
                  <td class="border border-border px-4 py-2 font-medium">
                    {{ t('HIGH_RISK_PATIENTS') }}
                  </td>
                  <td class="border border-border px-4 py-2">{{ t('SCREENING_HIGH_RISK') }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Final Advice Section -->
    <Card class="mb-8">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Heart class="h-5 w-5 text-primary" />
          {{ t('FINAL_ADVICE_TITLE') }}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ul class="space-y-3">
          <li class="flex items-start gap-2">
            <CheckCircle2 class="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
            <span class="text-sm font-medium">{{ t('FINAL_ADVICE_PROACTIVE') }}</span>
          </li>
          <li class="flex items-start gap-2">
            <CheckCircle2 class="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
            <span class="text-sm font-medium">{{ t('FINAL_ADVICE_KNOW_NORMAL') }}</span>
          </li>
          <li class="flex items-start gap-2">
            <CheckCircle2 class="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
            <span class="text-sm font-medium">{{ t('FINAL_ADVICE_ENCOURAGE') }}</span>
          </li>
        </ul>

        <!-- Additional Information -->
        <div class="mt-6 pt-6 border-t border-border">
          <p class="text-sm text-muted-foreground italic">
            <i18n-t keypath="FINAL_ADVICE_MORE_INFO" tag="span">
              <template #esmoLink>
                <a
                  href="https://www.esmo.org/for-patients/patient-guides/breast-cancer"
                  target="_blank"
                  class="underline"
                >
                  {{ t('FINAL_ADVICE_ESMO') }}
                </a>
              </template>
              <template #nccnLink>
                <a href="https://www.nccn.org/" target="_blank" class="underline">
                  {{ t('FINAL_ADVICE_NCCN') }}
                </a>
              </template>
            </i18n-t>
          </p>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  Shield,
  Apple,
  Activity,
  Users,
  Eye,
  AlertCircle,
  CheckCircle,
  Info,
  Play,
  Stethoscope,
  AlertTriangle,
  Calendar,
  Heart,
  CheckCircle2,
} from 'lucide-vue-next'

const { t } = useI18n()

const openVideo = () => {
  window.open('https://youtu.be/-ygucOBbKJA?si=Q4XLS2NLqz_vhM0R', '_blank')
}
</script>
