<template>
	<div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
		<div class="main-center col-span-3 space-y-4">
			<div class="bg-white border border-gray-200 rounded-lg">
				<form @submit.prevent="submitForm" method="post">
					<div class="p-4">
						<textarea
							v-model="body"
							class="p-4 w-full bg-gray-100 rounded-lg"
							placeholder="你现在正在想什么？"
						></textarea>
					</div>

					<div class="p-4 border-t border-gray-100 flex justify-between">
						<button
							class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg"
						>
							添加图片
						</button>
						<button
							class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg"
						>
							发表
						</button>
					</div>
				</form>
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
import axios from 'axios'
import { ref, onMounted } from 'vue'

const posts = ref([])
const body = ref('')

function getFeed() {
	axios
		.get('/api/posts/')
		.then((res) => {
			console.log('data :>> ', res.data)
			posts.value = res.data
		})
		.catch((error) => {
			console.log('error :>> ', error)
		})
}

function submitForm() {
	console.log('body :>> ', body.value)

	axios
		.post('/api/posts/create/', {
			body: body.value,
		})
		.then((res) => {
			console.log('data :>> ', res.data)
			posts.value.unshift(res.data)
		})
}

onMounted(() => {
	getFeed()
})
</script>
