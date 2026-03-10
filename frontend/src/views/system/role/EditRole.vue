<template>
  <div class="system-edit-role-container">
    <el-dialog
        draggable :title="state.editType === 'save'? `新增` : `修改`" v-model="state.isShowDialog" width="769px">
      <el-form :model="state.form" :rules="state.rules" label-width="90px" ref="formRef">
        <el-row :gutter="35">
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="角色名称" prop="name">
              <el-input v-model="state.form.name" placeholder="请输入角色名称" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="角色类型" prop="role_type">
              <template #label>
                <el-tooltip effect="dark" content="10 超级管理员, 20 管理员, 30 普通用户" placement="top-start">
                  <span>角色类型</span>
                </el-tooltip>
              </template>
              <el-select v-model="state.form.role_type" clearable placeholder="选择角色类型">
                <el-option
                    v-for="item in [{role_type: 10, label:'超级管理员'},{role_type: 20, label:'管理员'},{role_type: 30, label:'普通用户'}]"
                    :key="item.role_type"
                    :label="item.label"
                    :value="item.role_type"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="角色状态">
              <el-switch v-model="state.form.status" :active-value="1" :inactive-value="0" inline-prompt
                         active-text="启用"
                         inactive-text="禁用"></el-switch>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="角色描述">
              <el-input v-model="state.form.description" type="textarea" placeholder="请输入角色描述"
                        maxlength="150"></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="权限设置">
              <div style="width: 100%; overflow-x: auto;">
                <p class="permission-label">菜单权限：</p>
                <el-tree ref="roleTreeRef"
                         :data="state.menuData"
                         :props="state.menuProps"
                         @check-change="roleTreeChange"
                         :default-expanded-keys="state.expandedKeys"
                         node-key="id"
                         show-checkbox
                         check-strictly
                         class="menu-data-tree"/>
              </div>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
		<span class="dialog-footer">
			<el-button @click="onCancel">取 消</el-button>
			<el-button type="primary" @click="saveOrUpdate">保 存</el-button>
		</span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup name="SaveOrUpdateRole">
import {reactive, ref, nextTick} from 'vue';
import {useMenuApi} from "/@/api/useSystemApi/menu";
import {useRolesApi} from "/@/api/useSystemApi/roles";
import {ElMessage} from "element-plus";
import { Session } from '/@/utils/storage';

// 定义接口来定义对象的类型
interface MenuDataTree {
  id: number | string;
  title: string;
  children?: MenuDataTree[];
}

interface RoleData {
  id?: string | number | null;
  name: string;
  role_type: number;
  menus: Array<number>;
  description: string;
  status: number;
  buttons: Array<string>;
}

interface RoleState {
  isShowDialog: boolean;
  editType: any;
  form: RoleData;
  rules: Object;
  menuData: Array<MenuDataTree>;
  menuProps: {
    children: string;
    label: string;
  };
  expandedKeys: Array<number | string>;
}

const emit = defineEmits(['getList'])

let createForm = () => {
  return {
    name: '',  // 角色名称
    role_type: 30,   // 角色类型
    menus: [],    // 关联菜单
    description: '',   //描述
    status: 1,   // 角色状态 1 启用，0 禁用
    buttons: [],  // 关联权限
  }
}
const formRef = ref()
const roleTreeRef = ref()
const state = reactive<RoleState>({
  editType: null,
  isShowDialog: false,
  form: createForm(),
  menuData: [],
  rules: {
    name: [{required: true, message: '请输入角色名称', trigger: 'blur'},],
    role_type: [{required: true, message: '请选择角色类型', trigger: 'blur'},],
  },
  menuProps: {
    children: 'children',
    label: 'title',
  },
  expandedKeys: [],
});
// 打开弹窗
const openDialog = async (editType: string, row: RoleData) => {
  console.log('openDialog called with:', editType, row);
  state.editType = editType;
  // 等待菜单和按钮权限加载完毕
  await getMenuData();
  if (row) {
    state.form = JSON.parse(JSON.stringify(row));
    // 确保 menus 和 buttons 是数组格式
    if (typeof (state.form as any).menus === 'string') {
      (state.form as any).menus = (state.form as any).menus.split(',').filter((id: string) => id !== '').map((id: string) => parseInt(id, 10));
    }
    if (typeof (state.form as any).buttons === 'string') {
      (state.form as any).buttons = (state.form as any).buttons.split(',').filter((id: string) => id !== '');
    }
    // 如果 menus 或 buttons 为 null 或 undefined，设置为空数组
    if (!(state.form as any).menus) (state.form as any).menus = [];
    if (!(state.form as any).buttons) (state.form as any).buttons = [];
  } else {
    state.form = createForm();
  }
  // 先显示对话框，确保树组件渲染
  state.isShowDialog = true;
  
  nextTick(() => {
    console.log('nextTick executed');
    // 递归获取所有菜单的 id，确保全部展开
    const getAllMenuIds = (menuList: MenuDataTree[]): (number | string)[] => {
      let ids: (number | string)[] = [];
      menuList.forEach(item => {
        if (item.id) {
          ids.push(item.id);
        }
        if (item.children && item.children.length > 0) {
          ids = [...ids, ...getAllMenuIds(item.children)];
        }
      });
      return ids;
    };
    
    // 设置默认展开的菜单（全部展开）
    state.expandedKeys = getAllMenuIds(state.menuData).filter(id => typeof id === 'number');
    // 强制同步树勾选状态
    const keys = [...state.form.menus, ...state.form.buttons];
    // 使用 setTimeout 确保树组件已经完全渲染
    setTimeout(() => {
      console.log('setTimeout executed');
      if (roleTreeRef.value) {
        roleTreeRef.value.setCheckedKeys(keys);
        console.log('setCheckedKeys called');
      }
      // 为三级项的 el-tree-node__content 添加类名
      console.log('Calling addThreeLevelClass...');
      addThreeLevelClass();
    }, 500);
  });
};
// 关闭弹窗
const closeDialog = () => {
  state.isShowDialog = false;
};
// 取消
const onCancel = () => {
  closeDialog();
};
// 更新-新增
const saveOrUpdate = () => {
  formRef.value.validate((valid: any) => {
    if (valid) {
      // 在保存前强制更新 menus 和 buttons，确保获取最新的勾选状态
      roleTreeChange();
      
      // 转换 menus 和 buttons 为字符串格式传递给后端
      const payload = {
        ...state.form,
        menus: state.form.menus.join(','),
        buttons: state.form.buttons.join(','),
      };
      useRolesApi().saveOrUpdate(payload)
          .then(() => {
            ElMessage.success('操作成功');
            Session.remove('menuData'); // 清除菜单缓存，强制下次重新获取
            Session.remove('userInfo'); // 清除用户信息缓存，强制下次重新获取
            emit('getList')
            closeDialog(); // 关闭弹窗
          })
    }
  })

}
// 获取菜单结构数据
const getMenuData = async () => {
  const res = await useMenuApi().allMenu({ t: Date.now() });
  const menuList = res.data;
  // 构建树结构
  const buildTree = (list: any[], parentId = 0): any[] => {
    return list.filter(item => item.parent_id === parentId).map(item => ({
      ...item,
      children: buildTree(list, item.id)
    }));
  };
  const nestedMenuList = buildTree(menuList);
  // 为二级菜单添加按钮权限
  const addButtonsToMenu = (menu: any) => {
    if (menu.children && menu.children.length > 0) {
      menu.children.forEach((child: any) => {
        // 检查是否已经有按钮权限（children 中的第一个元素是否有字符串类型的 id）
        const hasButtons = child.children && child.children.length > 0 && typeof child.children[0].id === 'string';
        
        if (child.title && (!child.children || child.children.length === 0) && child.title !== '个人中心') {
          // 根据菜单标题生成按钮
          const module = child.title.replace('管理', '');
          const buttons = [
            { id: `${module.toLowerCase()}:add`, title: `新增${module}` },
            { id: `${module.toLowerCase()}:edit`, title: `编辑${module}` },
            { id: `${module.toLowerCase()}:delete`, title: `删除${module}` },
            { id: `${module.toLowerCase()}:view`, title: `查看${module}` },
          ];
          child.children = buttons;
        } else if (child.title === '个人中心') {
          // 跳过个人中心
        } else if (!hasButtons) {
          // 递归处理子菜单（只有在没有按钮权限时才递归）
          addButtonsToMenu(child);
        }
      });
    }
  };
  nestedMenuList.forEach(addButtonsToMenu);
  state.menuData = nestedMenuList;
  return nestedMenuList;
}

// 为三级项的 el-tree-node__content 添加类名
const addThreeLevelClass = () => {
  // 获取所有的 el-tree-node 元素
  const treeNodes = document.querySelectorAll('.menu-data-tree .el-tree-node');
  console.log('Found tree nodes:', treeNodes.length);
  treeNodes.forEach((node) => {
    // 检查是否是三级项（按钮权限）
    const content = node.querySelector('.el-tree-node__content');
    if (content) {
      // 获取节点的 key 属性
      const nodeKey = node.getAttribute('data-key');
      console.log('Node key:', nodeKey);
      // 按钮权限的 id 是字符串类型，包含 :
      if (nodeKey && nodeKey.includes(':')) {
        content.classList.add('el-tree-node__content__three');
        console.log('Added class to:', nodeKey);
      }
    }
  });
};

// 赋值勾选的权限
const roleTreeChange = () => {
  // 获取所有选中的节点（false 表示只获取完全选中的节点，不包含半选节点）
  const checkedNodes = roleTreeRef.value.getCheckedNodes(false) as any[];
  // 获取半选中的节点（菜单）
  const halfCheckedNodes = roleTreeRef.value.getHalfCheckedNodes() as any[];
  
  // 分开菜单和按钮权限
  const menuIds = new Set<number>();
  const buttonIds: string[] = [];
  
  // 遍历完全选中的节点（包括按钮和菜单）
  checkedNodes.forEach(node => {
    if (typeof node.id === 'string') {
      // 是按钮权限
      buttonIds.push(node.id);
    } else {
      // 是菜单权限
      menuIds.add(node.id);
    }
  });
  
  // 遍历半选中的节点（只有菜单）
  halfCheckedNodes.forEach(node => {
    if (typeof node.id === 'number') {
      // 是菜单权限
      menuIds.add(node.id);
    }
  });
  
  // 转换为数组
  state.form.menus = Array.from(menuIds);
  state.form.buttons = buttonIds;
};

defineExpose({
  openDialog,

})
</script>

<style scoped lang="scss">
.system-edit-role-container {
  .menu-data-tree {
    border: var(--el-input-border, var(--el-border-base));
    border-radius: var(--el-input-border-radius, var(--el-border-radius-base));
    padding: 5px;
    width: 100%;
    overflow-x: auto;
    
    /* 一级菜单 */
    .el-tree-node > .el-tree-node__content {
      font-weight: bold;
    }
    
    /* 二级菜单 */
    .el-tree > .el-tree-node > .el-tree-node__children {
      margin-left: 20px;
    }
    
    /* 三级菜单横向排列 - 使用浮动 */
    :deep(.el-tree-node__children .el-tree-node__children) {
      overflow: hidden !important;
      margin-left: 20px !important;
      padding-bottom: 10px !important;
      width: 100% !important;
    }
    
    /* 三级菜单项样式 - 浮动布局 */
    :deep(.el-tree-node__children .el-tree-node__children .el-tree-node) {
      float: left !important;
      margin-right: 20px !important;
      white-space: nowrap !important;
      width: 120px !important;
    }
    
    /* 三级菜单项内容样式 - 使用新的类名 */
    :deep(.el-tree-node__content.el-tree-node__content__three) {
      width: 120px !important;
      display: inline-flex !important;
      justify-content: center !important;
      align-items: center !important;
      padding-left: 0 !important;
    }
    
    /* 确保三级菜单项内容区域宽度 */
    :deep(.el-tree-node__content.el-tree-node__content__three .el-tree-node__label) {
      width: auto !important;
      overflow: hidden !important;
      text-overflow: ellipsis !important;
      white-space: nowrap !important;
    }
  }
  .permission-label {
    font-weight: bold;
    margin-bottom: 10px;
    color: var(--el-text-color-primary);
  }
}
</style>
