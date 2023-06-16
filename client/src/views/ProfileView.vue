<template>
	<div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
		<div class="main-left col-span-1">
			<div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
				<img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full" />
				<p>
					<strong>{{ user.name }}</strong>
				</p>
				<div class="mt-6 flex space-x-8 justify-around">
					<p class="text-xs text-gray-500">100 friends</p>
					<p class="text-xs text-gray-500">210 posts</p>
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
import { useRoute } from 'vue-router'
import axios from 'axios'
import { ref, onMounted, watch } from 'vue'

const userStore = useUserStore()
const route = useRoute()

const posts = ref([])
const user = ref({})
const body = ref('')

function getFeed() {
	axios
		.get(`api/posts/profile/${route.params.id}/`)
		.then((res) => {
			console.log('data :>> ', res.data)
			posts.value = res.data.posts
			user.value = res.data.user
			console.log(user.value)
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

// 修复个人资料页中路由监听页面内容不刷新的问题
watch(
	() => route.params,
	() => {
		// console.log('..111')
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
