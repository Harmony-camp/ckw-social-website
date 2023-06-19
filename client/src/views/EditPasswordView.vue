<template>
	<div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
		<div class="main-left">
			<div class="p-12 bg-white border border-gray-200 rounded-lg">
				<h1 class="mb-6 text-2xl">Edit password</h1>
				<p class="mb-6 text-gray-500">Here you can change your password!</p>

				<router-link to="/profile/edit/password" class="underline">
					Edit password</router-link
				>
			</div>
		</div>

		<div class="main-right">
			<div class="p-12 bg-white border border-gray-200 rounded-lg">
				<form class="space-y-6" @submit.prevent="submitForm">
					<div>
						<label>Old password</label><br />
						<input
							type="password"
							v-model="form.old_password"
							placeholder="Your old password"
							class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
						/>
					</div>

					<div>
						<label>New password</label><br />
						<input
							type="password"
							v-model="form.new_password1"
							placeholder="Your new password"
							class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
						/>
					</div>

					<div>
						<label>Repeat password</label><br />
						<input
							type="password"
							v-model="form.new_password2"
							placeholder="Repeat password"
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
	old_password: '',
	new_password1: '',
	new_password2: '',
})

const errors = ref([])

function submitForm() {
	errors.value = []

	if (form.new_password1 !== form.new_password2) {
		errors.push('The password does not match')
	}

	if (errors.value.length === 0) {
		let formData = new FormData()
		formData.append('old_password', form.old_password)
		formData.append('new_password1', form.new_password1)
		formData.append('new_password2', form.new_password2)

		axios
			.post('/api/editpassword/', formData, {
				headers: {
					'Content-Type': 'multipart/form-data',
				},
			})
			.then((res) => {
				if (res.data.message === 'success') {
					toastStore.showToast(
						5000,
						'The information was saved',
						'bg-emerald-500'
					)

					router.push(`/profile/${userStore.user.id}`)
				} else {
					const data = JSON.parse(res.data.message)
					for (const key in data) {
						errors.value.push(data[key][0].message)
					}
				}
			})
			.catch((error) => {
				console.log('error :>> ', error)
			})
	}
}
</script>
