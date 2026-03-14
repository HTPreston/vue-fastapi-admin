<template>
  <div class="personnel-edit-container">
    <z-card shadow="hover">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>{{ isEdit ? '编辑人员' : '新增人员' }}</span>
        </div>
      </template>
      
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
        
        <el-form-item label="工作经历" prop="work_experience" class="textarea-item">
          <el-input
            v-model="form.work_experience"
            type="textarea"
            :rows="8"
            placeholder="请输入工作经历"
          />
        </el-form-item>

        <el-form-item label="项目经验" prop="project_experience" class="textarea-item">
          <el-input
            v-model="form.project_experience"
            type="textarea"
            :rows="8"
            placeholder="请输入项目经验"
          />
        </el-form-item>
      </el-form>
    </z-card>
    
    <!-- 固定保存按钮 -->
    <div class="fixed-save-button">
      <el-button type="primary" size="large" @click="handleSubmit">
        <el-icon>
          <ele-Check/>
        </el-icon>
        保存
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts" name="PersonnelEdit">
import {ref, reactive, onMounted} from 'vue';
import {ElMessage} from 'element-plus';
import {usePersonnelApi} from '../../api/useSystemApi/personnel';
import {useRoute, useRouter} from 'vue-router';

// 定义变量
const formRef = ref();
const personnelApi = usePersonnelApi();
const route = useRoute();
const router = useRouter();

// 获取路由参数
const id = route.query.id as string;
const isEdit = !!id;

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

// 获取人员详情
const getPersonnelDetail = async () => {
  if (isEdit) {
    try {
      const res = await personnelApi.getById(Number(id));
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
    } catch (error) {
      ElMessage.error('获取人员详情失败');
      console.error('获取人员详情失败:', error);
    }
  }
};

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        if (isEdit) {
          await personnelApi.update(form);
          ElMessage.success('编辑成功');
        } else {
          await personnelApi.create(form);
          ElMessage.success('新增成功');
        }
        // 跳转回人员管理页面
        router.push('/personnel');
      } catch (error) {
        ElMessage.error(isEdit ? '编辑失败' : '新增失败');
        console.error('提交失败:', error);
      }
    }
  });
};

// 页面挂载时获取数据
onMounted(() => {
  getPersonnelDetail();
});
</script>

<style scoped lang="scss">
.personnel-edit-container {
  padding: 30px;
  display: flex;
  justify-content: center;
  position: relative;
  min-height: 100vh;
}

.personnel-edit-container .el-card {
  width: 100%;
  max-width: 1200px;
  margin-bottom: 80px; /* 为固定按钮留出空间 */
}

.personnel-edit-container :deep(.el-card__body) {
  padding: 40px;
  display: flex;
  justify-content: center;
}

.personnel-edit-container :deep(.el-form) {
  max-width: 1000px;
  width: 100%;
}

.personnel-edit-container :deep(.el-form-item) {
  margin-bottom: 40px !important;
  min-height: 60px;
}

.personnel-edit-container :deep(.el-form-item__label) {
  font-size: 14px;
  font-weight: 500;
  line-height: 44px;
}

.personnel-edit-container :deep(.el-form-item__content) {
  line-height: 44px;
}

.personnel-edit-container :deep(.el-input) {
  height: 44px;
}

.personnel-edit-container :deep(.el-input__wrapper) {
  padding: 0 16px;
  height: 44px;
}

.personnel-edit-container :deep(.el-select) {
  height: 44px;
}

.personnel-edit-container :deep(.el-select .el-input__wrapper) {
  height: 44px;
}

.personnel-edit-container :deep(.el-date-picker) {
  width: 100%;
  height: 44px;
}

/* 工作经历和项目经验间距 */
.personnel-edit-container :deep(.textarea-item) {
  margin-bottom: 40px !important;
}

.personnel-edit-container :deep(.textarea-item) .el-textarea {
  min-height: auto;
  margin-bottom: 25px;
}

.personnel-edit-container :deep(.textarea-item) .el-textarea__inner {
  min-height: auto;
}

/* 固定保存按钮 */
.fixed-save-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.95);
  padding: 15px 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(10px);
}

.fixed-save-button .el-button {
  padding: 12px 30px;
  font-size: 16px;
}
</style>