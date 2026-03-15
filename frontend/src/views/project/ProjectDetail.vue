<template>
  <div class="project-detail-container">
    <z-card shadow="hover">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>项目详情</span>
          <el-button type="primary" @click="handleEdit">
            <el-icon>
              <ele-Edit/>
            </el-icon>
            编辑
          </el-button>
        </div>
      </template>

      <div class="detail-content">
        <div class="detail-section">
          <div class="section-title">基本信息</div>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <span class="detail-label">项目名称：</span>
                <span class="detail-value">{{ projectData.name || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <span class="detail-label">项目编号：</span>
                <span class="detail-value">{{ projectData.project_code || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <span class="detail-label">项目类型：</span>
                <span class="detail-value">{{ projectData.project_type || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <span class="detail-label">项目地点：</span>
                <span class="detail-value">{{ projectData.project_location || '-' }}</span>
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="detail-section">
          <div class="section-title">招标信息</div>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <span class="detail-label">招标单位：</span>
                <span class="detail-value">{{ projectData.tender_organization || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <span class="detail-label">招标代理机构：</span>
                <span class="detail-value">{{ projectData.tender_agent || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <span class="detail-label">招标编号：</span>
                <span class="detail-value">{{ projectData.tender_number || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <span class="detail-label">招标日期：</span>
                <span class="detail-value">{{ projectData.tender_date || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <span class="detail-label">开标日期：</span>
                <span class="detail-value">{{ projectData.bid_open_date || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <span class="detail-label">项目预计费用：</span>
                <span class="detail-value">{{ projectData.project_cost || '-' }}</span>
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="detail-section">
          <div class="section-title">状态信息</div>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <span class="detail-label">项目状态：</span>
                <el-tag :type="getStatusType(projectData.project_status)" size="small">
                  {{ projectData.project_status || '-' }}
                </el-tag>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <span class="detail-label">创建时间：</span>
                <span class="detail-value">{{ projectData.created_at || '-' }}</span>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>

      <div class="detail-footer">
        <el-button @click="handleBack">返回</el-button>
      </div>
    </z-card>
  </div>
</template>

<script setup lang="ts" name="ProjectDetail">
import {ref, onMounted} from 'vue';
import {ElMessage} from 'element-plus';
import {useProjectApi} from '../../api/project/project';
import {useRoute, useRouter} from 'vue-router';

interface ProjectData {
  id: number;
  name: string;
  project_code: string;
  project_type: string;
  project_location: string;
  tender_organization: string;
  tender_agent: string;
  tender_number: string;
  tender_date: string;
  bid_open_date: string;
  project_status: string;
  project_cost: string;
  created_at: string;
}

// 定义变量
const projectApi = useProjectApi();
const route = useRoute();
const router = useRouter();

// 获取路由参数
const id = route.query.id as string;

// 项目数据
const projectData = ref<ProjectData>({
  id: 0,
  name: '',
  project_code: '',
  project_type: '',
  project_location: '',
  tender_organization: '',
  tender_agent: '',
  tender_number: '',
  tender_date: '',
  bid_open_date: '',
  project_status: '',
  project_cost: '',
  created_at: ''
});

// 获取状态类型
const getStatusType = (status: string) => {
  switch (status) {
    case '投标中': return 'warning';
    case '已中标': return 'success';
    case '未中标': return 'info';
    case '已放弃': return 'danger';
    default: return 'default';
  }
};

// 获取项目详情
const getProjectDetail = async () => {
  if (!id) {
    ElMessage.error('项目ID不存在');
    return;
  }
  try {
    const res = await projectApi.getById(Number(id));
    const data = res.data;
    projectData.value = {
      id: data.id,
      name: data.name || '',
      project_code: data.project_code || '',
      project_type: data.project_type || '',
      project_location: data.project_location || '',
      tender_organization: data.tender_organization || '',
      tender_agent: data.tender_agent || '',
      tender_number: data.tender_number || '',
      tender_date: data.tender_date || '',
      bid_open_date: data.bid_open_date || '',
      project_status: data.project_status || '',
      project_cost: data.project_cost || '',
      created_at: data.created_at || ''
    };
  } catch (error) {
    ElMessage.error('获取项目详情失败');
    console.error('获取项目详情失败:', error);
  }
};

// 编辑
const handleEdit = () => {
  router.push(`/project/edit?id=${id}`);
};

// 返回
const handleBack = () => {
  router.push('/project');
};

// 页面挂载时获取数据
onMounted(() => {
  getProjectDetail();
});
</script>

<style scoped lang="scss">
.project-detail-container {
  padding: 30px;
  display: flex;
  justify-content: center;
}

.project-detail-container :deep(.el-card) {
  width: 100%;
  max-width: 1200px;
}

.project-detail-container :deep(.el-card__body) {
  padding: 40px;
}

.detail-content {
  max-width: 1000px;
  margin: 0 auto;
}

.detail-section {
  margin-bottom: 40px;

  &:last-child {
    margin-bottom: 0;
  }
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e4e7ed;
}

.detail-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  font-size: 14px;
  min-height: 44px;
}

.detail-label {
  color: #606266;
  min-width: 100px;
  font-weight: 500;
}

.detail-value {
  color: #303133;
  flex: 1;
}

.detail-footer {
  display: flex;
  justify-content: center;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
}
</style>
