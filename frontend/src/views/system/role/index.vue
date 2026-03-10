<template>
  <div class="system-role-container app-container">
    <el-card>
      <div class="system-user-search mb15">
        <el-input v-model="state.listQuery.name" placeholder="请输入角色名称" style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="search">查询
        </el-button>
        <el-button type="success" class="ml10" v-auth="'role:add'" @click="onOpenSaveOrUpdate('save', null)">新增
        </el-button>
      </div>
      <z-table
          :columns="state.columns"
          :data="state.listData"
          ref="tableRef"
          v-model:page-size="state.listQuery.pageSize"
          v-model:page="state.listQuery.page"
          :total="state.total"
          @pagination-change="getList"
      />
    </el-card>
    <SaveOrUpdateRole ref="SaveOrUpdateRoleRef" @getList="getList"/>
  </div>
</template>

<script lang="ts" setup name="SystemRole">
import {h, onMounted, reactive, ref} from 'vue';
import {ElButton, ElMessage, ElMessageBox, ElTag} from 'element-plus';
import SaveOrUpdateRole from '/@/views/system/role/EditRole.vue';
import {useRolesApi} from "/@/api/useSystemApi/roles";
import {useUserStore} from '/@/stores/user';
import {hasPermission} from '/@/utils/auth';

const userStore = useUserStore();


const SaveOrUpdateRoleRef = ref();
const tableRef = ref();
const state = reactive({
  columns: [
    {
      label: '操作', fixed: 'left', width: '', align: 'center',
      render: (row: any) => {
        const buttons = [];
        // 权限检查：只有拥有对应权限的用户才能操作
        if (hasPermission('role:edit')) {
          if (row.role_type === 10) {
            // 只有role_type为10的超级管理员才能编辑超级管理员角色
            if (userStore.userInfos.role_type === 10) {
              buttons.push(h(ElButton, {
                type: "primary",
                size: "small",
                onClick: () => {
                  onOpenSaveOrUpdate("update", row)
                }
              }, () => '编辑'));
            }
          } else {
            // 其他角色都可以编辑
            buttons.push(h(ElButton, {
              type: "primary",
              size: "small",
              onClick: () => {
                onOpenSaveOrUpdate("update", row)
              }
            }, () => '编辑'));
          }
        }
        // 只有非超级管理员角色才能被删除
        if (hasPermission('role:delete') && row.role_type !== 10) {
          buttons.push(h(ElButton, {
            type: "danger",
            size: "small",
            onClick: () => {
              deleted(row)
            }
          }, () => '删除'));
        }
        return h("div", { style: { display: 'flex', gap: '8px', justifyContent: 'center' } }, buttons);
      }
    },
    {
      key: 'name', label: '角色名称', width: '', align: 'center', show: true,
      render: (row: any) => h(ElTag, {
        type: row.role_type == 10 ? "danger" : row.role_type == 20 ? "warning" : "primary",
        effect: "light"
      }, () => row.name)
    },
    {key: 'role_type', label: '权限类型', width: '', align: 'center', show: true},
    {
      key: 'status', label: '角色状态', width: '', align: 'center', show: true,
      render: (row: any) => h(ElTag, {
        type: row.status == 1 ? "success" : "info",
      }, () => row.status == 1 ? "启用" : "禁用",)
    },
    {key: 'description', label: '备注', width: '', align: 'center', show: true},
    {key: 'updation_date', label: '更新时间', width: '', align: 'center', show: true},
    {key: 'creation_date', label: '创建时间', width: '', align: 'center', show: true},
  ],
  // list
  listData: [],
  tableLoading: false,
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    name: '',
  },
});
// 初始化表格数据
const getList = () => {
  tableRef.value.openLoading()
  useRolesApi().getList(state.listQuery)
      .then(res => {
        state.listData = res.data.rows
        state.total = res.data.rowTotal
      })
      .finally(() => {
        tableRef.value.closeLoading()
      })
};

// 查询
const search = () => {
  state.listQuery.page = 1
  getList()
}

// 新增或修改角色
const onOpenSaveOrUpdate = (editType: string, row: any) => {
  SaveOrUpdateRoleRef.value.openDialog(editType, row);
};

// 删除角色
const deleted = (row: any) => {
  if (!row || !row.id) {
    ElMessage.error('无效的角色数据');
    return;
  }
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
      .then(() => {
        useRolesApi().deleted({id: row.id})
            .then(() => {
              ElMessage.success('删除成功');
              getList()
            })
            .catch((error) => {
              ElMessage.error(error.response?.data?.message || '删除失败');
            })
      })
      .catch(() => {
      });
};

// 页面加载时
onMounted(() => {
  getList();
});

</script>
