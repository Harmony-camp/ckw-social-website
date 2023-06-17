<template>
	<div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
		<div class="main-center col-span-3 space-y-4">
			<div
				class="p-4 bg-white border border-gray-200 rounded-lg"
				v-if="post.id"
			>
				<FeedItem :post="post" />
			</div>

			<div
				class="p-4 ml-6 bg-white border border-gray-200 rounded-lg"
				v-for="comment in post.comments"
				:key="comment.id"
			>
				<CommentItem :comment="comment" />
			</div>

			<div class="bg-white border border-gray-200 rounded-lg">
				<form v-on:submit.prevent="submitForm" method="post">
					<div class="p-4">
						<textarea
							v-model="body"
							class="p-4 w-full bg-gray-100 rounded-lg"
							placeholder="What do you think?"
						></textarea>
					</div>

					<div class="p-4 order-t border-gray-100">
						<button
							class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg"
						>
							Comment
						</button>
					</div>
				</form>
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
import CommentItem from '../components/CommentItem.vue'
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const post = ref({
	comments: [],
})
const body = ref('')

function getPost() {
	axios
		.get(`/api/posts/${route.params.id}/`)
		.then((res) => {
			console.log('data :>> ', res.data)
			post.value = res.data
		})
		.catch((error) => {
			console.log('error :>> ', error)
		})
}

function submitForm() {
	console.log('body :>> ', body.value)

	axios
		.post(`/api/posts/${route.params.id}/comment/`, {
			body: body.value,
		})
		.then((res) => {
			console.log('data :>> ', res.data)
			post.value.comments.push(res.data)
			post.value.comments_count += 1
			body.value = ''
		})
}

onMounted(() => {
	getPost()
	// console.log('router :>> ', route.params)
})
</script>
