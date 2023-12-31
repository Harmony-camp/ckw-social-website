<template>
	<div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
		<div class="main-left col-span-1">
			<div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
				<img :src="user.get_avatar" class="w-36 mb-6 mx-auto rounded-full" />
				<p>
					<strong>{{ user.name }}</strong>
				</p>
				<div class="mt-6 flex space-x-8 justify-around">
					<p class="text-xs text-gray-500">{{ user.friends_count }} friends</p>
					<p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
				</div>
			</div>
		</div>

		<div class="main-center col-span-2 space-y-4">
			<div
				class="p-4 bg-white border border-gray-200 rounded-lg"
				v-if="friendshipRequests.length"
			>
				<h2 class="mb-6 text-xl">friendship request</h2>
				<div
					v-for="friendshipRequest in friendshipRequests"
					:key="friendshipRequest.id"
					class="p-4 text-center bg-gray-100 rounded-lg"
				>
					<img
						:src="friendshipRequest.created_by.get_avatar"
						class="w-36 mb-6 mx-auto rounded-full"
					/>
					<p>
						<strong>
							<router-link
								:to="{ name: 'profile', params: { id: friendshipRequest.id } }"
								>{{ friendshipRequest.created_by.name }}</router-link
							>
						</strong>
					</p>

					<div class="mt-6 flex space-x-8 justify-around">
						<p class="text-xs text-gray-500">
							{{ user.friends_count }} friends
						</p>
						<p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
					</div>

					<div class="mt-6 space-x-4">
						<button
							@click="
								handleRequest('accepted', friendshipRequest.created_by.id)
							"
							class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg"
						>
							accept
						</button>
						<button
							@click="
								handleRequest('rejected', friendshipRequest.created_by.id)
							"
							class="inline-block py-4 px-6 bg-red-600 text-white rounded-lg"
						>
							reject
						</button>
					</div>
				</div>

				<hr />
			</div>

			<div
				class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-2 gap-4"
				v-if="friends.length"
			>
				<div
					v-for="user in friends"
					:key="user.id"
					class="p-4 text-center bg-gray-100 rounded-lg"
				>
					<img
						:src="user.get_avatar"
						class="w-40 h-40 mb-6 mx-auto rounded-full"
					/>
					<p>
						<strong>
							<router-link :to="{ name: 'profile', params: { id: user.id } }">{{
								user.name
							}}</router-link>
						</strong>
					</p>

					<div class="mt-6 flex space-x-8 justify-around">
						<p class="text-xs text-gray-500">
							{{ user.friends_count }} friends
						</p>
						<p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
					</div>
				</div>
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
import { useUserStore } from '@/stores/user'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { ref, onMounted } from 'vue'

const userStore = useUserStore()
const route = useRoute()

const user = ref({})
const friendshipRequests = ref([])
const friends = ref([])

onMounted(() => {
	getFriends()
})

function getFriends() {
	axios
		.get(`/api/friends/${route.params.id}/`)
		.then((res) => {
			console.log('data :>> ', res.data)

			friendshipRequests.value = res.data.requests
			friends.value = res.data.friends
			user.value = res.data.user
			console.log('friends :>> ', friends.value)
		})
		.catch((error) => {
			console.log('error :>> ', error)
		})
}

function handleRequest(status, pk) {
	console.log('handleRequest :>> ', status)

	axios
		.post(`/api/friends/${pk}/${status}/`)
		.then((res) => {
			console.log('data :>> ', res.data)
		})
		.catch((error) => {
			console.log('error :>> ', error)
		})
}
</script>
