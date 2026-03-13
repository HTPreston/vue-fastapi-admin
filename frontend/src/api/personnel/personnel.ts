import request from '/@/utils/request';

/**
 * 获取人员信息列表
 * @param params 查询参数
 * @returns 返回人员信息列表
 */
export function getPersonnelList(params: any) {
    return request({
        url: '/personnel/list',
        method: 'post',
        data: params
    });
}

/**
 * 根据ID获取人员信息
 * @param id 人员ID
 * @returns 返回人员信息
 */
export function getPersonnelById(id: number) {
    return request({
        url: '/personnel/get',
        method: 'post',
        data: {id}
    });
}

/**
 * 新增人员信息
 * @param params 人员信息
 * @returns 返回操作结果
 */
export function createPersonnel(params: any) {
    return request({
        url: '/personnel/create',
        method: 'post',
        data: params
    });
}

/**
 * 更新人员信息
 * @param params 人员信息
 * @returns 返回操作结果
 */
export function updatePersonnel(params: any) {
    return request({
        url: '/personnel/update',
        method: 'post',
        data: params
    });
}

/**
 * 删除人员信息
 * @param id 人员ID
 * @returns 返回操作结果
 */
export function deletePersonnel(id: number) {
    return request({
        url: '/personnel/delete',
        method: 'post',
        data: {id}
    });
}

/**
 * 获取员工资质证书列表
 * @param params 查询参数
 * @returns 返回员工资质证书列表
 */
export function getQualificationList(params: any) {
    return request({
        url: '/personnel/qualification/list',
        method: 'post',
        data: params
    });
}

/**
 * 根据ID获取员工资质证书
 * @param id 证书ID
 * @returns 返回员工资质证书
 */
export function getQualificationById(id: number) {
    return request({
        url: '/personnel/qualification/get',
        method: 'post',
        data: {id}
    });
}

/**
 * 新增员工资质证书
 * @param params 员工资质证书信息
 * @returns 返回操作结果
 */
export function createQualification(params: any) {
    return request({
        url: '/personnel/qualification/create',
        method: 'post',
        data: params
    });
}

/**
 * 更新员工资质证书
 * @param params 员工资质证书信息
 * @returns 返回操作结果
 */
export function updateQualification(params: any) {
    return request({
        url: '/personnel/qualification/update',
        method: 'post',
        data: params
    });
}

/**
 * 删除员工资质证书
 * @param id 证书ID
 * @returns 返回操作结果
 */
export function deleteQualification(id: number) {
    return request({
        url: '/personnel/qualification/delete',
        method: 'post',
        data: {id}
    });
}
