<template>
	<div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
		<div class="main-left col-span-3 space-y-4">
			<div class="bg-white border border-gray-200 rounded-lg">
				<form @submit.prevent="submitForm" class="p-4 flex space-x-4">
					<input
						v-model="query"
						type="search"
						class="p-4 w-full bg-gray-100 rounded-lg"
						placeholder="搜索您感兴趣的内容..."
					/>

					<button
						href="#"
						class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg"
					>
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
								d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
							/>
						</svg>
					</button>
				</form>
			</div>

			<div
				class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-4 gap-4"
				v-if="users.length"
			>
				<div
					v-for="user in users"
					:key="user.id"
					class="p-4 text-center bg-gray-100 rounded-lg"
				>
					<img :src="user.get_avatar" class="mb-6 rounded-full" />
					<p>
						<strong>
							<router-link :to="{ name: 'profile', params: { id: user.id } }">{{
								user.name
							}}</router-link>
						</strong>
					</p>

					<div class="mt-6 flex space-x-8 justify-around">
						<p class="text-xs text-gray-500">{{ user.friends_count }} 好友</p>
						<p class="text-xs text-gray-500">{{ user.posts_count }} 推文</p>
					</div>
				</div>
			</div>

			<div
				class="p-4 bg-white border border-gray-200 rounded-lg"
				v-for="post in posts"
				:key="post.id"
			>
				<FeedItem :post="post" />
			</div>
		</div>

		<div class="main-right col-span-1 space-y-4">
			<PeopleYouMayKnow />
			<Trends />
		</div>
	</div>
</template>

<script setup>
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
import { ref } from 'vue'
import axios from 'axios'

const query = ref('')
// 搜索对象
const users = ref([])
const posts = ref([])

function submitForm() {
	console.log('submitForm')

	axios
		.post('/api/search/', {
			query: query.value,
		})
		.then((res) => {
			console.log('res :>> ', res.data)
			users.value = res.data.users
			posts.value = res.data.posts
		})
		.catch((error) => {
			console.log('error :>> ', error)
		})
}
</script>
