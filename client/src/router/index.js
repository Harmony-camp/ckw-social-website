import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import FeedView from '../views/FeedView.vue'
import MessagesView from '../views/MessagesView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'
import EditProfileView from '../views/EditProfileView.vue'
import EditPasswordView from '../views/EditPasswordView.vue'
import PostView from '../views/PostView.vue'
import FriendsView from '../views/FriendsView.vue'
import ChatView from '../views/ChatView.vue'
import TrendView from '../views/TrendView.vue'
import NotificationsView from '../views/NotificationsView.vue'

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: '/',
			name: 'home',
			component: FeedView,
		},
		{
			path: '/feed',
			name: 'feed',
			component: FeedView,
		},
		{
			path: '/messages',
			name: 'messages',
			component: MessagesView,
		},
		{
			path: '/chat',
			name: 'chat',
			component: ChatView,
		},
		{
			path: '/notifications',
			name: 'notifications',
			component: NotificationsView,
		},
		{
			path: '/search',
			name: 'search',
			component: SearchView,
		},
		{
			path: '/profile/:id',
			name: 'profile',
			component: ProfileView,
		},
		{
			path: '/profile/edit',
			name: 'editprofile',
			component: EditProfileView,
		},
		{
			path: '/profile/edit/password',
			name: 'editpassword',
			component: EditPasswordView,
		},
		{
			path: '/profile/:id/friends',
			name: 'friends',
			component: FriendsView,
		},
		{
			path: '/:id',
			name: 'postview',
			component: PostView,
		},
		{
			path: '/trends/:id',
			name: 'trendview',
			component: TrendView,
		},
		{
			path: '/signup',
			name: 'signup',
			component: SignupView,
		},
		{
			path: '/login',
			name: 'login',
			component: LoginView,
		},
	],
})

export default router
