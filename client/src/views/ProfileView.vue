<template>
	<div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
		<div class="main-left col-span-1">
			<div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
				<img :src="user.get_avatar" class="mb-6 rounded-full" />
				<p>
					<strong>{{ user.name }}</strong>
				</p>
				<div class="mt-6 flex space-x-8 justify-around" v-if="user.id">
					<router-link :to="{ name: 'friends', params: { id: user.id } }">
						<p class="text-xs text-gray-500">
							{{ user.friends_count }} friends
						</p>
					</router-link>
					<p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
				</div>

				<div class="mt-6">
					<button
						v-if="userStore.user.id !== user.id"
						@click="sendFriendshipRequest"
						class="inline-block py-3 px-6 bg-purple-600 text-xs text-white rounded-lg"
					>
						Send friendship request
					</button>

					<button
						v-if="userStore.user.id !== user.id"
						@click="sendDirectMessage"
						class="inline-block mt-4 py-3 px-6 bg-purple-600 text-xs text-white rounded-lg"
					>
						Send direct message
					</button>

					<router-link
						v-if="userStore.user.id === user.id"
						to="/profile/edit"
						class="inline-block py-3 px-6 bg-purple-600 text-xs text-white rounded-lg"
					>
						Edit Profile
					</router-link>

					<button
						v-if="userStore.user.id === user.id"
						@click="logout"
						class="ml-2 inline-block py-3 px-6 bg-red-600 text-xs text-white rounded-lg"
					>
						Log out
					</button>
				</div>
			</div>
		</div>

		<div class="main-center col-span-2 space-y-4">
			<div
				class="bg-white border border-gray-200 rounded-lg"
				v-if="userStore.user.id === user.id"
			>
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
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { ref, onMounted, watch } from 'vue'

const userStore = useUserStore()
const toastStore = useToastStore()
const route = useRoute()
const router = useRouter()

const posts = ref([])
const user = ref({
	id: '',
})
const body = ref('')

function sendFriendshipRequest() {
	axios
		.post(`/api/friends/${route.params.id}/request/`)
		.then((res) => {
			console.log('data :>> ', res.data)
			// user = response.data.user

			if (res.data == 'request already sent') {
				toastStore.showToast(
					5000,
					'The request has already been sent!',
					'bg-red-300'
				)
			} else {
				toastStore.showToast(5000, 'The request was sent!', 'bg-emerald-300')
			}
		})
		.catch((error) => {
			console.log('error :>> ', error)
		})
}

function sendDirectMessage() {
	console.log('messagesend')

	axios
		.get(`/api/chat/${route.params.id}/get-or-create/`)
		.then((res) => {
			console.log('conversation :>> ', res.data)
			router.push('/chat')
		})
		.catch((error) => {
			console.log('error :>> ', error)
		})
}

function getFeed() {
	axios
		.get(`api/posts/profile/${route.params.id}/`)
		.then((res) => {
			console.log('posts :>> ', res.data)
			posts.value = res.data.posts
			user.value = res.data.user
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
			console.log('user submit post :>> ', res.data)
			posts.value.unshift(res.data)
			body.value = ''
			user.value.posts_count += 1
		})
}

function logout() {
	userStore.removeToken()

	router.push('/login')
}

// 修复个人资料页中路由监听页面内容不刷新的问题
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

// watch('$route.params.id', getFeed(), {
// 	immediate: true,
// 	deep: true,
// })

// 在路由跳转之前检查要跳转的name是否与当前页的name相同
// onBeforeRouteUpdate((to, from, next) => {
// 	console.log('from >> ', from)
// 	console.log('to :>> ', to)
// 	if (from.name === to.name) {
// 		getFeed()
// 	}
// })

onMounted(() => {
	getFeed()
})
</script>
