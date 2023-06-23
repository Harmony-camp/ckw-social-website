<template>
	<form @submit.prevent="submitForm" method="post">
		<div class="p-4">
			<textarea
				v-model="body"
				class="p-4 w-full bg-gray-100 rounded-lg"
				placeholder="What are you thinking?"
			></textarea>

			<label> <input type="checkbox" v-model="is_private" /> Private </label>

			<div id="preview" v-if="preview">
				<img :src="preview" class="w-1/2 hover:w-full mt-3 rounded-xl" />
			</div>
		</div>

		<div class="p-4 border-t border-gray-100 flex justify-between">
			<label
				class="custom-file-upload inline-block py-4 px-6 bg-gray-600 text-white rounded-lg"
			>
				<input type="file" ref="image" @change="onFileChange" />
				Attach image
			</label>

			<button
				class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg"
			>
				Post
			</button>
		</div>
	</form>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps({
	posts: Array,
	user: Object,
})

const body = ref('')
const preview = ref('')
const image = ref(null)
const is_private = ref(false)

function onFileChange(e) {
	let file = e.target.files[0]
	preview.value = URL.createObjectURL(file)
}

function submitForm() {
	// console.log('body :>> ', body.value)
	let formData = new FormData()
	formData.append('image', image.value.files[0])
	formData.append('body', body.value)
	formData.append('is_private', is_private.value)

	axios
		.post('/api/posts/create/', formData, {
			headers: {
				'Content-Type': 'multipart/form-data',
			},
		})
		.then((res) => {
			console.log('user submit post :>> ', res.data)
			props.posts.unshift(res.data)
			body.value = ''
			is_private.value = false
			preview.value = null
			if (props.user) {
				props.user.posts_count += 1
			}
		})
		.catch((error) => {
			console.log('error :>> ', error)
		})
}
</script>

<style scoped>
input[type='file'] {
	display: none;
}

.custom-file-upload {
	cursor: pointer;
}
</style>
