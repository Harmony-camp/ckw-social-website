<template>
	<div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
		<div class="main-left">
			<div class="p-12 bg-white border border-gray-200 rounded-lg">
				<h1 class="mb-6 text-2xl">登录</h1>
				<p class="mb-6 text-gray-500">
					Lorem ipsum, dolor sit amet consectetur adipisicing elit. Harum at
					minima saepe quo dolore quam obcaecati sint voluptatibus, error natus
					pariatur numquam sapiente consectetur rem velit id, sit vitae aliquid!
				</p>

				<p class="font-bold">
					没有账号？<RouterLink :to="{ name: 'signup' }" class="underline"
						>请点击这里</RouterLink
					>
					注册新账号以登录！
				</p>
			</div>
		</div>
		<div class="main-right">
			<div class="p-12 bg-white border border-gray-200 rounded-lg">
				<form class="space-y-6">
					<div>
						<label>邮箱账号</label><br />
						<input
							type="email"
							placeholder="请输入邮箱地址"
							class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
						/>
					</div>
					<div>
						<label>密码</label><br />
						<input
							type="password"
							placeholder="请输入密码"
							class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
						/>
					</div>

					<div>
						<button class="py-4 px-6 bg-purple-600 text-white rounded-lg">
							登录
						</button>
					</div>
				</form>
			</div>
		</div>
	</div>
</template>
