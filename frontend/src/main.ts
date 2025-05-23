import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import axios from 'axios'
import i18n from '@/i18n'

axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:3000'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.use(i18n)

app.mount('#app')
