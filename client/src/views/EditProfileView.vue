<template>
	<div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
		<div class="main-left">
			<div class="p-12 bg-white border border-gray-200 rounded-lg">
				<h1 class="mb-6 text-2xl">Edit profile</h1>
				<p class="mb-6 text-gray-500">
					Lorem ipsum, dolor sit amet consectetur adipisicing elit. Harum at
					minima saepe quo dolore quam obcaecati sint voluptatibus, error natus
					pariatur numquam sapiente consectetur rem velit id, sit vitae aliquid!
				</p>
			</div>
		</div>

		<div class="main-right">
			<div class="p-12 bg-white border border-gray-200 rounded-lg">
				<form class="space-y-6" @submit.prevent="submitForm">
					<div>
						<label>Name</label><br />
						<input
							type="text"
							placeholder="请输入昵称"
							v-model="form.name"
							class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
						/>
					</div>
					<div>
						<label>E-mail</label><br />
						<input
							type="email"
							v-model="form.email"
							placeholder="请输入邮箱地址"
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
							Save changes
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
import { useRouter } from 'vue-router'
import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'

const router = useRouter()

const toastStore = useToastStore()
const userStore = useUserStore()

const form = reactive({
	email: userStore.user.email,
	name: userStore.user.name,
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

	if (errors.value.length === 0) {
		axios
			.post('/api/editprofile/', form)
			.then((res) => {
				if (res.data === 'information updated') {
					toastStore.showToast(
						5000,
						'The information was saved',
						'bg-emerald-500'
					)

					// Todo update the user store in the browser

					userStore.setUserInfo({
						id: userStore.user.id,
						name: form.name,
						email: form.email,
					})

					router.back()
				} else {
					toastStore.showToast(
						5000,
						`${res.data}.Please try again`,
						'bg-red-300'
					)
				}
			})
			.catch((error) => {
				console.log('error :>> ', error)
			})
	}
}
</script>
