<template>
  <div class="project-container">
    <z-card shadow="hover">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>项目管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon>
              <ele-Plus/>
            </el-icon>
            新增项目
          </el-button>
        </div>
      </template>

      <div class="project-search">
        <el-form :inline="true" :model="searchForm" class="mb20">
          <el-form-item label="项目名称">
            <el-input v-model="searchForm.name" placeholder="请输入项目名称" clearable />
          </el-form-item>
          <el-form-item label="项目状态">
            <el-select v-model="searchForm.project_status" placeholder="请选择状态" clearable>
              <el-option label="投标中" value="投标中" />
              <el-option label="已中标" value="已中标" />
              <el-option label="未中标" value="未中标" />
              <el-option label="已放弃" value="已放弃" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="project-cards">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="item in tableData" :key="item.id">
            <el-card class="project-card" shadow="hover" @click="handleView(item)">
              <div class="card-header">
                <span class="project-name">{{ item.name }}</span>
                <el-tag :type="getStatusType(item.project_status)" size="small">
                  {{ item.project_status }}
                </el-tag>
              </div>
              <div class="card-body">
                <div class="info-item">
                  <span class="info-label">项目编号：</span>
                  <span class="info-value">{{ item.project_code || '-' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">项目类型：</span>
                  <span class="info-value">{{ item.project_type || '-' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">项目地点：</span>
                  <span class="info-value">{{ item.project_location || '-' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">招标单位：</span>
                  <span class="info-value">{{ item.tender_organization || '-' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">创建时间：</span>
                  <span class="info-value">{{ item.created_at }}</span>
                </div>
              </div>
              <div class="card-footer">
                <el-button type="primary" size="small" @click.stop="handleEdit(item)">
                  编辑
                </el-button>
                <el-button type="danger" size="small" @click.stop="handleDelete(item.id)">
                  删除
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>

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
      </div>
    </z-card>
  </div>
</template>

<script setup lang="ts" name="projectIndex">
import {ref, reactive, onMounted} from 'vue';
import {ElMessage, ElMessageBox} from 'element-plus';
import {useProjectApi} from '../../api/project/project';
import {useRouter} from 'vue-router';

interface ProjectItem {
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
const loading = ref(false);
const projectApi = useProjectApi();
const router = useRouter();

// 搜索表单
const searchForm = reactive({
  name: '',
  project_status: ''
});

// 表格数据
const tableData = ref<ProjectItem[]>([]);

// 分页数据
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
});

// 获取项目列表
const getProjectList = async () => {
  loading.value = true;
  try {
    const params = {
      name: searchForm.name,
      project_status: searchForm.project_status,
      page: pagination.page,
      page_size: pagination.pageSize
    };
    const res = await projectApi.getList(params);
    tableData.value = res.data.list;
    pagination.total = res.data.total;
  } catch (error) {
    ElMessage.error('获取项目列表失败');
    console.error('获取项目列表失败:', error);
  } finally {
    loading.value = false;
  }
};

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

// 搜索
const handleSearch = () => {
  pagination.page = 1;
  getProjectList();
};

// 重置
const resetForm = () => {
  searchForm.name = '';
  searchForm.project_status = '';
  pagination.page = 1;
  getProjectList();
};

// 查看详情
const handleView = (row: ProjectItem) => {
  router.push(`/project/detail?id=${row.id}`);
};

// 新增
const handleAdd = () => {
  router.push('/project/edit');
};

// 编辑
const handleEdit = (row: ProjectItem) => {
  router.push(`/project/edit?id=${row.id}`);
};

// 删除
const handleDelete = (id: number) => {
  ElMessageBox.confirm('确定要删除这条记录吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await projectApi.delete(id);
      ElMessage.success('删除成功');
      getProjectList();
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
  getProjectList();
};

const handleCurrentChange = (current: number) => {
  pagination.page = current;
  getProjectList();
};

// 页面挂载时获取数据
onMounted(() => {
  getProjectList();
});
</script>

<style scoped lang="scss">
.project-container {
  padding: 20px;

  .project-search {
    margin-bottom: 20px;
  }

  .project-cards {
    width: 100%;

    .project-card {
      margin-bottom: 20px;
      cursor: pointer;
      transition: all 0.3s;
      border-radius: 8px;

      &:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
      }

      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid #e4e7ed;

        .project-name {
          font-size: 16px;
          font-weight: bold;
          color: #303133;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          flex: 1;
          margin-right: 10px;
        }
      }

      .card-body {
        .info-item {
          display: flex;
          margin-bottom: 8px;
          font-size: 14px;

          .info-label {
            color: #606266;
            min-width: 80px;
          }

          .info-value {
            color: #303133;
            flex: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
          }
        }
      }

      .card-footer {
        display: flex;
        justify-content: flex-end;
        margin-top: 15px;
        padding-top: 10px;
        border-top: 1px solid #e4e7ed;
      }
    }
  }

  .mb20 {
    margin-bottom: 20px;
  }
}
</style>
