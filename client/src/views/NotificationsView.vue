<template>
	<div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
		<div class="main-center col-span-3 space-y-4">
			<div
				v-if="notifications.length"
				class="p-4 bg-white border border-gray-200 rounded-lg"
				v-for="notification in notifications"
				:key="notification.id"
			>
				{{ notification.body }}

				<button class="underline" @click="readNotification(notification)">
					Read more
				</button>
			</div>
			<div v-else class="p-4 bg-white border border-gray-200 rounded-lg">
				You don't have any unread notifications!
			</div>
		</div>
	</div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const notifications = ref([])

onMounted(() => {
	getNotifications()
})

function getNotifications() {
	axios
		.get('/api/notifications/')
		.then((res) => {
			// console.log('notifications :>> ', res.data)
			notifications.value = res.data
		})
		.catch((error) => {
			console.log('error :>> ', error)
		})
}

async function readNotification(notification) {
	// console.log('readNotification', notification)
	await axios
		.post(`/api/notifications/read/${notification.id}/`)
		.then((res) => {
			console.log('notifications :>> ', res.data)
		})
		.catch((error) => {
			console.log('error :>> ', error)
		})
	if (
		notification.type_of_notification == 'post_like' ||
		notification.type_of_notification == 'post_comment'
	) {
		// Rediect to post page
		router.push({ name: 'postview', params: { id: notification.post_id } })
	} else {
		// Rediect to friends page
		router.push({
			name: 'friends',
			params: { id: notification.created_for_id },
		})
	}
}
</script>
