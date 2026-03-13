<template>
  <div class="project-container">
    <z-card shadow="hover">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>项目管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon>
              <ele-Plus/>
            </el-icon>
            新增项目
          </el-button>
        </div>
      </template>
      
      <div class="project-search">
        <el-form :inline="true" :model="searchForm" class="mb20">
          <el-form-item label="项目名称">
            <el-input v-model="searchForm.name" placeholder="请输入项目名称" clearable />
          </el-form-item>
          <el-form-item label="项目状态">
            <el-select v-model="searchForm.project_status" placeholder="请选择状态" clearable>
              <el-option label="投标中" value="投标中" />
              <el-option label="已中标" value="已中标" />
              <el-option label="未中标" value="未中标" />
              <el-option label="已放弃" value="已放弃" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <div class="project-table">
        <el-table :data="tableData" style="width: 100%" v-loading="loading">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="项目名称" />
          <el-table-column prop="project_code" label="项目编号" />
          <el-table-column prop="project_type" label="项目类型" />
          <el-table-column prop="project_location" label="项目地点" />
          <el-table-column prop="tender_organization" label="招标单位" />
          <el-table-column prop="project_status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.project_status)">
                {{ scope.row.project_status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleEdit(scope.row)">
                编辑
              </el-button>
              <el-button type="danger" size="small" @click="handleDelete(scope.row.id)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <div class="pagination-container" style="margin-top: 20px;">
          <el-pagination
            v-model:current-page="pagination.page"
            v-model:page-size="pagination.pageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="pagination.total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </z-card>
    
    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增项目' : '编辑项目'"
      width="600px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="项目编号" prop="project_code">
          <el-input v-model="form.project_code" placeholder="请输入项目编号" />
        </el-form-item>
        <el-form-item label="项目类型" prop="project_type">
          <el-input v-model="form.project_type" placeholder="请输入项目类型" />
        </el-form-item>
        <el-form-item label="项目地点" prop="project_location">
          <el-input v-model="form.project_location" placeholder="请输入项目地点" />
        </el-form-item>
        <el-form-item label="招标单位" prop="tender_organization">
          <el-input v-model="form.tender_organization" placeholder="请输入招标单位" />
        </el-form-item>
        <el-form-item label="招标代理机构" prop="tender_agent">
          <el-input v-model="form.tender_agent" placeholder="请输入招标代理机构" />
        </el-form-item>
        <el-form-item label="招标编号" prop="tender_number">
          <el-input v-model="form.tender_number" placeholder="请输入招标编号" />
        </el-form-item>
        <el-form-item label="招标日期" prop="tender_date">
          <el-date-picker v-model="form.tender_date" type="date" placeholder="请选择招标日期" style="width: 100%" />
        </el-form-item>
        <el-form-item label="开标日期" prop="bid_open_date">
          <el-date-picker v-model="form.bid_open_date" type="date" placeholder="请选择开标日期" style="width: 100%" />
        </el-form-item>
        <el-form-item label="项目状态" prop="project_status">
          <el-select v-model="form.project_status" placeholder="请选择项目状态">
            <el-option label="投标中" value="投标中" />
            <el-option label="已中标" value="已中标" />
            <el-option label="未中标" value="未中标" />
            <el-option label="已放弃" value="已放弃" />
          </el-select>
        </el-form-item>
        <el-form-item label="项目预计费用" prop="project_cost">
          <el-input v-model="form.project_cost" type="number" placeholder="请输入项目预计费用" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="projectIndex">
import {ref, reactive, onMounted} from 'vue';
import {ElMessage, ElMessageBox} from 'element-plus';
import {useProjectApi} from '../../api/project/project';

// 定义变量
const loading = ref(false);
const dialogVisible = ref(false);
const dialogType = ref('add');
const formRef = ref();
const projectApi = useProjectApi();

// 搜索表单
const searchForm = reactive({
  name: '',
  project_status: ''
});

// 表单数据
const form = reactive({
  id: '',
  name: '',
  project_code: '',
  project_type: '',
  project_location: '',
  tender_organization: '',
  tender_agent: '',
  tender_number: '',
  tender_date: '',
  bid_open_date: '',
  project_status: '投标中',
  project_cost: ''
});

// 表单验证规则
const rules = reactive({
  name: [
    {required: true, message: '请输入项目名称', trigger: 'blur'}
  ],
  project_code: [
    {required: true, message: '请输入项目编号', trigger: 'blur'}
  ],
  project_status: [
    {required: true, message: '请选择项目状态', trigger: 'change'}
  ]
});

// 表格数据
const tableData = ref([]);

// 分页数据
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
});

// 获取项目列表
const getProjectList = async () => {
  loading.value = true;
  try {
    const params = {
      name: searchForm.name,
      project_status: searchForm.project_status,
      page: pagination.page,
      page_size: pagination.pageSize
    };
    const res = await projectApi.getList(params);
    tableData.value = res.data.list;
    pagination.total = res.data.total;
  } catch (error) {
    ElMessage.error('获取项目列表失败');
    console.error('获取项目列表失败:', error);
  } finally {
    loading.value = false;
  }
};

// 获取状态类型
const getStatusType = (status: string) => {
  switch (status) {
    case '投标中': return 'warning';
    case '已中标': return 'success';
    case '未中标': return 'info';
    case '已放弃': return 'danger';
    default: return 'default';
  }
};

// 搜索
const handleSearch = () => {
  pagination.page = 1;
  getProjectList();
};

// 重置
const resetForm = () => {
  searchForm.name = '';
  searchForm.project_status = '';
  pagination.page = 1;
  getProjectList();
};

// 新增
const handleAdd = () => {
  dialogType.value = 'add';
  // 重置表单
  form.id = '';
  form.name = '';
  form.project_code = '';
  form.project_type = '';
  form.project_location = '';
  form.tender_organization = '';
  form.tender_agent = '';
  form.tender_number = '';
  form.tender_date = '';
  form.bid_open_date = '';
  form.project_status = '投标中';
  form.project_cost = '';
  dialogVisible.value = true;
};

// 编辑
const handleEdit = async (row: any) => {
  dialogType.value = 'edit';
  try {
    const res = await projectApi.getById(row.id);
    const data = res.data;
    // 填充表单数据
    form.id = data.id;
    form.name = data.name;
    form.project_code = data.project_code || '';
    form.project_type = data.project_type || '';
    form.project_location = data.project_location || '';
    form.tender_organization = data.tender_organization || '';
    form.tender_agent = data.tender_agent || '';
    form.tender_number = data.tender_number || '';
    form.tender_date = data.tender_date;
    form.bid_open_date = data.bid_open_date;
    form.project_status = data.project_status;
    form.project_cost = data.project_cost;
    dialogVisible.value = true;
  } catch (error) {
    ElMessage.error('获取项目详情失败');
    console.error('获取项目详情失败:', error);
  }
};

// 删除
const handleDelete = (id: number) => {
  ElMessageBox.confirm('确定要删除这条记录吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await projectApi.delete(id);
      ElMessage.success('删除成功');
      getProjectList();
    } catch (error) {
      ElMessage.error('删除失败');
      console.error('删除失败:', error);
    }
  }).catch(() => {
    // 取消删除
  });
};

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        if (dialogType.value === 'add') {
          await projectApi.create(form);
          ElMessage.success('新增成功');
        } else {
          await projectApi.update(form);
          ElMessage.success('编辑成功');
        }
        dialogVisible.value = false;
        getProjectList();
      } catch (error) {
        ElMessage.error(dialogType.value === 'add' ? '新增失败' : '编辑失败');
        console.error('提交失败:', error);
      }
    }
  });
};

// 分页处理
const handleSizeChange = (size: number) => {
  pagination.pageSize = size;
  getProjectList();
};

const handleCurrentChange = (current: number) => {
  pagination.page = current;
  getProjectList();
};

// 页面挂载时获取数据
onMounted(() => {
  getProjectList();
});
</script>

<style scoped lang="scss">
.project-container {
  padding: 20px;
  
  .project-search {
    margin-bottom: 20px;
  }
  
  .project-table {
    width: 100%;
  }
  
  .mb20 {
    margin-bottom: 20px;
  }
}
</style>