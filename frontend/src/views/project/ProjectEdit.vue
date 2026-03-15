<template>
  <div class="project-edit-container">
    <z-card shadow="hover">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>{{ isEdit ? '编辑项目' : '新增项目' }}</span>
          <el-button type="primary" size="large" @click="handleSubmit">
            <el-icon>
              <ele-Check/>
            </el-icon>
            保存
          </el-button>
        </div>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="项目名称" prop="name">
              <el-input v-model="form.name" placeholder="请输入项目名称" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="项目编号" prop="project_code">
              <el-input v-model="form.project_code" placeholder="请输入项目编号" clearable />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="项目类型" prop="project_type">
              <el-input v-model="form.project_type" placeholder="请输入项目类型" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="项目地点" prop="project_location">
              <el-input v-model="form.project_location" placeholder="请输入项目地点" clearable />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="招标单位" prop="tender_organization">
              <el-input v-model="form.tender_organization" placeholder="请输入招标单位" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="招标代理机构" prop="tender_agent">
              <el-input v-model="form.tender_agent" placeholder="请输入招标代理机构" clearable />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="招标编号" prop="tender_number">
              <el-input v-model="form.tender_number" placeholder="请输入招标编号" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="项目状态" prop="project_status">
              <el-select v-model="form.project_status" placeholder="请选择项目状态" clearable style="width: 100%">
                <el-option label="投标中" value="投标中" />
                <el-option label="已中标" value="已中标" />
                <el-option label="未中标" value="未中标" />
                <el-option label="已放弃" value="已放弃" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="招标日期" prop="tender_date">
              <el-date-picker
                v-model="form.tender_date"
                type="date"
                placeholder="请选择招标日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="开标日期" prop="bid_open_date">
              <el-date-picker
                v-model="form.bid_open_date"
                type="date"
                placeholder="请选择开标日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="项目预计费用" prop="project_cost">
              <el-input v-model="form.project_cost" type="number" placeholder="请输入项目预计费用" clearable />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </z-card>
  </div>
</template>

<script setup lang="ts" name="ProjectEdit">
import {ref, reactive, onMounted} from 'vue';
import {ElMessage} from 'element-plus';
import {useProjectApi} from '../../api/project/project';
import {useRoute, useRouter} from 'vue-router';

// 定义变量
const formRef = ref();
const projectApi = useProjectApi();
const route = useRoute();
const router = useRouter();

// 获取路由参数
const id = route.query.id as string;
const isEdit = !!id;

// 表单数据
const form = reactive({
  id: null as number | null,
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

// 获取项目详情
const getProjectDetail = async () => {
  if (!id) return;
  try {
    const res = await projectApi.getById(Number(id));
    const data = res.data;
    // 填充表单数据
    form.id = data.id;
    form.name = data.name || '';
    form.project_code = data.project_code || '';
    form.project_type = data.project_type || '';
    form.project_location = data.project_location || '';
    form.tender_organization = data.tender_organization || '';
    form.tender_agent = data.tender_agent || '';
    form.tender_number = data.tender_number || '';
    form.tender_date = data.tender_date || '';
    form.bid_open_date = data.bid_open_date || '';
    form.project_status = data.project_status || '投标中';
    form.project_cost = data.project_cost || '';
  } catch (error) {
    ElMessage.error('获取项目详情失败');
    console.error('获取项目详情失败:', error);
  }
};

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        if (isEdit) {
          await projectApi.update(form);
          ElMessage.success('编辑成功');
        } else {
          await projectApi.create(form);
          ElMessage.success('新增成功');
        }
        // 返回列表页
        router.push('/project');
      } catch (error) {
        ElMessage.error(isEdit ? '编辑失败' : '新增失败');
        console.error('提交失败:', error);
      }
    }
  });
};

// 页面挂载时获取数据
onMounted(() => {
  if (isEdit) {
    getProjectDetail();
  }
});
</script>

<style scoped lang="scss">
.project-edit-container {
  padding: 30px;
  display: flex;
  justify-content: center;
  position: relative;
}

.project-edit-container :deep(.el-card) {
  width: 100%;
  max-width: 1200px;
}

.project-edit-container :deep(.el-card__body) {
  padding: 40px;
  display: flex;
  justify-content: center;
}

.project-edit-container :deep(.el-form) {
  max-width: 1000px;
  width: 100%;
}

.project-edit-container :deep(.el-form-item) {
  margin-bottom: 40px !important;
  min-height: 60px;
}

.project-edit-container :deep(.el-form-item__label) {
  font-size: 14px;
  font-weight: 500;
  line-height: 44px;
}

.project-edit-container :deep(.el-form-item__content) {
  line-height: 44px;
}

.project-edit-container :deep(.el-input) {
  height: 44px;
}

.project-edit-container :deep(.el-input__wrapper) {
  padding: 0 16px;
  height: 44px;
}

.project-edit-container :deep(.el-select) {
  height: 44px;
}

.project-edit-container :deep(.el-select .el-input__wrapper) {
  height: 44px;
}

.project-edit-container :deep(.el-date-picker) {
  width: 100%;
  height: 44px;
}
</style>
