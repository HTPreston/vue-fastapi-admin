<template>
  <div class="qualification-edit-container">
    <el-page-header @back="goBack" content="编辑资质证书" />
    
    <el-card class="edit-card" v-loading="loading">
      <el-form :model="qualificationForm" :rules="qualificationRules" ref="qualificationFormRef" size="default" label-width="140px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="证书类型" prop="certificate_type">
              <el-input v-model="qualificationForm.certificate_type" placeholder="请输入证书类型" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="岗位名称" prop="certificate_title">
              <el-input v-model="qualificationForm.certificate_title" placeholder="请输入岗位名称" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="证书全称" prop="certificate_full_name">
              <el-input v-model="qualificationForm.certificate_full_name" placeholder="请输入证书全称" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="证书编号" prop="certificate_no">
              <el-input v-model="qualificationForm.certificate_no" placeholder="请输入证书编号" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="证书等级" prop="certificate_level">
              <el-input v-model="qualificationForm.certificate_level" placeholder="请输入证书等级" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="证书专业" prop="certificate_profession">
              <el-input v-model="qualificationForm.certificate_profession" placeholder="请输入证书专业" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="发证机构" prop="issue_organization">
              <el-input v-model="qualificationForm.issue_organization" placeholder="请输入发证机构" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="证书状态" prop="certificate_status">
              <el-select v-model="qualificationForm.certificate_status" placeholder="请选择证书状态" clearable style="width: 100%">
                <el-option label="有效" value="有效" />
                <el-option label="无效" value="无效" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="发证日期" prop="issue_date">
              <el-date-picker
                v-model="qualificationForm.issue_date"
                type="date"
                placeholder="请选择发证日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="有效期至" prop="valid_until">
              <el-date-picker
                v-model="qualificationForm.valid_until"
                type="date"
                placeholder="请选择有效期至"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="专业有效期" prop="profession_validity">
              <el-input v-model="qualificationForm.profession_validity" placeholder="请输入专业有效期" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="培训机构/评审组织" prop="training_institution">
              <el-input v-model="qualificationForm.training_institution" placeholder="请输入培训机构/评审组织" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="qualificationForm.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入备注"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitLoading">保 存</el-button>
          <el-button @click="goBack">取 消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts" name="QualificationEdit">
import {reactive, ref, onMounted} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {ElMessage} from 'element-plus';
import {useQualificationApi} from '/@/api/useSystemApi/personnel';

const route = useRoute();
const router = useRouter();
const qualificationApi = useQualificationApi();

const qualificationFormRef = ref();
const loading = ref(false);
const submitLoading = ref(false);

const qualificationForm = reactive({
  id: null as number | null,
  personnel_id: null as number | null,
  personnel_name: '',
  certificate_type: '',
  certificate_title: '',
  certificate_full_name: '',
  certificate_no: '',
  certificate_level: '',
  certificate_profession: '',
  issue_organization: '',
  issue_date: '',
  valid_until: '',
  certificate_status: '有效',
  profession_validity: '',
  training_institution: '',
  remark: ''
});

const qualificationRules = {
  certificate_type: [{required: true, message: '请输入证书类型', trigger: 'blur'}],
  certificate_title: [{required: true, message: '请输入岗位名称', trigger: 'blur'}]
};

const getQualificationDetail = async () => {
  loading.value = true;
  try {
    const id = route.query.id as string;
    if (!id) {
      ElMessage.error('缺少证书ID');
      goBack();
      return;
    }
    
    const res = await qualificationApi.getById(Number(id));
    if (res.data) {
      Object.assign(qualificationForm, res.data);
    }
  } catch (error) {
    ElMessage.error('获取证书详情失败');
    console.error('获取证书详情失败:', error);
  } finally {
    loading.value = false;
  }
};

const handleSubmit = async () => {
  if (!qualificationFormRef.value) return;
  await qualificationFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      submitLoading.value = true;
      try {
        const submitData = {...qualificationForm};
        await qualificationApi.update(submitData);
        ElMessage.success('编辑成功');
        goBack();
      } catch (error) {
        ElMessage.error('编辑失败');
        console.error('编辑失败:', error);
      } finally {
        submitLoading.value = false;
      }
    }
  });
};

const goBack = () => {
  router.back();
};

onMounted(() => {
  getQualificationDetail();
});
</script>

<style scoped lang="scss">
.qualification-edit-container {
  padding: 20px;
  
  .edit-card {
    margin-top: 20px;
  }
}
</style>
