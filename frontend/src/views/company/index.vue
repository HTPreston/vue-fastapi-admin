<template>
  <div class="company-container">
    <z-card shadow="hover">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>公司管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon>
              <ele-Plus/>
            </el-icon>
            新增公司
          </el-button>
        </div>
      </template>
      
      <div class="company-search">
        <el-form :inline="true" :model="searchForm" class="mb20">
          <el-form-item label="公司名称">
            <el-input v-model="searchForm.name" placeholder="请输入公司名称" clearable />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="启用" value="1" />
              <el-option label="禁用" value="0" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <div class="company-table">
        <el-table :data="tableData" style="width: 100%" v-loading="loading">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="公司名称" />
          <el-table-column prop="short_name" label="公司简称" />
          <el-table-column prop="contact_phone" label="联系电话" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === 1 ? 'success' : 'info'">
                {{ scope.row.status === 1 ? '启用' : '禁用' }}
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
      :title="dialogType === 'add' ? '新增公司' : '编辑公司'"
      width="600px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="公司名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入公司名称" />
        </el-form-item>
        <el-form-item label="公司简称" prop="short_name">
          <el-input v-model="form.short_name" placeholder="请输入公司简称" />
        </el-form-item>
        <el-form-item label="统一社会信用代码" prop="credit_code">
          <el-input v-model="form.credit_code" placeholder="请输入统一社会信用代码" />
        </el-form-item>
        <el-form-item label="法人代表" prop="legal_representative">
          <el-input v-model="form.legal_representative" placeholder="请输入法人代表" />
        </el-form-item>
        <el-form-item label="联系电话" prop="contact_phone">
          <el-input v-model="form.contact_phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="注册地址" prop="registered_address">
          <el-input v-model="form.registered_address" placeholder="请输入注册地址" />
        </el-form-item>
        <el-form-item label="办公地址" prop="office_address">
          <el-input v-model="form.office_address" placeholder="请输入办公地址" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态">
            <el-option label="启用" value="1" />
            <el-option label="禁用" value="0" />
          </el-select>
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

<script setup lang="ts" name="companyIndex">
import {ref, reactive, onMounted} from 'vue';
import {ElMessage, ElMessageBox} from 'element-plus';
import {useCompanyApi} from '../../api/company/company';

// 定义变量
const loading = ref(false);
const dialogVisible = ref(false);
const dialogType = ref('add');
const formRef = ref();
const companyApi = useCompanyApi();

// 搜索表单
const searchForm = reactive({
  name: '',
  status: ''
});

// 表单数据
const form = reactive({
  id: '',
  name: '',
  short_name: '',
  credit_code: '',
  legal_representative: '',
  contact_phone: '',
  registered_address: '',
  office_address: '',
  status: 1
});

// 表单验证规则
const rules = reactive({
  name: [
    {required: true, message: '请输入公司名称', trigger: 'blur'}
  ],
  short_name: [
    {required: true, message: '请输入公司简称', trigger: 'blur'}
  ],
  contact_phone: [
    {required: true, message: '请输入联系电话', trigger: 'blur'}
  ],
  status: [
    {required: true, message: '请选择状态', trigger: 'change'}
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

// 获取公司列表
const getCompanyList = async () => {
  loading.value = true;
  try {
    const params = {
      name: searchForm.name,
      status: searchForm.status,
      page: pagination.page,
      page_size: pagination.pageSize
    };
    const res = await companyApi.getList(params);
    tableData.value = res.data.list;
    pagination.total = res.data.total;
  } catch (error) {
    ElMessage.error('获取公司列表失败');
    console.error('获取公司列表失败:', error);
  } finally {
    loading.value = false;
  }
};

// 搜索
const handleSearch = () => {
  pagination.page = 1;
  getCompanyList();
};

// 重置
const resetForm = () => {
  searchForm.name = '';
  searchForm.status = '';
  pagination.page = 1;
  getCompanyList();
};

// 新增
const handleAdd = () => {
  dialogType.value = 'add';
  // 重置表单
  form.id = '';
  form.name = '';
  form.short_name = '';
  form.credit_code = '';
  form.legal_representative = '';
  form.contact_phone = '';
  form.registered_address = '';
  form.office_address = '';
  form.status = 1;
  dialogVisible.value = true;
};

// 编辑
const handleEdit = async (row: any) => {
  dialogType.value = 'edit';
  try {
    const res = await companyApi.getById(row.id);
    const data = res.data;
    // 填充表单数据
    form.id = data.id;
    form.name = data.name;
    form.short_name = data.short_name || '';
    form.credit_code = data.credit_code || '';
    form.legal_representative = data.legal_representative || '';
    form.contact_phone = data.contact_phone || '';
    form.registered_address = data.registered_address || '';
    form.office_address = data.office_address || '';
    form.status = data.status;
    dialogVisible.value = true;
  } catch (error) {
    ElMessage.error('获取公司详情失败');
    console.error('获取公司详情失败:', error);
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
      await companyApi.delete(id);
      ElMessage.success('删除成功');
      getCompanyList();
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
          await companyApi.create(form);
          ElMessage.success('新增成功');
        } else {
          await companyApi.update(form);
          ElMessage.success('编辑成功');
        }
        dialogVisible.value = false;
        getCompanyList();
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
  getCompanyList();
};

const handleCurrentChange = (current: number) => {
  pagination.page = current;
  getCompanyList();
};

// 页面挂载时获取数据
onMounted(() => {
  getCompanyList();
});
</script>

<style scoped lang="scss">
.company-container {
  padding: 20px;
  
  .company-search {
    margin-bottom: 20px;
  }
  
  .company-table {
    width: 100%;
  }
  
  .mb20 {
    margin-bottom: 20px;
  }
}
</style>