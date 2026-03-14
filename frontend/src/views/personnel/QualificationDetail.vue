<template>
  <div class="qualification-detail-container">
    <el-page-header @back="goBack" content="资质证书详情" />
    
    <el-card class="detail-card" v-loading="loading">
      <!-- 基本信息 -->
      <div class="section-title">基本信息</div>
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="info-item">
            <span class="info-label">姓名：</span>
            <span class="info-value">{{ qualificationData.personnel_name }}</span>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="info-item">
            <span class="info-label">证书类型：</span>
            <span class="info-value">{{ qualificationData.certificate_type }}</span>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="info-item">
            <span class="info-label">岗位名称：</span>
            <span class="info-value">{{ qualificationData.certificate_title }}</span>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="info-item">
            <span class="info-label">证书全称：</span>
            <span class="info-value">{{ qualificationData.certificate_full_name }}</span>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="info-item">
            <span class="info-label">证书编号：</span>
            <span class="info-value">{{ qualificationData.certificate_no }}</span>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="info-item">
            <span class="info-label">证书等级：</span>
            <span class="info-value">{{ qualificationData.certificate_level }}</span>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="info-item">
            <span class="info-label">证书专业：</span>
            <span class="info-value">{{ qualificationData.certificate_profession }}</span>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="info-item">
            <span class="info-label">证书状态：</span>
            <el-tag :type="qualificationData.certificate_status === '有效' ? 'success' : 'danger'">
              {{ qualificationData.certificate_status }}
            </el-tag>
          </div>
        </el-col>
      </el-row>

      <!-- 发证信息 -->
      <div class="section-title" style="margin-top: 30px;">发证信息</div>
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="info-item">
            <span class="info-label">发证机构：</span>
            <span class="info-value">{{ qualificationData.issue_organization }}</span>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="info-item">
            <span class="info-label">发证日期：</span>
            <span class="info-value">{{ qualificationData.issue_date }}</span>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="info-item">
            <span class="info-label">有效期至：</span>
            <span class="info-value">{{ qualificationData.valid_until }}</span>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="info-item">
            <span class="info-label">专业有效期：</span>
            <span class="info-value">{{ qualificationData.profession_validity }}</span>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="info-item">
            <span class="info-label">培训机构/评审组织：</span>
            <span class="info-value">{{ qualificationData.training_institution }}</span>
          </div>
        </el-col>
      </el-row>

      <!-- 其他信息 -->
      <div class="section-title" style="margin-top: 30px;">其他信息</div>
      <el-row :gutter="20">
        <el-col :span="24">
          <div class="info-item">
            <span class="info-label">备注：</span>
            <span class="info-value">{{ qualificationData.remark || '无' }}</span>
          </div>
        </el-col>
      </el-row>
      
      <div class="certificate-image" style="margin-top: 20px;">
        <el-divider>证书图片</el-divider>
        <el-image
          :src="qualificationData.certificate_path || defaultImage"
          fit="contain"
          style="width: 100%; height: 750px;"
          :preview-src-list="[qualificationData.certificate_path || defaultImage]"
          preview-teleported
        >
          <template #error>
            <div class="image-slot">
              <img :src="defaultImage" style="width: 100%; height: 100%; object-fit: contain;" />
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
import defaultCertificateImage from '/@/assets/img/图片示例.png';

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

// 默认证书图片（使用本地图片）
const defaultImage = defaultCertificateImage;

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

  .section-title {
    font-size: 16px;
    font-weight: bold;
    color: #303133;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid #e4e7ed;
  }

  .info-item {
    display: flex;
    align-items: center;
    padding: 12px 0;
    min-height: 40px;

    .info-label {
      color: #606266;
      font-weight: 500;
      min-width: 120px;
      flex-shrink: 0;
    }

    .info-value {
      color: #303133;
      flex: 1;
    }
  }

  .el-row {
    margin-bottom: 0;
  }

  .certificate-image {
    width: 100%;
    min-height: 750px;

    .image-slot {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 750px;
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
