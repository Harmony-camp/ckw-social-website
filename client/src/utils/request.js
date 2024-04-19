import axios from 'axios'

axios.defaults.baseURL = import.meta.env.VITE_API_URL

console.log(import.meta.env.VITE_API_URL)

const service = axios.create({
	baseURL: import.meta.env.VITE_BASEURL,
	timeout: 5000,
})
