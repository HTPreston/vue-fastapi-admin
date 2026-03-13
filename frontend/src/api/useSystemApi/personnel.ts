import request from '/@/utils/request';

/**
 * 人员管理接口
 * @method getList 获取人员列表
 * @method getById 根据ID获取人员信息
 * @method create 新增人员
 * @method update 更新人员
 * @method delete 删除人员
 */
export function usePersonnelApi() {
  return {
    // 获取人员列表
    getList: (data?: object) => {
      return request({
        url: '/personnel/list',
        method: 'POST',
        data,
      });
    },
    // 根据ID获取人员信息
    getById: (id: number) => {
      return request({
        url: '/personnel/get',
        method: 'POST',
        data: {id},
      });
    },
    // 新增人员
    create: (data?: object) => {
      return request({
        url: '/personnel/create',
        method: 'POST',
        data,
      });
    },
    // 更新人员
    update: (data?: object) => {
      return request({
        url: '/personnel/update',
        method: 'POST',
        data,
      });
    },
    // 删除人员
    delete: (id: number) => {
      return request({
        url: '/personnel/delete',
        method: 'POST',
        data: {id},
      });
    },
  };
}

/**
 * 员工资质证书接口
 * @method getList 获取资质证书列表
 * @method getById 根据ID获取资质证书
 * @method create 新增资质证书
 * @method update 更新资质证书
 * @method delete 删除资质证书
 */
export function useQualificationApi() {
  return {
    // 获取资质证书列表
    getList: (data?: object) => {
      return request({
        url: '/personnel/qualification/list',
        method: 'POST',
        data,
      });
    },
    // 根据ID获取资质证书
    getById: (id: number) => {
      return request({
        url: '/personnel/qualification/get',
        method: 'POST',
        data: {id},
      });
    },
    // 新增资质证书
    create: (data?: object) => {
      return request({
        url: '/personnel/qualification/create',
        method: 'POST',
        data,
      });
    },
    // 更新资质证书
    update: (data?: object) => {
      return request({
        url: '/personnel/qualification/update',
        method: 'POST',
        data,
      });
    },
    // 删除资质证书
    delete: (id: number) => {
      return request({
        url: '/personnel/qualification/delete',
        method: 'POST',
        data: {id},
      });
    },
  };
}
