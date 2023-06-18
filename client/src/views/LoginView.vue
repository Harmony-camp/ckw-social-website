<template>
	<div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
		<div class="main-left">
			<div class="p-12 bg-white border border-gray-200 rounded-lg">
				<h1 class="mb-6 text-2xl">登录</h1>
				<p class="mb-6 text-gray-500">
					Lorem ipsum, dolor sit amet consectetur adipisicing elit. Harum at
					minima saepe quo dolore quam obcaecati sint voluptatibus, error natus
					pariatur numquam sapiente consectetur rem velit id, sit vitae aliquid!
				</p>

				<p class="font-bold">
					没有账号？<RouterLink :to="{ name: 'signup' }" class="underline"
						>请点击这里</RouterLink
					>
					注册新账号以登录！
				</p>
			</div>
		</div>
		<div class="main-right">
			<div class="p-12 bg-white border border-gray-200 rounded-lg">
				<form class="space-y-6" @submit.prevent="submitForm">
					<div>
						<label>邮箱账号</label><br />
						<input
							type="email"
							v-model="form.email"
							placeholder="请输入邮箱地址"
							class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
						/>
					</div>
					<div>
						<label>密码</label><br />
						<input
							type="password"
							v-model="form.password"
							placeholder="请输入密码"
							class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
						/>
					</div>

					<template v-if="errors.length > 0">
						<div class="bg-red-300 text-white rounded-lg p-6">
							<p v-for="error in errors" :key="error">{{ error }}</p>
						</div>
					</template>

					<div>
						<button class="py-4 px-6 bg-purple-600 text-white rounded-lg">
							登录
						</button>
					</div>
				</form>
			</div>
		</div>
	</div>
</template>

<script setup>
import axios from 'axios'
import { reactive, ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const form = reactive({
	email: '',
	password: '',
})

const errors = ref([])

async function submitForm() {
	if (form.email === '') {
		errors.value.push('您还未填写邮箱地址')
	}

	if (form.password === '') {
		errors.value.push('您还未填写密码')
	}
	if (errors.value.length === 0) {
		await axios
			.post('/api/login/', form)
			.then((res) => {
				userStore.setToken(res.data)

				axios.defaults.headers.common['Authorization'] =
					'Bearer ' + res.data.access
			})
			.catch((error) => {
				console.log('error :>> ', error)
				errors.value.push('The email or password is in correct!')
			})
	}
	if (errors.value.length === 0) {
		await axios
			.get('/api/me/')
			.then((res) => {
				userStore.setUserInfo(res.data)

				router.push('/feed')
			})
			.catch((error) => {
				console.log('error :>> ', error)
			})
	}
}
</script>
