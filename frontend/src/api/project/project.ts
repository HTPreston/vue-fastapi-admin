import request from '/@/utils/request';

/**
 * 项目管理接口
 */
export function useProjectApi() {
  return {
    // 获取项目列表
    getList: (data?: object) => {
      return request({
        url: '/project/list',
        method: 'POST',
        data,
      });
    },
    // 获取项目详情
    getById: (id: number) => {
      return request({
        url: '/project/get',
        method: 'POST',
        data: { id },
      });
    },
    // 新增项目
    create: (data?: object) => {
      return request({
        url: '/project/create',
        method: 'POST',
        data,
      });
    },
    // 更新项目
    update: (data?: object) => {
      return request({
        url: '/project/update',
        method: 'POST',
        data,
      });
    },
    // 删除项目
    delete: (id: number) => {
      return request({
        url: '/project/delete',
        method: 'POST',
        data: { id },
      });
    },
  };
}
