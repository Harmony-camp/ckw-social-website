<template>
	<div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
		<div class="main-left col-span-1">
			<div class="p-4 bg-white border border-gray-200 rounded-lg">
				<div class="space-y-4">
					<div
						v-for="conversation in conversations"
						:key="conversation.id"
						@click="setActiveConversation(conversation.id)"
						class="flex items-center justify-between"
					>
						<div class="flex items-center space-x-2">
							<template v-for="user in conversation.users" :key="user.id">
								<img
									v-if="user.id !== userStore.user.id"
									:src="user.get_avatar"
									class="w-[40px] rounded-full"
								/>
								<p
									class="text-xs font-bold"
									v-if="user.id !== userStore.user.id"
								>
									{{ user.name }}
								</p>
							</template>
						</div>

						<span class="text-xs text-gray-500">{{
							conversation.modified_at_formatted
						}}</span>
					</div>
				</div>
			</div>
		</div>

		<div class="main-center col-span-3 space-y-4">
			<div class="bg-white border border-gray-200 rounded-lg">
				<div class="flex flex-col flex-grow p-4">
					<template
						v-for="message in activeConversation.messages"
						:key="message.id"
					>
						<div
							class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
							v-if="message.created_by.id == userStore.user.id"
						>
							<div>
								<div
									class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg"
								>
									<p class="text-sm">
										{{ message.body }}
									</p>
								</div>
								<span class="text-xs text-gray-500 leading-none">{{
									message.created_at_formatted
								}}</span>
							</div>
							<div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
								<img
									:src="message.created_by.get_avatar"
									class="w-[40px] rounded-full"
								/>
							</div>
						</div>

						<div v-else class="flex w-full mt-2 space-x-3 max-w-md">
							<div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
								<img
									:src="message.created_by.get_avatar"
									class="w-[40px] rounded-full"
								/>
							</div>

							<div>
								<div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
									<p class="text-sm">
										{{ message.body }}
									</p>
								</div>
								<span class="text-xs text-gray-500 leading-none">{{
									message.created_at_formatted
								}}</span>
							</div>
						</div>
					</template>
				</div>
			</div>

			<div class="bg-white border border-gray-200 rounded-lg">
				<form @submit.prevent="submitForm" method="post">
					<div class="p-4">
						<textarea
							v-model="body"
							class="p-4 w-full bg-gray-100 rounded-lg"
							placeholder="请输入你想说的话..."
						></textarea>
					</div>

					<div class="p-4 border-t border-gray-100 flex justify-between">
						<button
							class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg"
						>
							发送
						</button>
					</div>
				</form>
			</div>
		</div>
	</div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const conversations = ref([])
const activeConversation = ref({})
const body = ref('')

function setActiveConversation(id) {
	console.log('setActiveConversation ', id)

	activeConversation.value = id
	getMessages()
}

function getConversations() {
	axios
		.get('/api/chat/')
		.then((res) => {
			console.log('conversations :>> ', res.data)

			// get all conversations
			conversations.value = res.data
			if (conversations.value.length) {
				activeConversation.value = conversations.value[0].id
			}

			getMessages()
		})
		.catch((error) => {
			console.log('error :>> ', error)
		})
}

function getMessages() {
	// console.log('getMessage')

	axios.get(`/api/chat/${activeConversation.value}/`).then((res) => {
		console.log('messages :>> ', res.data)

		activeConversation.value = res.data
	})
}

function submitForm() {
	// console.log('submitForm :>> ', body.value)
	axios
		.post(`/api/chat/${activeConversation.value.id}/send/`, {
			body: body.value,
		})
		.then((res) => {
			console.log('res :>> ', res.data)
			activeConversation.value.messages.push(res.data)
		})
		.catch((error) => {
			console.log('error :>> ', error)
		})
}

onMounted(() => {
	getConversations()
})
</script>
