<template>
	<div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
		<div class="main-center col-span-3 space-y-4">
			<div class="bg-white border border-gray-200 rounded-lg">
				<FeedForm :user="user" :posts="posts" />
			</div>

			<div
				class="p-4 bg-white border border-gray-200 rounded-lg"
				v-for="post in posts"
				:key="post.id"
			>
				<FeedItem :post="post" @deletePost="deletePost" />
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
import FeedForm from '../components/FeedForm.vue'
import axios from 'axios'
import { ref, onMounted } from 'vue'

const posts = ref([])
const user = ref(null)

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

function deletePost(id) {
	// console.log('deletepost in profile id :>> ', id)

	posts.value = posts.value.filter((post) => post.id !== id)
}

// function submitForm() {
// 	console.log('body :>> ', body.value)

// 	axios
// 		.post('/api/posts/create/', {
// 			body: body.value,
// 		})
// 		.then((res) => {
// 			console.log('data :>> ', res.data)
// 			posts.value.unshift(res.data)
// 		})
// }

onMounted(() => {
	getFeed()
})
</script>
