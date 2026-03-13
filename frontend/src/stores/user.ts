import {defineStore} from 'pinia';
import {Session} from '/@/utils/storage';
import {useUserApi} from "/@/api/useSystemApi/user";

/**
 * 用户信息
 * @methods setUserInfos 设置用户信息
 */
export const useUserStore = defineStore('userInfo', {
	state: (): UserInfosState => ({
		userInfos: {
			id: null,
			authBtnList: [],
			buttons: [],
			avatar: '',
			roles: [],
			time: 0,
			username: '',
			phone: '',
			user_type: null,
			login_time: "",
			lastLoginTime: ""
		},
	}),

	actions: {
		async setUserInfos(force = false) {
			if (!force && Session.get('userInfo')) {
				this.userInfos = Session.get('userInfo');
			} else {
				this.userInfos = await this.getApiUserInfo();
				Session.set("userInfo", this.userInfos);
			}
		},
		async getApiUserInfo() {
		let {data} = await useUserApi().getUserInfoByToken();
		// 确保 buttons 字段存在且是数组
		if (!data.buttons) data.buttons = [];
		if (!Array.isArray(data.buttons)) data.buttons = [];
		// 过滤空字符串
		data.buttons = data.buttons.filter((btn: string) => btn.trim());
		// 转换权限标识格式：中文 -> 英文
		const convertPermission = (permission: string): string => {
			const moduleMap: Record<string, string> = {
				'用户': 'user',
				'菜单': 'menu',
				'角色': 'role',
				'部门': 'dept'
			};
			// 提取中文模块名和操作
			const match = permission.match(/^(.*?):(.*)$/);
			if (match) {
				const [, chineseModule, action] = match;
				const englishModule = moduleMap[chineseModule] || chineseModule;
				return `${englishModule.toLowerCase()}:${action}`;
			}
			return permission;
		};
		// 转换权限标识格式
		data.buttons = data.buttons.map(convertPermission);
		// 将 buttons 赋值给 authBtnList（只使用 buttons 字段）
		data.authBtnList = data.buttons;
		// 根据 role_type 生成 roles 字段
		// 这里根据后端返回的 role_type 映射到前端需要的角色名称
		// 注意：role_type 可能是字符串类型，需要进行类型转换
		const roleType = Number(data.role_type);
		if (!data.roles || !Array.isArray(data.roles)) {
			data.roles = [];
			// 根据 role_type 映射到对应的角色名称
			if (roleType === 10) {
				data.roles = ['super_admin'];
			} else if (roleType === 20) {
				data.roles = ['admin'];
			} else if (roleType === 30) {
				data.roles = ['common'];
			}
		}
		// 打印权限信息，方便调试
		console.log('User permissions:', data.buttons);
		console.log('User roles:', data.roles);
		console.log('User role_type:', data.role_type);
		return data;
	},
		async updateUserInfo(data: UserInfos) {
			this.userInfos = data;
			Session.set("userInfo", data);
		},
		async refreshPermissions() {
			this.userInfos = await this.getApiUserInfo();
			Session.set("userInfo", this.userInfos);
		}
	}
});
