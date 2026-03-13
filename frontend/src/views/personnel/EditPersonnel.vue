<template>
  <div class="edit-personnel-container">
    <el-dialog
      draggable
      :title="state.dialogType === 'add' ? '新增人员' : '编辑人员'"
      v-model="state.isShowDialog"
      width="900px"
      @close="handleClose"
    >
      <el-form :model="state.form" :rules="state.rules" ref="formRef" size="default" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="state.form.name" placeholder="请输入姓名" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="state.form.gender" placeholder="请选择性别" clearable style="width: 100%">
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
                v-model="state.form.birth_date"
                type="date"
                placeholder="请选择出生日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="身份证号码" prop="id_card_no">
              <el-input v-model="state.form.id_card_no" placeholder="请输入身份证号码" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="state.form.phone" placeholder="请输入手机号码" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="电子邮箱" prop="email">
              <el-input v-model="state.form.email" placeholder="请输入电子邮箱" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="学历" prop="education">
              <el-input v-model="state.form.education" placeholder="请输入学历" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="毕业院校" prop="graduate_school">
              <el-input v-model="state.form.graduate_school" placeholder="请输入毕业院校" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="专业" prop="major">
              <el-input v-model="state.form.major" placeholder="请输入专业" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="职称" prop="title">
              <el-input v-model="state.form.title" placeholder="请输入职称" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="工作年限" prop="work_years">
              <el-input-number v-model="state.form.work_years" :min="0" placeholder="请输入工作年限" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="参加工作时间" prop="work_start_date">
              <el-date-picker
                v-model="state.form.work_start_date"
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
                v-model="state.form.employment_date"
                type="date"
                placeholder="请选择入职日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="人员状态" prop="personnel_status">
              <el-select v-model="state.form.personnel_status" placeholder="请选择人员状态" clearable style="width: 100%">
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
              <el-select v-model="state.form.is_full_time" placeholder="请选择" clearable style="width: 100%">
                <el-option label="是" :value="1" />
                <el-option label="否" :value="0" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="是否公司负责人" prop="is_principal">
              <el-select v-model="state.form.is_principal" placeholder="请选择" clearable style="width: 100%">
                <el-option label="是" :value="1" />
                <el-option label="否" :value="0" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="工作经历" prop="work_experience">
          <el-input
            v-model="state.form.work_experience"
            type="textarea"
            :rows="3"
            placeholder="请输入工作经历"
          />
        </el-form-item>
        
        <el-form-item label="项目经验" prop="project_experience">
          <el-input
            v-model="state.form.project_experience"
            type="textarea"
            :rows="3"
            placeholder="请输入项目经验"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleClose">取 消</el-button>
          <el-button type="primary" @click="handleSubmit">保 存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="EditPersonnel">
import {reactive, ref} from 'vue';
import {ElMessage} from 'element-plus';
import {usePersonnelApi} from '/@/api/useSystemApi/personnel';

const emit = defineEmits(['getList']);
const formRef = ref();
const personnelApi = usePersonnelApi();

const createForm = () => {
  return {
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
  };
};

const state = reactive({
  isShowDialog: false,
  dialogType: 'add',
  form: createForm(),
  rules: {
    name: [{required: true, message: '请输入姓名', trigger: 'blur'}],
    phone: [{required: true, message: '请输入手机号码', trigger: 'blur'}]
  }
});

const openDialog = (type: string, row: any) => {
  state.dialogType = type;
  if (row) {
    const copiedRow = JSON.parse(JSON.stringify(row));
    state.form.id = copiedRow.id;
    state.form.name = copiedRow.name || '';
    state.form.gender = copiedRow.gender || '';
    state.form.birth_date = copiedRow.birth_date || '';
    state.form.id_card_no = copiedRow.id_card_no || '';
    state.form.phone = copiedRow.phone || '';
    state.form.email = copiedRow.email || '';
    state.form.education = copiedRow.education || '';
    state.form.graduate_school = copiedRow.graduate_school || '';
    state.form.major = copiedRow.major || '';
    state.form.title = copiedRow.title || '';
    state.form.work_years = copiedRow.work_years || 0;
    state.form.work_start_date = copiedRow.work_start_date || '';
    state.form.employment_date = copiedRow.employment_date || '';
    state.form.personnel_status = copiedRow.personnel_status !== undefined ? copiedRow.personnel_status : 1;
    state.form.is_full_time = copiedRow.is_full_time !== undefined ? copiedRow.is_full_time : 1;
    state.form.is_principal = copiedRow.is_principal !== undefined ? copiedRow.is_principal : 0;
    state.form.work_experience = copiedRow.work_experience || '';
    state.form.project_experience = copiedRow.project_experience || '';
  } else {
    const newForm = createForm();
    Object.assign(state.form, newForm);
  }
  state.isShowDialog = true;
};

const handleClose = () => {
  state.isShowDialog = false;
};

const handleSubmit = async () => {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        const submitData = {...state.form};
        if (state.dialogType === 'add') {
          await personnelApi.create(submitData);
          ElMessage.success('新增成功');
        } else {
          await personnelApi.update(submitData);
          ElMessage.success('编辑成功');
        }
        state.isShowDialog = false;
        emit('getList');
      } catch (error) {
        ElMessage.error(state.dialogType === 'add' ? '新增失败' : '编辑失败');
        console.error('提交失败:', error);
      }
    }
  });
};

defineExpose({
  openDialog
});
</script>

<style scoped lang="scss">
.edit-personnel-container {
  :deep(.el-dialog__body) {
    max-height: 600px;
    overflow-y: auto;
  }
}
</style>
