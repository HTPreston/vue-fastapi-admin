import type { App } from 'vue';
import { useUserStore } from '/@/stores/user';
import { judementSameArr } from '/@/utils/arrayOperation';

/**
 * 用户权限指令
 * @directive 单个权限验证（v-auth="xxx"）
 * @directive 多个权限验证，满足一个则显示（v-auths="[xxx,xxx]"）
 * @directive 多个权限验证，全部满足则显示（v-auth-all="[xxx,xxx]"）
 */
export function authDirective(app: App) {
	// 单个权限验证（v-auth="xxx"）
	app.directive('auth', {
		mounted(el, binding) {
			const stores = useUserStore();
			
			// 立即执行权限检查
			const checkPermission = () => {
				const hasPermission = stores.userInfos.authBtnList.some((v: string) => v === binding.value);
				if (!hasPermission) {
					// 使用 CSS 隐藏按钮
					el.style.display = 'none';
					el.setAttribute('hidden', 'true');
				} else {
					// 显示按钮
					el.style.display = '';
					el.removeAttribute('hidden');
				}
			};
			
			// 检查用户信息是否已加载（id 存在表示用户信息已加载）
			if (stores.userInfos.id) {
				// 用户信息已加载，直接检查权限
				checkPermission();
			} else {
				// 如果用户信息还未加载，等待加载完成后再检查
				const interval = setInterval(() => {
					if (stores.userInfos.id) {
						checkPermission();
						clearInterval(interval);
					}
				}, 100);
				// 最多检查10秒
				setTimeout(() => clearInterval(interval), 10000);
			}
			
			// 使用 $subscribe 监听 store 变化
			const unsubscribe = stores.$subscribe((mutation, state) => {
				if (state.userInfos.id) {
					checkPermission();
				}
			});
			
			// 在元素被移除时停止监听
			(el as any).__unsubscribe = unsubscribe;
		},
		unmounted(el) {
			// 停止监听
			if ((el as any).__unsubscribe) {
				(el as any).__unsubscribe();
			}
		},
	});
	// 多个权限验证，满足一个则显示（v-auths="[xxx,xxx]"）
	app.directive('auths', {
		mounted(el, binding) {
			const stores = useUserStore();
			
			// 立即执行权限检查
			const checkPermission = () => {
				let flag = false;
				stores.userInfos.authBtnList.map((val: string) => {
					binding.value.map((v: string) => {
						if (val === v) flag = true;
					});
				});
				if (!flag) {
					// 使用 CSS 隐藏按钮
					el.style.display = 'none';
					el.setAttribute('hidden', 'true');
				} else {
					// 显示按钮
					el.style.display = '';
					el.removeAttribute('hidden');
				}
			};
			
			// 检查用户信息是否已加载（id 存在表示用户信息已加载）
			if (stores.userInfos.id) {
				// 用户信息已加载，直接检查权限
				checkPermission();
			} else {
				// 如果用户信息还未加载，等待加载完成后再检查
				const interval = setInterval(() => {
					if (stores.userInfos.id) {
						checkPermission();
						clearInterval(interval);
					}
				}, 100);
				// 最多检查10秒
				setTimeout(() => clearInterval(interval), 10000);
			}
		},
	});
	// 多个权限验证，全部满足则显示（v-auth-all="[xxx,xxx]"）
	app.directive('auth-all', {
		mounted(el, binding) {
			const stores = useUserStore();
			
			// 立即执行权限检查
			const checkPermission = () => {
				const flag = judementSameArr(binding.value, stores.userInfos.authBtnList);
				if (!flag) {
					// 使用 CSS 隐藏按钮
					el.style.display = 'none';
					el.setAttribute('hidden', 'true');
				} else {
					// 显示按钮
					el.style.display = '';
					el.removeAttribute('hidden');
				}
			};
			
			// 检查用户信息是否已加载（id 存在表示用户信息已加载）
			if (stores.userInfos.id) {
				// 用户信息已加载，直接检查权限
				checkPermission();
			} else {
				// 如果用户信息还未加载，等待加载完成后再检查
				const interval = setInterval(() => {
					if (stores.userInfos.id) {
						checkPermission();
						clearInterval(interval);
					}
				}, 100);
				// 最多检查10秒
				setTimeout(() => clearInterval(interval), 10000);
			}
		},
	});
}
