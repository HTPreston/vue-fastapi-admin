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
          <el-table-column prop="name" label="公司全称" />
          <el-table-column prop="short_name" label="公司简称" />
          <el-table-column prop="english_name" label="英文名称" />
          <el-table-column prop="credit_code" label="统一社会信用代码" />
          <el-table-column prop="legal_representative" label="法定代表人" />
          <el-table-column prop="registered_capital" label="注册资本(万元)" width="120" />
          <el-table-column prop="establishment_date" label="成立日期" width="120" />
          <el-table-column prop="business_term" label="经营期限" />
          <el-table-column prop="company_type" label="企业类型" />
          <el-table-column prop="business_scope" label="经营范围" show-overflow-tooltip />
          <el-table-column prop="registered_address" label="注册地址" />
          <el-table-column prop="office_address" label="办公地址" />
          <el-table-column prop="postal_code" label="邮政编码" width="100" />
          <el-table-column prop="contact_phone" label="联系电话" />
          <el-table-column prop="fax" label="传真号码" />
          <el-table-column prop="website" label="公司网址" />
          <el-table-column prop="email" label="电子邮箱" />
          <el-table-column prop="personnel_reserve" label="人员储备" width="100">
            <template #default="scope">
              <el-button type="text" @click="handleViewPersonnelReserve(scope.row.personnel_reserve)">
                查看
              </el-button>
            </template>
          </el-table-column>
          <el-table-column prop="bank_name" label="开户银行" />
          <el-table-column prop="bank_account" label="银行账号" />
          <el-table-column prop="business_license_path" label="营业执照" width="120">
            <template #default="scope">
              <el-button type="text" @click="handleViewImage(scope.row.business_license_path)">
                查看
              </el-button>
            </template>
          </el-table-column>
          <el-table-column prop="deposit_account_path" label="存款账户" width="120">
            <template #default="scope">
              <el-button type="text" @click="handleViewImage(scope.row.deposit_account_path)">
                查看
              </el-button>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === 1 ? 'success' : 'info'">
                {{ scope.row.status === 1 ? '启用' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column prop="updated_at" label="更新时间" width="180" />
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleEdit(scope.row)" style="margin-right: 8px">
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
        <el-form-item label="公司全称" prop="name">
          <el-input v-model="form.name" placeholder="请输入公司全称" />
        </el-form-item>
        <el-form-item label="公司简称" prop="short_name">
          <el-input v-model="form.short_name" placeholder="请输入公司简称" />
        </el-form-item>
        <el-form-item label="英文名称" prop="english_name">
          <el-input v-model="form.english_name" placeholder="请输入英文名称" />
        </el-form-item>
        <el-form-item label="统一社会信用代码" prop="credit_code">
          <el-input v-model="form.credit_code" placeholder="请输入统一社会信用代码" />
        </el-form-item>
        <el-form-item label="法定代表人" prop="legal_representative">
          <el-input v-model="form.legal_representative" placeholder="请输入法定代表人" />
        </el-form-item>
        <el-form-item label="注册资本(万元)" prop="registered_capital">
          <el-input-number v-model="form.registered_capital" :min="0" placeholder="请输入注册资本" />
        </el-form-item>
        <el-form-item label="成立日期" prop="establishment_date">
          <el-date-picker v-model="form.establishment_date" type="date" placeholder="请选择成立日期" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="经营期限" prop="business_term">
          <el-input v-model="form.business_term" placeholder="请输入经营期限" />
        </el-form-item>
        <el-form-item label="企业类型" prop="company_type">
          <el-input v-model="form.company_type" placeholder="请输入企业类型" />
        </el-form-item>
        <el-form-item label="经营范围" prop="business_scope">
          <el-input v-model="form.business_scope" type="textarea" :rows="3" placeholder="请输入经营范围" />
        </el-form-item>
        <el-form-item label="注册地址" prop="registered_address">
          <el-input v-model="form.registered_address" placeholder="请输入注册地址" />
        </el-form-item>
        <el-form-item label="办公地址" prop="office_address">
          <el-input v-model="form.office_address" placeholder="请输入办公地址" />
        </el-form-item>
        <el-form-item label="邮政编码" prop="postal_code">
          <el-input v-model="form.postal_code" placeholder="请输入邮政编码" />
        </el-form-item>
        <el-form-item label="联系电话" prop="contact_phone">
          <el-input v-model="form.contact_phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="传真号码" prop="fax">
          <el-input v-model="form.fax" placeholder="请输入传真号码" />
        </el-form-item>
        <el-form-item label="公司网址" prop="website">
          <el-input v-model="form.website" placeholder="请输入公司网址" />
        </el-form-item>
        <el-form-item label="电子邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入电子邮箱" />
        </el-form-item>
        <el-form-item label="开户银行" prop="bank_name">
          <el-input v-model="form.bank_name" placeholder="请输入开户银行" />
        </el-form-item>
        <el-form-item label="银行账号" prop="bank_account">
          <el-input v-model="form.bank_account" placeholder="请输入银行账号" />
        </el-form-item>
        <el-form-item label="营业执照图片路径" prop="business_license_path">
          <el-input v-model="form.business_license_path" placeholder="请输入营业执照图片路径" />
        </el-form-item>
        <el-form-item label="存款账户图片路径" prop="deposit_account_path">
          <el-input v-model="form.deposit_account_path" placeholder="请输入存款账户图片路径" />
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
    
    <!-- 图片查看对话框 -->
    <el-dialog
      v-model="imageDialogVisible"
      title="图片查看"
      width="800px"
    >
      <el-image
        v-if="currentImagePath"
        :src="currentImagePath"
        fit="contain"
        style="width: 100%; height: 600px"
      />
      <div v-else class="no-image">暂无图片</div>
    </el-dialog>
    
    <!-- 人员储备查看对话框 -->
    <el-dialog
      v-model="personnelDialogVisible"
      title="人员储备"
      width="600px"
    >
      <el-descriptions :column="1" border>
        <el-descriptions-item label="人员储备">
          <div v-if="currentPersonnelReserve" class="personnel-reserve">
            {{ JSON.stringify(currentPersonnelReserve, null, 2) }}
          </div>
          <div v-else>暂无人员储备数据</div>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="companyIndex">
import {ref, reactive, onMounted} from 'vue';
import {ElMessage, ElMessageBox, ElDialog, ElImage, ElDescriptions, ElDescriptionsItem} from 'element-plus';
import {useCompanyApi} from '../../api/company/company';

// 定义变量
const loading = ref(false);
const dialogVisible = ref(false);
const imageDialogVisible = ref(false);
const personnelDialogVisible = ref(false);
const currentImagePath = ref('');
const currentPersonnelReserve = ref(null);
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
  english_name: '',
  credit_code: '',
  legal_representative: '',
  registered_capital: null,
  establishment_date: '',
  business_term: '',
  company_type: '',
  business_scope: '',
  registered_address: '',
  office_address: '',
  postal_code: '',
  contact_phone: '',
  fax: '',
  website: '',
  email: '',
  personnel_reserve: null,
  bank_name: '',
  bank_account: '',
  business_license_path: '',
  deposit_account_path: '',
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
    const params: any = {
      name: searchForm.name,
      page: pagination.page,
      page_size: pagination.pageSize
    };
    // 只有当 status 有值时才传递
    if (searchForm.status !== '') {
      params.status = parseInt(searchForm.status);
    }
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
  form.english_name = '';
  form.credit_code = '';
  form.legal_representative = '';
  form.registered_capital = null;
  form.establishment_date = '';
  form.business_term = '';
  form.company_type = '';
  form.business_scope = '';
  form.registered_address = '';
  form.office_address = '';
  form.postal_code = '';
  form.contact_phone = '';
  form.fax = '';
  form.website = '';
  form.email = '';
  form.personnel_reserve = null;
  form.bank_name = '';
  form.bank_account = '';
  form.business_license_path = '';
  form.deposit_account_path = '';
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
    form.english_name = data.english_name || '';
    form.credit_code = data.credit_code || '';
    form.legal_representative = data.legal_representative || '';
    form.registered_capital = data.registered_capital || null;
    form.establishment_date = data.establishment_date || '';
    form.business_term = data.business_term || '';
    form.company_type = data.company_type || '';
    form.business_scope = data.business_scope || '';
    form.registered_address = data.registered_address || '';
    form.office_address = data.office_address || '';
    form.postal_code = data.postal_code || '';
    form.contact_phone = data.contact_phone || '';
    form.fax = data.fax || '';
    form.website = data.website || '';
    form.email = data.email || '';
    form.personnel_reserve = data.personnel_reserve || null;
    form.bank_name = data.bank_name || '';
    form.bank_account = data.bank_account || '';
    form.business_license_path = data.business_license_path || '';
    form.deposit_account_path = data.deposit_account_path || '';
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

// 查看图片
const handleViewImage = (imagePath: string) => {
  if (imagePath) {
    currentImagePath.value = imagePath;
    imageDialogVisible.value = true;
  } else {
    ElMessage.warning('暂无图片');
  }
};

// 查看人员储备
const handleViewPersonnelReserve = (personnelReserve: any) => {
  currentPersonnelReserve.value = personnelReserve;
  personnelDialogVisible.value = true;
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
  
  .no-image {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 600px;
    background-color: #f5f7fa;
    color: #909399;
    font-size: 16px;
  }
  
  .personnel-reserve {
    white-space: pre-wrap;
    font-family: 'Courier New', Courier, monospace;
    font-size: 14px;
    line-height: 1.5;
    color: #303133;
  }
}
</style>