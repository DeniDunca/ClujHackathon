import { createI18n } from 'vue-i18n'
import enMessages from './locales/en.json'
import roMessages from './locales/ro.json'

const preferredLanguage = localStorage.getItem('preferred-language') || 'en'

const i18n = createI18n({
  locale: preferredLanguage,
  fallbackLocale: 'en',
  messages: {
    en: enMessages,
    ro: roMessages,
  },
})

export default i18n
