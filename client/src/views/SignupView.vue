<template>
	<div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
		<div class="main-left">
			<div class="p-12 bg-white border border-gray-200 rounded-lg">
				<h1 class="mb-6 text-2xl">注册</h1>
				<p class="mb-6 text-gray-500">
					Lorem ipsum, dolor sit amet consectetur adipisicing elit. Harum at
					minima saepe quo dolore quam obcaecati sint voluptatibus, error natus
					pariatur numquam sapiente consectetur rem velit id, sit vitae aliquid!
				</p>

				<p class="font-bold">
					已经有账号了吗？<RouterLink :to="{ name: 'login' }" class="underline"
						>请点击这里</RouterLink
					>
					进行登录！
				</p>
			</div>
		</div>
		<div class="main-right">
			<div class="p-12 bg-white border border-gray-200 rounded-lg">
				<form class="space-y-6" @submit.prevent="submitForm">
					<div>
						<label>昵称</label><br />
						<input
							type="text"
							placeholder="请输入昵称"
							v-model="form.name"
							class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
						/>
					</div>
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
							v-model="form.password1"
							placeholder="请输入密码"
							class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
						/>
					</div>

					<div>
						<label>重复密码</label><br />
						<input
							type="password"
							v-model="form.password2"
							placeholder="请再次输入密码"
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
							注册
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
import { useToastStore } from '@/stores/toast'

const toastStore = useToastStore()

const form = reactive({
	email: '',
	name: '',
	password1: '',
	password2: '',
})

const errors = ref([])

function submitForm() {
	errors.value = []

	if (form.email === '') {
		errors.value.push('您还未填写邮箱地址')
	}

	if (form.name === '') {
		errors.value.push('您还未填写昵称')
	}

	if (form.password1 === '') {
		errors.value.push('您还未填写密码')
	}

	if (form.password1 !== form.password2) {
		errors.value.push('两次输入密码不一致')
	}

	if (errors.value.length === 0) {
		axios
			.post('/api/signup/', form)
			.then((res) => {
				if (res.data.message === 'success') {
					toastStore.showToast(5000, '该用户注册成功，请登录', 'bg-emerald-500')
					form.email = ''
					form.name = ''
					form.password1 = ''
					form.password2 = ''
				} else {
					toastStore.showToast(5000, '出现了一些错误，请重试', 'bg-red-300')
				}
			})
			.catch((error) => {
				console.log('error :>> ', error)
			})
	}
}
</script>
