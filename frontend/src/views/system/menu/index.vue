<template>
  <div class="system-menu-container app-container">
    <el-card>
      <div class="system-menu-search mb15">
        <el-input v-model="state.listQuery.name" placeholder="请输入菜单名称" style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="getList">查询
        </el-button>
        <el-button type="success" class="ml10" v-auth="'menu:add'" @click="onOpenSaveOrUpdate('save', null)">新增
        </el-button>
      </div>

      <z-table
          :columns="state.columns"
          :data="state.menuList"
          ref="tableRef"
          :row-key="'id'"
          :showPage="false"
          v-model:page-size="state.listQuery.pageSize"
          v-model:page="state.listQuery.page"
          :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
          @pagination-change="getList"
      />

    </el-card>
    <EditMenu :menuList="state.menuList"
              :allMenuList="state.allMenuList"
              @getList="getList"
              ref="EditRef"/>
  </div>
</template>

<script lang="ts" setup name="SystemMenu">
import {h, onMounted, reactive, ref} from 'vue';
import {useMenuApi} from '/@/api/useSystemApi/menu';
import {RouteRecordRaw} from 'vue-router';
import {ElButton, ElMessage, ElMessageBox} from 'element-plus';
import EditMenu from '/@/views/system/menu/EditMenu.vue';
import {hasPermission} from '/@/utils/auth';


const EditRef = ref();
const tableRef = ref();

// 定义菜单数据类型
interface MenuItem {
  id: number;
  parent_id: number | null;
  title: string;
  path: string;
  component: string;
  name: string;
  sort: number;
  menu_type: number;
  children?: MenuItem[];
  hasChildren?: boolean;
}

const state = reactive({
  columns: [
    {
      key: 'title', label: '菜单名称', width: '', align: 'left', show: true, render: (row: MenuItem) =>
          h(ElButton, {
            link: true,
            type: "primary",
            onClick: () => {
              onOpenSaveOrUpdate('update', row)
            }
          }, () => row.title),
    },
    {key: 'path', label: '路由路径', width: '', align: 'left', show: true},
    {key: 'component', label: '组件路径', width: '', align: 'left', show: true},
    {key: 'name', label: '路由名称', width: '', align: 'left', show: true},
    {key: 'sort', label: '排序', width: '', align: 'left', show: true},
    {key: 'menu_type', label: '类型', width: '', align: 'left', show: true, render: (row: MenuItem) => row.menu_type === 10 ? '菜单' : '按钮'}, {
      label: '操作', columnType: 'string', fixed: 'right', align: 'center', width: '140',
      render: (row: MenuItem) => {
        const buttons = [];
        if (hasPermission('menu:edit')) {
          buttons.push(h(ElButton, {
            type: "primary",
            onClick: () => {
              onOpenSaveOrUpdate('update', row)
            }
          }, () => '编辑'));
        }
        if (hasPermission('menu:delete')) {
          buttons.push(h(ElButton, {
            type: "danger",
            onClick: () => {
              deleted(row)
            }
          }, () => '删除'));
        }
        return h("div", null, buttons);
      }
    },
  ],
  // list
  menuList: [] as MenuItem[],
  allMenuList: [] as MenuItem[],
  listQuery: {
    page: 1,
    pageSize: 200,
    name: '',
  },
});

// 递归组装菜单
const menuAssembly = (parent_menu: MenuItem[], all_menu: MenuItem[]) => {
  parent_menu.forEach((parent) => {
    all_menu.forEach((menu) => {
      if (menu.parent_id == parent.id) {
        parent.children = parent.children ? parent.children : [];
        parent.children.push(menu);
      }
    })
    if (parent.children) menuAssembly(parent.children, all_menu);
  })
  state.menuList = parent_menu
};

// 获取菜单列表
const getList = async () => {
  tableRef.value.openLoading()
  let res = await useMenuApi().allMenu({ t: Date.now() })
  state.allMenuList = res.data
  let parent_menu: any = []
  res.data.forEach((menu: any) => {
    if (!menu.parent_id) {
      parent_menu.push(menu)
    }
  })
  menuAssembly(parent_menu, res.data)
  tableRef.value.closeLoading()
};
// 打开新增菜单弹窗
// const onOpenAddMenu = () => {
//   addMenuRef.value.openDialog();
// };
// 打开编辑菜单弹窗
const onOpenSaveOrUpdate = (editType: string, row: MenuItem | null) => {
  EditRef.value.openDialog(editType, row);
};
// 删除当前行
const deleted = (row: MenuItem) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '删除',
    cancelButtonText: '取消',
    type: 'warning',
  })
      .then(() => {
        ElMessage.success('删除成功');
      })
      .catch(() => {
      });
};
onMounted(() => {
  getList()
})

</script>

