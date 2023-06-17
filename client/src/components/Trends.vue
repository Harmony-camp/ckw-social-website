<template>
	<div class="p-4 bg-white border border-gray-200 rounded-lg">
		<h3 class="mb-6 text-xl">Trends</h3>

		<div class="space-y-4">
			<div
				v-for="trend in trends"
				:key="trend.id"
				class="flex item-center justify-between"
			>
				<p class="text-xs">
					<strong>#{{ trend.hashtag }}</strong
					><br />
					<span class="text-gray-500">{{ trend.occurences }} posts</span>
				</p>

				<router-link
					:to="{ name: 'trendview', params: { id: trend.hashtag } }"
					class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg"
					>Explore</router-link
				>
			</div>
		</div>
	</div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const trends = ref([])

onMounted(() => {
	getTrends()
})

function getTrends() {
	axios
		.get('/api/posts/trends/')
		.then((res) => {
			console.log('trends :>> ', res.data)
			trends.value = res.data
		})
		.catch((error) => {
			console.log('error :>> ', error)
		})
}
</script>
