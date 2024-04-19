import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import './utils/request.js'

import './assets/main.css'

// console.log(import.meta.env.VITE_API_URL)

// axios.defaults.baseURL = import.meta.env.VITE_API_URL

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
