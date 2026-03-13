import {RouteRecordRaw} from 'vue-router';
import {useUserStore} from '/@/stores/user';
import {useRequestOldRoutes} from '/@/stores/requestOldRoutes';
import {Session} from '/@/utils/storage';
import {NextLoading} from '/@/utils/loading';
import {dynamicRoutes, notFoundAndNoPower} from '/@/router/route';
import {formatFlatteningRoutes, formatTwoStageRoutes, router} from '/@/router';
import {useRoutesList} from '/@/stores/routesList';
import {useTagsViewRoutes} from '/@/stores/tagsViewRoutes';
import {useUserApi} from '/@/api/useSystemApi/user';

import {useMenuInfo} from "/@/stores/menu";


/**
 * 获取目录下的 .vue、.tsx 全部文件
 * @method import.meta.glob
 * @link 参考：https://cn.vitejs.dev/guide/features.html#json
 */
const layoutModules: any = import.meta.glob('../layout/routerView/*.{vue,tsx}');
const viewsModules: any = import.meta.glob('../views/**/*.{vue,tsx}');
const dynamicViewsModules = Object.assign({}, {...layoutModules}, {...viewsModules});

/**
 * 后端控制路由：初始化方法，防止刷新时路由丢失
 * @method NextLoading 界面 loading 动画开始执行
 * @method useUserStore().setUserInfos() 触发初始化用户信息 pinia
 * @method useRequestOldRoutes().setRequestOldRoutes() 存储接口原始路由（未处理component），根据需求选择使用
 * @method setAddRoute 添加动态路由
 * @method setFilterMenuAndCacheTagsViewRoutes 设置路由到 pinia routesList 中（已处理成多级嵌套路由）及缓存多级嵌套数组处理后的一维数组
 */
export async function initBackEndControlRoutes() {
	// 界面 loading 动画开始执行
	if (window.nextLoading === undefined) NextLoading.start();
	// 无 token 停止执行下一步
	if (!Session.get('token')) return false;
	// 触发初始化用户信息 pinia
	await useUserStore().setUserInfos(true); // 强制刷新用户信息
	// 获取路由菜单数据
	const menuData = await useMenuInfo().getMenuData();
	console.log('[initBackEndControlRoutes] 菜单数据:', menuData);
	
	// 检查菜单数据中是否有重复的路由
	if (menuData && Array.isArray(menuData)) {
		const menuPaths = new Set();
		const checkDuplicate = (routes: any[]) => {
			routes.forEach(route => {
				if (menuPaths.has(route.path)) {
					console.warn('[initBackEndControlRoutes] 发现重复路由:', route.path);
				}
				menuPaths.add(route.path);
				if (route.children) {
					checkDuplicate(route.children);
				}
			});
		};
		checkDuplicate(menuData);
	}
	
	// 存储接口原始路由（未处理component），根据需求选择使用
	await useRequestOldRoutes().setRequestOldRoutes(JSON.parse(JSON.stringify(menuData)));
	// 处理路由（component），替换 dynamicRoutes（/@/router/route）第一个顶级 children 的路由
	dynamicRoutes[0].children = backEndComponent(menuData);
	// 添加动态路由
	setAddRoute();
	// 设置路由到 pinia routesList 中（已处理成多级嵌套路由）及缓存多级嵌套数组处理后的一维数组
	await setFilterMenuAndCacheTagsViewRoutes();

}

/**
 * 设置路由到 pinia routesList 中（已处理成多级嵌套路由）及缓存多级嵌套数组处理后的一维数组
 * @description 用于左侧菜单、横向菜单的显示
 * @description 用于 tagsView、菜单搜索中：未过滤隐藏的(isHide)
 */
export async function setFilterMenuAndCacheTagsViewRoutes() {
	const storesRoutesList = useRoutesList();
	const children = dynamicRoutes[0]?.children || [];
	console.log('[setFilterMenuAndCacheTagsViewRoutes] 设置路由列表，数量:', children.length);
	await storesRoutesList.setRoutesList(children as any);
	await storesRoutesList.setIsGet(true);
	setCacheTagsViewRoutes();
	console.log('[setFilterMenuAndCacheTagsViewRoutes] 路由列表设置完成');
}

/**
 * 缓存多级嵌套数组处理后的一维数组
 * @description 用于 tagsView、菜单搜索中：未过滤隐藏的(isHide)
 */
export function setCacheTagsViewRoutes() {
	const storesTagsView = useTagsViewRoutes();
	const tagsViewRoutes = formatTwoStageRoutes(formatFlatteningRoutes(dynamicRoutes));
	if (tagsViewRoutes && tagsViewRoutes[0] && tagsViewRoutes[0].children) {
		storesTagsView.setTagsViewRoutes(tagsViewRoutes[0].children);
	}
}

/**
 * 处理路由格式及添加捕获所有路由或 404 Not found 路由
 * @description 替换 dynamicRoutes（/@/router/route）第一个顶级 children 的路由
 * @returns 返回替换后的路由数组
 */
export function setFilterRouteEnd() {
	let filterRouteEnd = formatTwoStageRoutes(formatFlatteningRoutes(dynamicRoutes));
	// notFoundAndNoPower 防止 404、401 不在 layout 布局中，不设置的话，404、401 界面将全屏显示
	// 关联问题 No match found for location with path 'xxx'
	// 使用深拷贝避免修改原始数组
	if (filterRouteEnd && filterRouteEnd[0] && filterRouteEnd[0].children) {
		filterRouteEnd[0].children = [...filterRouteEnd[0].children, ...notFoundAndNoPower];
	}
	return filterRouteEnd;
}

/**
 * 删除/重置路由
 * @method router.removeRoute
 * @description 此处循环为 dynamicRoutes（/@/router/route）第一个顶级 children 的路由一维数组，非多级嵌套
 * @link 参考：https://next.router.vuejs.org/zh/api/#push
 */
export function backEndsResetRoute() {
	console.log('[backEndsResetRoute] 开始重置路由');
	// 只删除 dynamicRoutes 中的路由，不删除 notFoundAndNoPower 中的路由
	const filterRouteEnd = formatTwoStageRoutes(formatFlatteningRoutes(dynamicRoutes));
	if (filterRouteEnd && filterRouteEnd[0] && filterRouteEnd[0].children) {
		filterRouteEnd[0].children.forEach((route: any) => {
			const routeName = route.name;
			if (routeName && router.hasRoute(routeName)) {
				console.log('[backEndsResetRoute] 删除路由:', routeName);
				router.removeRoute(routeName);
			}
		});
	}
	console.log('[backEndsResetRoute] 路由重置完成');
}

/**
 * 添加动态路由
 * @method router.addRoute
 * @description 此处循环为 dynamicRoutes（/@/router/route）第一个顶级 children 的路由一维数组，非多级嵌套
 * @link 参考：https://next.router.vuejs.org/zh/api/#addroute
 */
export function setAddRoute() {
	// 先删除已有的路由，避免重复添加
	backEndsResetRoute();
	const routes = setFilterRouteEnd();
	if (routes && Array.isArray(routes)) {
		console.log('[setAddRoute] 准备添加路由数量:', routes.length);
		routes.forEach((route: RouteRecordRaw) => {
			console.log('[setAddRoute] 添加路由:', route.name, route.path);
			router.addRoute(route);
		});
		console.log('[setAddRoute] 路由添加完成');
	} else {
		console.log('[setAddRoute] 没有路由需要添加');
	}
}

/**
 * 请求后端路由菜单接口
 * @description isRequestRoutes 为 true，则开启后端控制路由
 * @returns 返回后端路由菜单数据
 */
export async function getBackEndControlRoutes() {
	let {data} = await useUserApi().getMenuByToken()
	return data
}

/**
 * 重新请求后端路由菜单接口
 * @description 用于菜单管理界面刷新菜单（未进行测试）
 * @description 路径：/src/views/system/menu/component/addMenu.vue
 */
export async function setBackEndControlRefreshRoutes() {
	await getBackEndControlRoutes();
}

/**
 * 后端路由 component 转换
 * @param routes 后端返回的路由表数组
 * @returns 返回处理成函数后的 component
 */
export function backEndComponent(routes: any) {
	if (!routes || !Array.isArray(routes)) return [];
	return routes.map((item: any) => {
		// 修复路由 component 路径：如果 component 是 layout/routerView/parent 但路径对应 views 目录下的页面
		if (item.component === 'layout/routerView/parent' && item.path) {
			// 提取路径中的名称（如 /personnel -> personnel）
			const pathName = item.path.replace(/^\//, '').split('/')[0];
			// 检查是否存在对应的 views 目录下的组件
			const possibleComponent = `${pathName}/index`;
			const keys = Object.keys(dynamicViewsModules);
			const matchKeys = keys.filter((key) => {
				const k = key.replace(/\.\.\/views|\.\./, '');
				return k.startsWith(`/${possibleComponent}`) || k.startsWith(`${possibleComponent}`);
			});
			if (matchKeys.length === 1) {
				item.component = possibleComponent;
				console.log('[backEndComponent] 修复路由 component:', item.path, '->', item.component);
			}
		}
		if (item.component) item.component = dynamicImport(dynamicViewsModules, item.component);
		if (item.children && Array.isArray(item.children)) {
			item.children = backEndComponent(item.children);
		}
		return item;
	});
}

/**
 * 后端路由 component 转换函数
 * @param dynamicViewsModules 获取目录下的 .vue、.tsx 全部文件
 * @param component 当前要处理项 component
 * @returns 返回处理成函数后的 component
 */
export function dynamicImport(dynamicViewsModules: Record<string, Function>, component: string) {
	const keys = Object.keys(dynamicViewsModules);
	const matchKeys = keys.filter((key) => {
		const k = key.replace(/..\/views|../, '');
		return k.startsWith(`${component}`) || k.startsWith(`/${component}`);
	});
	if (matchKeys?.length === 1) {
		const matchKey = matchKeys[0];
		return dynamicViewsModules[matchKey];
	}
	if (matchKeys?.length > 1) {
		return false;
	}
}
