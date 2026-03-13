import request from '/@/utils/request';

/**
 * 公司管理接口
 */
export function useCompanyApi() {
  return {
    // 获取公司列表
    getList: (data?: object) => {
      return request({
        url: '/company/list',
        method: 'POST',
        data,
      });
    },
    // 获取公司详情
    getById: (id: number) => {
      return request({
        url: '/company/get',
        method: 'POST',
        data: { id },
      });
    },
    // 新增公司
    create: (data?: object) => {
      return request({
        url: '/company/create',
        method: 'POST',
        data,
      });
    },
    // 更新公司
    update: (data?: object) => {
      return request({
        url: '/company/update',
        method: 'POST',
        data,
      });
    },
    // 删除公司
    delete: (id: number) => {
      return request({
        url: '/company/delete',
        method: 'POST',
        data: { id },
      });
    },
    // 获取公司资质证书列表
    getQualificationList: (data?: object) => {
      return request({
        url: '/company/qualification/list',
        method: 'POST',
        data,
      });
    },
    // 新增公司资质证书
    createQualification: (data?: object) => {
      return request({
        url: '/company/qualification/create',
        method: 'POST',
        data,
      });
    },
    // 更新公司资质证书
    updateQualification: (data?: object) => {
      return request({
        url: '/company/qualification/update',
        method: 'POST',
        data,
      });
    },
    // 删除公司资质证书
    deleteQualification: (id: number) => {
      return request({
        url: '/company/qualification/delete',
        method: 'POST',
        data: { id },
      });
    },
  };
}
