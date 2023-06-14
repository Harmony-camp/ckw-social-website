<template>
	<div
		v-if="store.isVisible"
		class="transition easr-in-out dalay-500 duration-500 px-6 py-6 fixed top-full rounded-xl shadow-xl"
		:class="store.classes"
	>
		{{ store.message }}
	</div>
</template>

<script setup>
import { useToastStore } from '@/stores/toast'
const store = useToastStore()
</script>
