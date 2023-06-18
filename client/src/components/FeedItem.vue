<template>
	<div class="mb-6 flex items-center justify-between">
		<div class="flex items-center space-x-6">
			<img :src="post.created_by.get_avatar" class="w-[40px] rounded-full" />
			<p>
				<strong>
					<router-link
						:to="{ name: 'profile', params: { id: post.created_by.id } }"
					>
						{{ post.created_by.name }}
					</router-link>
				</strong>
			</p>
		</div>

		<p class="text-gray-600">{{ post.created_at_formatted }} ago</p>
	</div>

	<p>{{ post.body }}</p>

	<div class="my-6 flex justify-between">
		<div class="flex space-x-6">
			<div class="flex items-center space-x-2">
				<svg
					@click="likePost(post.id)"
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
					class="w-6 h-6"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"
					/>
				</svg>
				<span class="text-gray-500 text-xs">{{ post.likes_count }} likes</span>
			</div>

			<div class="flex items-center space-x-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
					class="w-6 h-6"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M2.25 12.76c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.076-4.076a1.526 1.526 0 011.037-.443 48.282 48.282 0 005.68-.494c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z"
					/>
				</svg>

				<router-link
					:to="{ name: 'postview', params: { id: post.id } }"
					class="text-gray-500 text-xs"
				>
					{{ post.comments_count }} comments</router-link
				>
			</div>
		</div>

		<div>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				stroke-width="1.5"
				stroke="currentColor"
				class="w-6 h-6"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z"
				/>
			</svg>
		</div>
	</div>
</template>

<script setup>
// import { onMounted } from 'vue'
import axios from 'axios'
const props = defineProps({
	post: Object,
})

function likePost(id) {
	// console.log('likePost :>> ', id)

	axios
		.post(`/api/posts/${id}/like/`)
		.then((res) => {
			// console.log('res.data :>> ', res.data)
			// console.log('props :>> ', props.post)
			if (res.data == 'like created') {
				props.post.likes_count += 1
			}
		})
		.catch((error) => {
			console.log('error :>> ', error)
		})
}
</script>
