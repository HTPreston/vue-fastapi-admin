/**
 * 按钮权限常量定义
 */

// 通用按钮权限
export const BUTTON_PERMISSIONS = {
  // 用户管理
  USER_ADD: 'user:add',
  USER_EDIT: 'user:edit',
  USER_DELETE: 'user:delete',
  USER_VIEW: 'user:view',

  // 角色管理
  ROLE_ADD: 'role:add',
  ROLE_EDIT: 'role:edit',
  ROLE_DELETE: 'role:delete',
  ROLE_VIEW: 'role:view',

  // 菜单管理
  MENU_ADD: 'menu:add',
  MENU_EDIT: 'menu:edit',
  MENU_DELETE: 'menu:delete',
  MENU_VIEW: 'menu:view',

  // 部门管理
  DEPT_ADD: 'dept:add',
  DEPT_EDIT: 'dept:edit',
  DEPT_DELETE: 'dept:delete',
  DEPT_VIEW: 'dept:view',

  // 字典管理
  DIC_ADD: 'dic:add',
  DIC_EDIT: 'dic:edit',
  DIC_DELETE: 'dic:delete',
  DIC_VIEW: 'dic:view',

  // 数据字典管理
  LOOKUP_ADD: 'lookup:add',
  LOOKUP_EDIT: 'lookup:edit',
  LOOKUP_DELETE: 'lookup:delete',
  LOOKUP_VIEW: 'lookup:view',

  // 系统设置
  SYSTEM_CONFIG: 'system:config',
  SYSTEM_BACKUP: 'system:backup',
  SYSTEM_RESTORE: 'system:restore',
} as const;

// 按钮权限列表
export const BUTTON_PERMISSION_LIST = Object.values(BUTTON_PERMISSIONS);

// 按钮权限树形结构
export const BUTTON_PERMISSION_TREE = [
  {
    id: 'system',
    title: '系统设置',
    children: [
      {
        id: 'user',
        title: '用户管理',
        children: [
          { id: BUTTON_PERMISSIONS.USER_ADD, title: '新增用户' },
          { id: BUTTON_PERMISSIONS.USER_EDIT, title: '编辑用户' },
          { id: BUTTON_PERMISSIONS.USER_DELETE, title: '删除用户' },
          { id: BUTTON_PERMISSIONS.USER_VIEW, title: '查看用户' },
        ],
      },
      {
        id: 'role',
        title: '角色管理',
        children: [
          { id: BUTTON_PERMISSIONS.ROLE_ADD, title: '新增角色' },
          { id: BUTTON_PERMISSIONS.ROLE_EDIT, title: '编辑角色' },
          { id: BUTTON_PERMISSIONS.ROLE_DELETE, title: '删除角色' },
          { id: BUTTON_PERMISSIONS.ROLE_VIEW, title: '查看角色' },
        ],
      },
      {
        id: 'menu',
        title: '菜单管理',
        children: [
          { id: BUTTON_PERMISSIONS.MENU_ADD, title: '新增菜单' },
          { id: BUTTON_PERMISSIONS.MENU_EDIT, title: '编辑菜单' },
          { id: BUTTON_PERMISSIONS.MENU_DELETE, title: '删除菜单' },
          { id: BUTTON_PERMISSIONS.MENU_VIEW, title: '查看菜单' },
        ],
      },
      {
        id: 'dept',
        title: '部门管理',
        children: [
          { id: BUTTON_PERMISSIONS.DEPT_ADD, title: '新增部门' },
          { id: BUTTON_PERMISSIONS.DEPT_EDIT, title: '编辑部门' },
          { id: BUTTON_PERMISSIONS.DEPT_DELETE, title: '删除部门' },
          { id: BUTTON_PERMISSIONS.DEPT_VIEW, title: '查看部门' },
        ],
      },
      {
        id: 'dic',
        title: '字典管理',
        children: [
          { id: BUTTON_PERMISSIONS.DIC_ADD, title: '新增字典' },
          { id: BUTTON_PERMISSIONS.DIC_EDIT, title: '编辑字典' },
          { id: BUTTON_PERMISSIONS.DIC_DELETE, title: '删除字典' },
          { id: BUTTON_PERMISSIONS.DIC_VIEW, title: '查看字典' },
        ],
      },
      {
        id: 'lookup',
        title: '数据字典管理',
        children: [
          { id: BUTTON_PERMISSIONS.LOOKUP_ADD, title: '新增数据字典' },
          { id: BUTTON_PERMISSIONS.LOOKUP_EDIT, title: '编辑数据字典' },
          { id: BUTTON_PERMISSIONS.LOOKUP_DELETE, title: '删除数据字典' },
          { id: BUTTON_PERMISSIONS.LOOKUP_VIEW, title: '查看数据字典' },
        ],
      },
      {
        id: 'system_ops',
        title: '系统操作',
        children: [
          { id: BUTTON_PERMISSIONS.SYSTEM_CONFIG, title: '系统配置' },
          { id: BUTTON_PERMISSIONS.SYSTEM_BACKUP, title: '系统备份' },
          { id: BUTTON_PERMISSIONS.SYSTEM_RESTORE, title: '系统恢复' },
        ],
      },
    ],
  },
];