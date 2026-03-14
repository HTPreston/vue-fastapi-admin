<template>
  <div class="personnel-detail-container">
    <z-card shadow="hover">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>人员详情</span>
          <el-button @click="handleBack">
            <el-icon>
              <ele-ArrowLeft/>
            </el-icon>
            返回
          </el-button>
        </div>
      </template>
      
      <div class="personnel-info">
        <div class="info-section">
          <h3 class="section-title">基本信息</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">姓名：</span>
              <span class="value">{{ personnelInfo.name }}</span>
            </div>
            <div class="info-item">
              <span class="label">性别：</span>
              <span class="value">{{ personnelInfo.gender }}</span>
            </div>
            <div class="info-item">
              <span class="label">出生日期：</span>
              <span class="value">{{ personnelInfo.birth_date }}</span>
            </div>
            <div class="info-item">
              <span class="label">身份证号码：</span>
              <span class="value">{{ personnelInfo.id_card_no }}</span>
            </div>
            <div class="info-item">
              <span class="label">手机号码：</span>
              <span class="value">{{ personnelInfo.phone }}</span>
            </div>
            <div class="info-item">
              <span class="label">电子邮箱：</span>
              <span class="value">{{ personnelInfo.email }}</span>
            </div>
          </div>
        </div>
        
        <div class="info-section">
          <h3 class="section-title">工作信息</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">学历：</span>
              <span class="value">{{ personnelInfo.education }}</span>
            </div>
            <div class="info-item">
              <span class="label">毕业院校：</span>
              <span class="value">{{ personnelInfo.graduate_school }}</span>
            </div>
            <div class="info-item">
              <span class="label">专业：</span>
              <span class="value">{{ personnelInfo.major }}</span>
            </div>
            <div class="info-item">
              <span class="label">职称：</span>
              <span class="value">{{ personnelInfo.title }}</span>
            </div>
            <div class="info-item">
              <span class="label">工作年限：</span>
              <span class="value">{{ personnelInfo.work_years }}年</span>
            </div>
            <div class="info-item">
              <span class="label">参加工作时间：</span>
              <span class="value">{{ personnelInfo.work_start_date }}</span>
            </div>
            <div class="info-item">
              <span class="label">入职日期：</span>
              <span class="value">{{ personnelInfo.employment_date }}</span>
            </div>
            <div class="info-item">
              <span class="label">人员状态：</span>
              <span class="value">
                <el-tag :type="getTagType(personnelInfo.personnel_status)">
                  {{ getStatusText(personnelInfo.personnel_status) }}
                </el-tag>
              </span>
            </div>
            <div class="info-item">
              <span class="label">是否专职：</span>
              <span class="value">{{ personnelInfo.is_full_time === 1 ? '是' : '否' }}</span>
            </div>
            <div class="info-item">
              <span class="label">是否公司负责人：</span>
              <span class="value">{{ personnelInfo.is_principal === 1 ? '是' : '否' }}</span>
            </div>
          </div>
        </div>
        
        <div class="info-section">
          <h3 class="section-title">其他信息</h3>
          <div class="info-text">
            <div class="text-item">
              <span class="label">工作经历：</span>
              <div class="text-content">{{ personnelInfo.work_experience || '无' }}</div>
            </div>
            <div class="text-item">
              <span class="label">项目经验：</span>
              <div class="text-content">{{ personnelInfo.project_experience || '无' }}</div>
            </div>
          </div>
        </div>
      </div>
    </z-card>
  </div>
</template>

<script setup lang="ts" name="PersonnelDetail">
import {ref, reactive, onMounted} from 'vue';
import {ElMessage} from 'element-plus';
import {usePersonnelApi} from '../../api/useSystemApi/personnel';
import {useRoute, useRouter} from 'vue-router';

// 定义变量
const personnelApi = usePersonnelApi();
const route = useRoute();
const router = useRouter();

// 获取路由参数
const id = route.query.id as string;

// 人员信息
const personnelInfo = reactive({
  id: null,
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

// 获取人员详情
const getPersonnelDetail = async () => {
  if (id) {
    try {
      const res = await personnelApi.getById(Number(id));
      const data = res.data;
      // 填充人员信息
      Object.assign(personnelInfo, data);
    } catch (error) {
      ElMessage.error('获取人员详情失败');
      console.error('获取人员详情失败:', error);
    }
  }
};

// 返回人员管理页面
const handleBack = () => {
  router.push('/personnel');
};

// 获取状态标签类型
const getTagType = (status: number) => {
  switch (status) {
    case 1:
      return 'success';
    case 0:
      return 'danger';
    case 2:
      return 'warning';
    default:
      return 'info';
  }
};

// 获取状态文本
const getStatusText = (status: number) => {
  switch (status) {
    case 1:
      return '在职';
    case 0:
      return '离职';
    case 2:
      return '休假';
    default:
      return '未知';
  }
};

// 页面挂载时获取数据
onMounted(() => {
  getPersonnelDetail();
});
</script>

<style scoped lang="scss">
.personnel-detail-container {
  padding: 30px;
  
  .info-section {
    margin-bottom: 30px;
    
    .section-title {
      font-size: 18px;
      font-weight: 600;
      margin-bottom: 16px;
      color: #303133;
      border-bottom: 1px solid #ebeef5;
      padding-bottom: 8px;
    }
  }
  
  .info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 16px;
  }
  
  .info-item {
    display: flex;
    align-items: center;
    
    .label {
      width: 120px;
      color: #909399;
      font-size: 14px;
    }
    
    .value {
      flex: 1;
      color: #303133;
      font-size: 14px;
    }
  }
  
  .info-text {
    .text-item {
      margin-bottom: 20px;
      
      .label {
        display: block;
        color: #909399;
        font-size: 14px;
        margin-bottom: 8px;
      }
      
      .text-content {
        color: #303133;
        font-size: 14px;
        line-height: 1.6;
        white-space: pre-wrap;
        background: #f5f7fa;
        padding: 12px;
        border-radius: 4px;
      }
    }
  }
}
</style>