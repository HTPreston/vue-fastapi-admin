import {RouteRecordRaw} from 'vue-router';
import {storeToRefs} from "/@/stores";
import {formatFlatteningRoutes, formatTwoStageRoutes, router} from '/@/router/index';
import {dynamicRoutes, notFoundAndNoPower} from '/@/router/route';
import {Session} from '/@/utils/storage';
import {useUserStore} from '/@/stores/user';
import {useTagsViewRoutes} from '/@/stores/tagsViewRoutes';
import {useRoutesList} from '/@/stores/routesList';
import {NextLoading} from '/@/utils/loading';

// 前端控制路由

/**
 * 前端控制路由：初始化方法，防止刷新时路由丢失
 * @method  NextLoading 界面 loading 动画开始执行
 * @method useUserStore(pinia).setUserInfos() 触发初始化用户信息 pinia
 * @method setAddRoute 添加动态路由
 * @method setFilterMenuAndCacheTagsViewRoutes 设置递归过滤有权限的路由到 pinia routesList 中（已处理成多级嵌套路由）及缓存多级嵌套数组处理后的一维数组
 */
export async function initFrontEndControlRoutes() {
	// 界面 loading 动画开始执行
	if (window.nextLoading === undefined) NextLoading.start();
	// 无 token 停止执行下一步
	if (!Session.get('token')) {
		NextLoading.done();
		return false;
	}
	
	try {
		// 触发初始化用户信息 pinia
		await useUserStore().setUserInfos();
		// 无登录权限时，添加判断
		// if (useUserStore().userInfos.roles.length <= 0) return Promise.resolve(true);
		// 添加动态路由
		await setAddRoute();
		// 设置递归过滤有权限的路由到 pinia routesList 中（已处理成多级嵌套路由）及缓存多级嵌套数组处理后的一维数组
		setFilterMenuAndCacheTagsViewRoutes();
	} catch (error) {
		console.error('初始化前端路由失败:', error);
		// 即使出错也要设置 isGet 为 true，防止无限循环
		const storesRoutesList = useRoutesList();
		storesRoutesList.setIsGet(true);
	} finally {
		// 结束 loading 动画
		NextLoading.done();
	}
}

/**
 * 添加动态路由
 * @method router.addRoute
 * @description 此处循环为 dynamicRoutes（/@/router/route）第一个顶级 children 的路由一维数组，非多级嵌套
 * @link 参考：https://next.router.vuejs.org/zh/api/#addroute
 */
export async function setAddRoute() {
	// 先删除所有动态路由，避免重复添加
	if (dynamicRoutes[0]?.children) {
		dynamicRoutes[0].children.forEach((route: RouteRecordRaw) => {
			const routeName = route.name;
			if (routeName) router.hasRoute(routeName) && router.removeRoute(routeName);
		});
	}
	
	// 添加动态路由
	setFilterRouteEnd().forEach((route: RouteRecordRaw) => {
		router.addRoute(route);
	});
}

/**
 * 删除/重置路由
 * @method router.removeRoute
 * @description 此处循环为 dynamicRoutes（/@/router/route）第一个顶级 children 的路由一维数组，非多级嵌套
 * @link 参考：https://next.router.vuejs.org/zh/api/#push
 */
export async function frontEndsResetRoute() {
	await setFilterRouteEnd().forEach((route: any) => {
		const routeName = route.name;
		router.hasRoute(routeName) && router.removeRoute(routeName);
	});
}

/**
 * 获取有当前用户权限标识的路由数组，进行对原路由的替换
 * @description 替换 dynamicRoutes（/@/router/route）第一个顶级 children 的路由
 * @returns 返回替换后的路由数组
 */
export function setFilterRouteEnd() {
	let filterRouteEnd: any = formatTwoStageRoutes(formatFlatteningRoutes(dynamicRoutes));
	// notFoundAndNoPower 防止 404、401 不在 layout 布局中，不设置的话，404、401 界面将全屏显示
	// 关联问题 No match found for location with path 'xxx'
	if (filterRouteEnd[0] && filterRouteEnd[0].children) {
		filterRouteEnd[0].children = [...setFilterRoute(filterRouteEnd[0].children), ...notFoundAndNoPower];
	}
	return filterRouteEnd;
}

/**
 * 获取当前用户权限标识去比对路由表（未处理成多级嵌套路由）
 * @description 这里主要用于动态路由的添加，router.addRoute
 * @link 参考：https://next.router.vuejs.org/zh/api/#addroute
 * @param chil dynamicRoutes（/@/router/route）第一个顶级 children 的下路由集合
 * @returns 返回有当前用户权限标识的路由数组
 */
export function setFilterRoute(chil: any) {
	const stores = useUserStore();
	const {userInfos} = storeToRefs(stores);
	let filterRoute: any = [];
	// 确保 chil 是数组
	if (Array.isArray(chil)) {
		chil.forEach((route: any) => {
			// 检查路由是否有权限要求
			if (route.meta?.roles) {
				// 检查用户是否有对应权限
				const hasPermission = route.meta.roles.some((metaRoles: any) => 
					userInfos.value.roles.includes(metaRoles)
				);
				if (hasPermission) {
					filterRoute.push({...route});
				}
			} else {
				// 没有权限要求的路由默认允许访问
				filterRoute.push({...route});
			}
		});
	}
	return filterRoute;
}

/**
 * 缓存多级嵌套数组处理后的一维数组
 * @description 用于 tagsView、菜单搜索中：未过滤隐藏的(isHide)
 */
export function setCacheTagsViewRoutes() {
	// 获取有权限的路由，否则 tagsView、菜单搜索中无权限的路由也将显示
	const stores = useUserStore();
	const storesTagsView = useTagsViewRoutes();
	const {userInfos} = storeToRefs(stores);
	let rolesRoutes = setFilterHasRolesMenu(dynamicRoutes, userInfos.value.roles);
	// 添加到 pinia setTagsViewRoutes 中
	const formattedRoutes = formatTwoStageRoutes(formatFlatteningRoutes(rolesRoutes));
	storesTagsView.setTagsViewRoutes(formattedRoutes[0]?.children || []);
}

/**
 * 设置递归过滤有权限的路由到 pinia routesList 中（已处理成多级嵌套路由）及缓存多级嵌套数组处理后的一维数组
 * @description 用于左侧菜单、横向菜单的显示
 * @description 用于 tagsView、菜单搜索中：未过滤隐藏的(isHide)
 */
export function setFilterMenuAndCacheTagsViewRoutes() {
	const stores = useUserStore();
	const storesRoutesList = useRoutesList();
	const {userInfos} = storeToRefs(stores);
	// 确保 dynamicRoutes[0] 和 dynamicRoutes[0].children 存在
	const childrenRoutes = dynamicRoutes[0]?.children || [];
	storesRoutesList.setRoutesList(setFilterHasRolesMenu(childrenRoutes, userInfos.value.roles));
	storesRoutesList.setIsGet(true); // 设置 isGet 为 true，防止重复初始化
	setCacheTagsViewRoutes();
}

/**
 * 判断路由 `meta.roles` 中是否包含当前登录用户权限字段
 * @param roles 用户权限标识，在 userInfos（用户信息）的 roles（登录页登录时缓存到浏览器）数组
 * @param route 当前循环时的路由项
 * @returns 返回对比后有权限的路由项
 */
export function hasRoles(roles: any, route: any) {
	if (route.meta && route.meta.roles) return roles.some((role: any) => route.meta.roles.includes(role));
	else return true;
}

/**
 * 获取当前用户权限标识去比对路由表，设置递归过滤有权限的路由
 * @param routes 当前路由 children
 * @param roles 用户权限标识，在 userInfos（用户信息）的 roles（登录页登录时缓存到浏览器）数组
 * @returns 返回有权限的路由数组 `meta.roles` 中控制
 */
export function setFilterHasRolesMenu(routes: any, roles: any) {
	const menu: any = [];
	// 确保 routes 是数组
	if (Array.isArray(routes)) {
		routes.forEach((route: any) => {
			const item = {...route};
			if (hasRoles(roles, item)) {
				if (item.children) item.children = setFilterHasRolesMenu(item.children, roles);
				menu.push(item);
			}
		});
	}
	return menu;
}
