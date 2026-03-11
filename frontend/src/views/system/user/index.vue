<template>
  <div class="system-user-container app-container">
    <el-card>
      <div class="system-user-search mb15">
        <el-input v-model="state.listQuery.username" placeholder="请输入用户名称" style="max-width: 180px"></el-input>
        <el-button type="primary" class="ml10" @click="search">查询
        </el-button>
        <el-button v-auth="'user:add'" type="success" class="ml10" @click="onOpenSaveOrUpdate('save', null)">
          新增
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
    <SaveOrUpdateUser @getList="getList" ref="SaveOrUpdateUserRef"/>
  </div>
</template>

<script lang="ts" setup name="SystemUser">
import {h, onMounted, reactive, ref, computed} from 'vue';
import {ElButton, ElMessage, ElMessageBox, ElTag} from 'element-plus';
import SaveOrUpdateUser from '/@/views/system/user/EditUser.vue';
import {useUserApi} from '/@/api/useSystemApi/user';
import {hasPermission} from '/@/utils/auth';

// 定义接口来定义对象的类型
interface TableDataRow {
  id: number;
  username: string;
  email: string;
  status: boolean;
  role_type: number;
  created_by: number;
  updated_by: number;
  creation_date: string;
  updation_date: string;
}

interface listQueryRow {
  page: number;
  pageSize: number;
  username: string;

}

interface StateRow {
  columns: Array<any>;
  fieldData: Array<any>;
  listData: Array<TableDataRow>;
  total: number;
  listQuery: listQueryRow;
}


const SaveOrUpdateUserRef = ref()
const tableRef = ref()

const state = reactive<StateRow>({
  fieldData: [],
  columns: [
    {
      key: 'username', label: '账户名称', width: '140px', align: 'center', show: true,
      render: (row: any) => h(ElTag, {
        type: row.role_type == 10 ? "danger" : row.role_type == 20 ? "warning" : "primary",
        effect: "light"
      }, () => row.username)
    },
    {key: 'phone', label: '手机号', width: '', align: 'center', show: true},


    {key: 'email', label: '邮箱', width: '', align: 'center', show: true},
    {
      key: 'status', label: '用户状态', width: '', align: 'center', show: true,
      render: (row: any) => h(ElTag, {
        type: row.status ? "success" : "info",
      }, () => row.status ? "启用" : "禁用",)
    },
    {key: 'remarks', label: '备注', width: '', align: 'center', show: true},
    {key: 'creation_date', label: '创建时间', width: '', align: 'center', show: true},
    {
      label: '操作', width: '150px', align: 'center',
      render: (row: any) => {
        const buttons = [];
        if (hasPermission('user:edit')) {
          buttons.push(h(ElButton, {
            type: "primary",
            size: "small",
            onClick: () => {
              onOpenSaveOrUpdate('update', row)
            }
          }, () => '编辑'));
        }
        if (hasPermission('user:delete')) {
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
  ],
  // list
  listData: [],
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    username: '',
  },
  //rule

});
// 获取用户数据
const getList = () => {
  tableRef.value.openLoading()
  useUserApi().getList(state.listQuery)
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

// 新增或修改用户
const onOpenSaveOrUpdate = (editType: string, row: TableDataRow | null = null) => {
  SaveOrUpdateUserRef.value.openDialog(editType, row);
};

// 删除用户
const deleted = (row: TableDataRow) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(() => {
      useUserApi().deleted({id: row.id})
        .then(() => {
          ElMessage.success('删除成功');
          getList()
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
