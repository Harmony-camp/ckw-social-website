<template>
	<div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
		<div class="main-center col-span-3 space-y-4">
			<div class="p-4 bg-white border border-gray-200 rounded-lg">
				<h2 class="text-xl">#{{ route.params.id }}</h2>
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
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const posts = ref([])

function getFeed() {
	axios
		.get(`/api/posts/?trend=${route.params.id}`)
		.then((res) => {
			console.log('data :>> ', res.data)
			posts.value = res.data
		})
		.catch((error) => {
			console.log('error :>> ', error)
		})
}

watch(
	() => route.params.id,
	() => {
		console.log('route.params.id :>> ', route.params.id)
		getFeed()
	},
	{
		immediate: true,
		deep: true,
	}
)

onMounted(() => {
	getFeed()
})
</script>
