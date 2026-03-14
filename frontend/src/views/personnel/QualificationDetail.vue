<template>
  <div class="qualification-detail-container">
    <el-page-header @back="goBack" content="资质证书详情" />
    
    <el-card class="detail-card" v-loading="loading">
      <el-descriptions title="基本信息" :column="2" border>
        <el-descriptions-item label="姓名">{{ qualificationData.personnel_name }}</el-descriptions-item>
        <el-descriptions-item label="证书类型">{{ qualificationData.certificate_type }}</el-descriptions-item>
        <el-descriptions-item label="岗位名称">{{ qualificationData.certificate_title }}</el-descriptions-item>
        <el-descriptions-item label="证书全称">{{ qualificationData.certificate_full_name }}</el-descriptions-item>
        <el-descriptions-item label="证书编号">{{ qualificationData.certificate_no }}</el-descriptions-item>
        <el-descriptions-item label="证书等级">{{ qualificationData.certificate_level }}</el-descriptions-item>
        <el-descriptions-item label="证书专业">{{ qualificationData.certificate_profession }}</el-descriptions-item>
        <el-descriptions-item label="证书状态">
          <el-tag :type="qualificationData.certificate_status === '有效' ? 'success' : 'danger'">
            {{ qualificationData.certificate_status }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
      
      <el-descriptions title="发证信息" :column="2" border style="margin-top: 20px;">
        <el-descriptions-item label="发证机构">{{ qualificationData.issue_organization }}</el-descriptions-item>
        <el-descriptions-item label="发证日期">{{ qualificationData.issue_date }}</el-descriptions-item>
        <el-descriptions-item label="有效期至">{{ qualificationData.valid_until }}</el-descriptions-item>
        <el-descriptions-item label="专业有效期">{{ qualificationData.profession_validity }}</el-descriptions-item>
        <el-descriptions-item label="培训机构/评审组织" :span="2">
          {{ qualificationData.training_institution }}
        </el-descriptions-item>
      </el-descriptions>
      
      <el-descriptions title="其他信息" :column="1" border style="margin-top: 20px;">
        <el-descriptions-item label="备注">
          {{ qualificationData.remark || '无' }}
        </el-descriptions-item>
      </el-descriptions>
      
      <div class="certificate-image" v-if="qualificationData.certificate_path" style="margin-top: 20px;">
        <el-divider>证书图片</el-divider>
        <el-image
          :src="qualificationData.certificate_path"
          fit="contain"
          style="width: 100%; max-height: 500px;"
          :preview-src-list="[qualificationData.certificate_path]"
          preview-teleported
        >
          <template #error>
            <div class="image-slot">
              <el-icon><ele-Picture /></el-icon>
              <span>图片加载失败</span>
            </div>
          </template>
        </el-image>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts" name="QualificationDetail">
import {reactive, ref, onMounted} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {ElMessage} from 'element-plus';
import {useQualificationApi} from '/@/api/useSystemApi/personnel';

const route = useRoute();
const router = useRouter();
const qualificationApi = useQualificationApi();

const loading = ref(false);
const qualificationData = reactive({
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
  certificate_status: '',
  profession_validity: '',
  training_institution: '',
  certificate_path: '',
  remark: ''
});

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
      Object.assign(qualificationData, res.data);
    }
  } catch (error) {
    ElMessage.error('获取证书详情失败');
    console.error('获取证书详情失败:', error);
  } finally {
    loading.value = false;
  }
};

const goBack = () => {
  router.back();
};

onMounted(() => {
  getQualificationDetail();
});
</script>

<style scoped lang="scss">
.qualification-detail-container {
  padding: 20px;
  
  .detail-card {
    margin-top: 20px;
  }
  
  .certificate-image {
    .image-slot {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 300px;
      background-color: #f5f7fa;
      color: #909399;
      font-size: 14px;
      
      .el-icon {
        font-size: 48px;
        margin-bottom: 10px;
      }
    }
  }
}
</style>
