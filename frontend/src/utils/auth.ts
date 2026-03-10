import { useUserStore } from '/@/stores/user';

/**
 * 检查用户是否有指定权限
 * @param permission 权限标识
 * @returns 是否有权限
 */
export function hasPermission(permission: string): boolean {
	const userStore = useUserStore();
	// 确保 authBtnList 存在且是数组
	if (!userStore.userInfos || !userStore.userInfos.authBtnList) {
		console.log('No authBtnList available');
		return false;
	}
	// 打印权限检查信息，方便调试
	console.log('Checking permission:', permission);
	console.log('Available permissions:', userStore.userInfos.authBtnList);
	const hasPerm = userStore.userInfos.authBtnList.includes(permission);
	console.log('Permission check result:', hasPerm);
	return hasPerm;
}

/**
 * 检查用户是否有任意一个指定权限
 * @param permissions 权限标识数组
 * @returns 是否有任意一个权限
 */
export function hasAnyPermission(permissions: string[]): boolean {
	const userStore = useUserStore();
	// 确保 authBtnList 存在且是数组
	if (!userStore.userInfos || !userStore.userInfos.authBtnList) {
		return false;
	}
	return permissions.some(permission => userStore.userInfos.authBtnList.includes(permission));
}

/**
 * 检查用户是否有所有指定权限
 * @param permissions 权限标识数组
 * @returns 是否有所有权限
 */
export function hasAllPermissions(permissions: string[]): boolean {
	const userStore = useUserStore();
	// 确保 authBtnList 存在且是数组
	if (!userStore.userInfos || !userStore.userInfos.authBtnList) {
		return false;
	}
	return permissions.every(permission => userStore.userInfos.authBtnList.includes(permission));
}
