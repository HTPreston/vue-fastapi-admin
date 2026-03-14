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
      
      <div class="personnel-cards" v-loading="loading">
        <div class="personnel-card" v-for="item in tableData" :key="item.id" @click="handleDetail(item)">
          <div class="card-header">
            <h3 class="name">{{ item.name }}</h3>
            <el-tag 
              :type="item.personnel_status === 1 ? 'success' : item.personnel_status === 0 ? 'danger' : 'warning'"
            >
              {{ item.personnel_status === 1 ? '在职' : item.personnel_status === 0 ? '离职' : '休假' }}
            </el-tag>
          </div>
          <div class="card-body">
            <div class="info-item">
              <span class="label">职称：</span>
              <span class="value">{{ item.title || '无' }}</span>
            </div>
            <div class="info-item">
              <span class="label">工作年限：</span>
              <span class="value">{{ item.work_years }}年</span>
            </div>
            <div class="info-item">
              <span class="label">性别：</span>
              <span class="value">{{ item.gender }}</span>
            </div>
            <div class="info-item">
              <span class="label">手机号码：</span>
              <span class="value">{{ item.phone }}</span>
            </div>
            <div class="info-item">
              <span class="label">入职日期：</span>
              <span class="value">{{ item.employment_date }}</span>
            </div>
          </div>
          <div class="card-footer">
            <el-button type="primary" size="small" @click.stop="handleEdit(item)" style="margin-right: 8px">
              编辑
            </el-button>
            <el-button type="success" size="small" @click.stop="handleQualification(item)" style="margin-right: 8px">
              资质证书
            </el-button>
            <el-button type="danger" size="small" @click.stop="handleDelete(item.id)">
              删除
            </el-button>
          </div>
        </div>
      </div>
      
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
    </z-card>
    

    
    <!-- 资质证书对话框 -->
    <QualificationDialog ref="qualificationDialogRef" />
  </div>
</template>

<script setup lang="ts" name="personnelIndex">
import {ref, reactive, onMounted} from 'vue';
import {ElMessage, ElMessageBox} from 'element-plus';
import {usePersonnelApi} from '../../api/useSystemApi/personnel';
import {useRouter} from 'vue-router';
import QualificationDialog from './QualificationDialog.vue';

// 定义变量
const loading = ref(false);
const qualificationDialogRef = ref();
const personnelApi = usePersonnelApi();
const router = useRouter();

// 搜索表单
const searchForm = reactive({
  name: '',
  gender: '',
  personnel_status: null as number | null,
  is_full_time: null as number | null
});

// 人员数据类型定义
interface PersonnelItem {
  id: number;
  name: string;
  gender: string;
  phone: string;
  email: string;
  education: string;
  title: string;
  work_years: number;
  is_full_time: number;
  personnel_status: number;
  employment_date: string;
  work_experience?: string;
  project_experience?: string;
}

// 表格数据
const tableData = ref<PersonnelItem[]>([]);

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
  // 跳转到编辑页面（不带id参数表示新增）
  router.push('/personnel/edit');
};

// 编辑
const handleEdit = (row: any) => {
  // 跳转到编辑页面
  router.push({
    path: '/personnel/edit',
    query: { id: row.id }
  });
};

// 详情
const handleDetail = (row: any) => {
  // 跳转到详情页面
  router.push({
    path: '/personnel/detail',
    query: { id: row.id }
  });
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
  
  .personnel-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
  }
  
  .personnel-card {
    background: #ffffff;
    border: 1px solid #ebeef5;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: all 0.3s ease;
    
    &:hover {
      box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.15);
      transform: translateY(-2px);
    }
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      
      .name {
        font-size: 18px;
        font-weight: 600;
        color: #303133;
        margin: 0;
      }
    }
    
    .card-body {
      margin-bottom: 20px;
      
      .info-item {
        display: flex;
        margin-bottom: 8px;
        
        .label {
          width: 80px;
          color: #909399;
          font-size: 14px;
        }
        
        .value {
          flex: 1;
          color: #303133;
          font-size: 14px;
        }
      }
    }
    
    .card-footer {
      display: flex;
      justify-content: flex-start;
      padding-top: 16px;
      border-top: 1px solid #ebeef5;
    }
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
