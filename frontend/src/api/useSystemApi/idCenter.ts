import request from '/@/utils/request';

/**
 * 个人中心接口
 * @method getUserInfo 获取个人信息
 * @method updateProfile 更新个人信息
 * @method updateAvatar 更新头像
 * @method updatePhone 更新手机号
 * @method updateEmail 更新邮箱
 * @method resetPassword 修改密码
 * @method getMenu 获取个人菜单权限
 */
export function useIdCenterApi() {
  return {
    // 获取个人信息
    getUserInfo: () => {
      return request({
        url: '/profile/getUserInfo',
        method: 'POST',
        data: {},
      });
    },
    // 更新个人信息（批量）
    updateProfile: (data?: object) => {
      return request({
        url: '/profile/updateProfile',
        method: 'POST',
        data,
      });
    },
    // 更新头像
    updateAvatar: (data?: object) => {
      return request({
        url: '/profile/updateAvatar',
        method: 'POST',
        data,
      });
    },
    // 更新手机号
    updatePhone: (data?: object) => {
      return request({
        url: '/profile/updatePhone',
        method: 'POST',
        data,
      });
    },
    // 更新邮箱
    updateEmail: (data?: object) => {
      return request({
        url: '/profile/updateEmail',
        method: 'POST',
        data,
      });
    },
    // 修改密码
    resetPassword: (data?: object) => {
      return request({
        url: '/profile/resetPassword',
        method: 'POST',
        data,
      });
    },
    // 获取个人菜单权限
    getMenu: () => {
      return request({
        url: '/profile/getMenu',
        method: 'POST',
        data: {},
      });
    },
    // 获取登录记录
    getLoginRecords: (data?: object) => {
      return request({
        url: '/profile/getLoginRecords',
        method: 'POST',
        data,
      });
    },
  };
}
