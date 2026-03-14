<template>
  <div class="personnel-container">
    <z-card shadow="hover">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>人员管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon>
              <ele-Plus/>
            </el-icon>
            新增人员
          </el-button>
        </div>
      </template>
      
      <div class="personnel-search">
        <el-form :inline="true" :model="searchForm" class="mb20">
          <el-form-item label="姓名">
            <el-input v-model="searchForm.name" placeholder="请输入姓名" clearable />
          </el-form-item>
          <el-form-item label="性别">
            <el-select v-model="searchForm.gender" placeholder="请选择性别" clearable>
              <el-option label="男" value="男" />
              <el-option label="女" value="女" />
            </el-select>
          </el-form-item>
          <el-form-item label="人员状态">
            <el-select v-model="searchForm.personnel_status" placeholder="请选择状态" clearable>
              <el-option label="在职" :value="1" />
              <el-option label="离职" :value="0" />
              <el-option label="休假" :value="2" />
            </el-select>
          </el-form-item>
          <el-form-item label="是否专职">
            <el-select v-model="searchForm.is_full_time" placeholder="请选择" clearable>
              <el-option label="是" :value="1" />
              <el-option label="否" :value="0" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <div class="personnel-table">
        <el-table :data="tableData" style="width: 100%" v-loading="loading">
          <el-table-column prop="id" label="ID" />
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="gender" label="性别" />
          <el-table-column prop="phone" label="手机号码" />
          <el-table-column prop="email" label="电子邮箱" />
          <el-table-column prop="education" label="学历" />
          <el-table-column prop="title" label="职称" />
          <el-table-column prop="work_years" label="工作年限" />
          <el-table-column prop="is_full_time" label="是否专职">
            <template #default="scope">
              <el-tag :type="scope.row.is_full_time === 1 ? 'success' : 'info'">
                {{ scope.row.is_full_time === 1 ? '是' : '否' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="personnel_status" label="人员状态">
            <template #default="scope">
              <el-tag 
                :type="scope.row.personnel_status === 1 ? 'success' : scope.row.personnel_status === 0 ? 'danger' : 'warning'"
              >
                {{ scope.row.personnel_status === 1 ? '在职' : scope.row.personnel_status === 0 ? '离职' : '休假' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="employment_date" label="入职日期" />
          <el-table-column label="操作" fixed="right" width="240">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleEdit(scope.row)" style="margin-right: 8px">
                编辑
              </el-button>
              <el-button type="success" size="small" @click="handleQualification(scope.row)" style="margin-right: 8px">
                资质证书
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
      :title="dialogType === 'add' ? '新增人员' : '编辑人员'"
      width="80%"
    >
      <el-form :model="form" :rules="rules" ref="formRef" size="default" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="form.name" placeholder="请输入姓名" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="form.gender" placeholder="请选择性别" clearable style="width: 100%">
                <el-option label="男" value="男" />
                <el-option label="女" value="女" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="出生日期" prop="birth_date">
              <el-date-picker
                v-model="form.birth_date"
                type="date"
                placeholder="请选择出生日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="身份证号码" prop="id_card_no">
              <el-input v-model="form.id_card_no" placeholder="请输入身份证号码" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入手机号码" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="电子邮箱" prop="email">
              <el-input v-model="form.email" placeholder="请输入电子邮箱" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="学历" prop="education">
              <el-input v-model="form.education" placeholder="请输入学历" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="毕业院校" prop="graduate_school">
              <el-input v-model="form.graduate_school" placeholder="请输入毕业院校" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="专业" prop="major">
              <el-input v-model="form.major" placeholder="请输入专业" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="职称" prop="title">
              <el-input v-model="form.title" placeholder="请输入职称" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="工作年限" prop="work_years">
              <el-input-number v-model="form.work_years" :min="0" placeholder="请输入工作年限" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="参加工作时间" prop="work_start_date">
              <el-date-picker
                v-model="form.work_start_date"
                type="date"
                placeholder="请选择参加工作时间"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="入职日期" prop="employment_date">
              <el-date-picker
                v-model="form.employment_date"
                type="date"
                placeholder="请选择入职日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="人员状态" prop="personnel_status">
              <el-select v-model="form.personnel_status" placeholder="请选择人员状态" clearable style="width: 100%">
                <el-option label="在职" :value="1" />
                <el-option label="离职" :value="0" />
                <el-option label="休假" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="是否专职" prop="is_full_time">
              <el-select v-model="form.is_full_time" placeholder="请选择" clearable style="width: 100%">
                <el-option label="是" :value="1" />
                <el-option label="否" :value="0" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="是否公司负责人" prop="is_principal">
              <el-select v-model="form.is_principal" placeholder="请选择" clearable style="width: 100%">
                <el-option label="是" :value="1" />
                <el-option label="否" :value="0" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="工作经历" prop="work_experience">
          <el-input
            v-model="form.work_experience"
            type="textarea"
            :rows="3"
            placeholder="请输入工作经历"
          />
        </el-form-item>
        
        <el-form-item label="项目经验" prop="project_experience">
          <el-input
            v-model="form.project_experience"
            type="textarea"
            :rows="3"
            placeholder="请输入项目经验"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 资质证书对话框 -->
    <QualificationDialog ref="qualificationDialogRef" />
  </div>
</template>

<script setup lang="ts" name="personnelIndex">
import {ref, reactive, onMounted} from 'vue';
import {ElMessage, ElMessageBox} from 'element-plus';
import {usePersonnelApi} from '../../api/useSystemApi/personnel';
import QualificationDialog from './QualificationDialog.vue';

// 定义变量
const loading = ref(false);
const dialogVisible = ref(false);
const dialogType = ref('add');
const formRef = ref();
const qualificationDialogRef = ref();
const personnelApi = usePersonnelApi();

// 搜索表单
const searchForm = reactive({
  name: '',
  gender: '',
  personnel_status: null as number | null,
  is_full_time: null as number | null
});

// 表单数据
const form = reactive({
  id: null as number | null,
  name: '',
  gender: '',
  birth_date: '',
  id_card_no: '',
  phone: '',
  email: '',
  education: '',
  graduate_school: '',
  major: '',
  title: '',
  work_years: 0,
  work_start_date: '',
  employment_date: '',
  personnel_status: 1,
  is_full_time: 1,
  is_principal: 0,
  work_experience: '',
  project_experience: ''
});

// 表单验证规则
const rules = reactive({
  name: [{required: true, message: '请输入姓名', trigger: 'blur'}],
  phone: [{required: true, message: '请输入手机号码', trigger: 'blur'}]
});

// 表格数据
const tableData = ref([]);

// 分页数据
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
});

// 获取人员列表
const getPersonnelList = async () => {
  loading.value = true;
  try {
    const params = {
      name: searchForm.name,
      gender: searchForm.gender,
      personnel_status: searchForm.personnel_status,
      is_full_time: searchForm.is_full_time,
      page: pagination.page,
      page_size: pagination.pageSize
    };
    const res = await personnelApi.getList(params);
    tableData.value = res.data.list;
    pagination.total = res.data.total;
  } catch (error) {
    ElMessage.error('获取人员列表失败');
    console.error('获取人员列表失败:', error);
  } finally {
    loading.value = false;
  }
};

// 搜索
const handleSearch = () => {
  pagination.page = 1;
  getPersonnelList();
};

// 重置
const resetForm = () => {
  searchForm.name = '';
  searchForm.gender = '';
  searchForm.personnel_status = null;
  searchForm.is_full_time = null;
  pagination.page = 1;
  getPersonnelList();
};

// 新增
const handleAdd = () => {
  dialogType.value = 'add';
  // 重置表单
  form.id = null;
  form.name = '';
  form.gender = '';
  form.birth_date = '';
  form.id_card_no = '';
  form.phone = '';
  form.email = '';
  form.education = '';
  form.graduate_school = '';
  form.major = '';
  form.title = '';
  form.work_years = 0;
  form.work_start_date = '';
  form.employment_date = '';
  form.personnel_status = 1;
  form.is_full_time = 1;
  form.is_principal = 0;
  form.work_experience = '';
  form.project_experience = '';
  dialogVisible.value = true;
};

// 编辑
const handleEdit = async (row: any) => {
  dialogType.value = 'edit';
  try {
    const res = await personnelApi.getById(row.id);
    const data = res.data;
    // 填充表单数据
    form.id = data.id;
    form.name = data.name || '';
    form.gender = data.gender || '';
    form.birth_date = data.birth_date || '';
    form.id_card_no = data.id_card_no || '';
    form.phone = data.phone || '';
    form.email = data.email || '';
    form.education = data.education || '';
    form.graduate_school = data.graduate_school || '';
    form.major = data.major || '';
    form.title = data.title || '';
    form.work_years = data.work_years || 0;
    form.work_start_date = data.work_start_date || '';
    form.employment_date = data.employment_date || '';
    form.personnel_status = data.personnel_status !== undefined ? data.personnel_status : 1;
    form.is_full_time = data.is_full_time !== undefined ? data.is_full_time : 1;
    form.is_principal = data.is_principal !== undefined ? data.is_principal : 0;
    form.work_experience = data.work_experience || '';
    form.project_experience = data.project_experience || '';
    dialogVisible.value = true;
  } catch (error) {
    ElMessage.error('获取人员详情失败');
    console.error('获取人员详情失败:', error);
  }
};

// 资质证书
const handleQualification = (row: any) => {
  qualificationDialogRef.value.openDialog(row);
};

// 删除
const handleDelete = (id: number) => {
  ElMessageBox.confirm('确定要删除这条记录吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await personnelApi.delete(id);
      ElMessage.success('删除成功');
      getPersonnelList();
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
          await personnelApi.create(form);
          ElMessage.success('新增成功');
        } else {
          await personnelApi.update(form);
          ElMessage.success('编辑成功');
        }
        dialogVisible.value = false;
        getPersonnelList();
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
  getPersonnelList();
};

const handleCurrentChange = (current: number) => {
  pagination.page = current;
  getPersonnelList();
};

// 页面挂载时获取数据
onMounted(() => {
  getPersonnelList();
});
</script>

<style scoped lang="scss">
.personnel-container {
  padding: 20px;
  
  .personnel-search {
    margin-bottom: 20px;
  }
  
  .personnel-table {
    width: 100%;
  }
  
  .mb20 {
    margin-bottom: 20px;
  }
  
  :deep(.el-dialog__body) {
    max-height: 600px;
    overflow-y: auto;
  }
}
</style>
