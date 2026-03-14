<template>
  <div class="qualification-edit-container">
    <z-card shadow="hover">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>编辑资质证书</span>
          <el-button type="primary" size="default" @click="handleSubmit" :loading="submitLoading">
            <el-icon>
              <ele-Check/>
            </el-icon>
            保存
          </el-button>
        </div>
      </template>
      <el-form :model="qualificationForm" :rules="qualificationRules" ref="qualificationFormRef" size="default" label-width="120px" v-loading="loading">
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
            <el-form-item label="培训机构/组织" prop="training_institution">
              <el-input v-model="qualificationForm.training_institution" placeholder="请输入培训机构/评审组织" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="备注" prop="remark" class="remark-item">
          <el-input
            v-model="qualificationForm.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入备注"
          />
        </el-form-item>

        <el-form-item label="上传证书" prop="certificate_path" class="upload-item">
          <el-upload
            class="certificate-uploader"
            action="/api/file/upload"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
            :before-upload="beforeUpload"
            accept="image/*"
          >
            <template v-if="qualificationForm.certificate_path">
              <img :src="qualificationForm.certificate_path" class="certificate-image-preview" @error="handleImageError" />
            </template>
            <div v-else class="upload-placeholder">
              <el-icon><ele-Plus /></el-icon>
              <div class="upload-text">点击上传证书图片</div>
            </div>
          </el-upload>
          <div class="upload-tip">支持 JPG、PNG、GIF 格式，文件大小不超过 10MB</div>
        </el-form-item>
      </el-form>
    </z-card>
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
  certificate_path: '',
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

// 图片上传成功回调
const handleUploadSuccess = (response: any) => {
  if (response.code === 200) {
    qualificationForm.certificate_path = response.data.url;
    ElMessage.success('图片上传成功');
  } else {
    ElMessage.error(response.message || '图片上传失败');
  }
};

// 图片上传失败回调
const handleUploadError = () => {
  ElMessage.error('图片上传失败，请重试');
};

// 上传前校验
const beforeUpload = (file: File) => {
  const isImage = file.type.startsWith('image/');
  const isLt10M = file.size / 1024 / 1024 < 10;

  if (!isImage) {
    ElMessage.error('只能上传图片文件！');
    return false;
  }
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过 10MB！');
    return false;
  }
  return true;
};

// 图片加载错误处理
const handleImageError = () => {
  qualificationForm.certificate_path = '';
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
  padding: 30px;
  display: flex;
  justify-content: center;
  position: relative;

  :deep(.el-card) {
    width: 100%;
    max-width: 1200px;
  }

  :deep(.el-card__body) {
    height: auto;
    min-height: auto;
  }

  :deep(.el-form) {
    max-width: 1000px;
    width: 100%;
  }

  :deep(.el-row) {
    margin-bottom: 0;
  }

  :deep(.el-form-item) {
    margin-bottom: 25px;
    min-height: 50px;
  }

  :deep(.el-form-item__label) {
    font-size: 14px;
    font-weight: 500;
    line-height: 36px;
  }

  :deep(.el-form-item__content) {
    line-height: 36px;
  }

  :deep(.el-input) {
    height: 36px;
  }

  :deep(.el-input__wrapper) {
    padding: 0 12px;
    height: 36px;
  }

  :deep(.el-select) {
    height: 36px;
  }

  :deep(.el-select .el-input__wrapper) {
    height: 36px;
  }

  :deep(.el-date-picker) {
    width: 100%;
    height: 36px;
  }

  :deep(.el-textarea) {
    min-height: 100px;
    height: 100px;
    margin-top: 8px;
  }

  :deep(.el-textarea__inner) {
    min-height: 100px;
    height: 100px;
  }

  :deep(.remark-item) {
    margin-bottom: 25px !important;

    .el-textarea {
      min-height: 100px !important;
      height: 100px !important;
    }

    .el-textarea__inner {
      min-height: 100px !important;
      height: 100px !important;
    }
  }

  :deep(.upload-item) {
    margin-top: 0 !important;
    margin-bottom: 25px !important;
  }

  :deep(.certificate-uploader) {
    .el-upload {
      border: 1px dashed var(--el-border-color);
      border-radius: 6px;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      transition: var(--el-transition-duration-fast);
      width: 300px;
      height: 200px;
      display: flex;
      align-items: center;
      justify-content: center;

      &:hover {
        border-color: var(--el-color-primary);
      }
    }
  }

  .certificate-image-preview {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  .upload-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: var(--el-text-color-secondary);
    width: 100%;
    height: 100%;

    .el-icon {
      font-size: 32px;
      margin-bottom: 12px;
      color: var(--el-color-primary);
    }

    .upload-text {
      font-size: 14px;
    }
  }

  .upload-tip {
    margin-top: 8px;
    font-size: 12px;
    color: var(--el-text-color-secondary);
  }
}
</style>
