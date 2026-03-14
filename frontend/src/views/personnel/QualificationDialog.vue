<template>
  <div class="qualification-dialog-container">
    <el-dialog
      draggable
      v-model="state.isShowDialog"
      width="900px"
      :show-close="false"
      @close="handleClose"
    >
      <template #header>
        <div class="dialog-header" style="margin-top: 10px;">
          <span class="dialog-title" style="padding-left: 10px;">资质证书管理</span>
          <el-button type="primary" @click="handleAdd" style="margin-right: 10px;">
            <el-icon>
              <ele-Plus/>
            </el-icon>
            新增资质证书
          </el-button>
        </div>
      </template>

      <hr style="opacity: 0.3; margin: 10px 0;"/>
      
      <div class="qualification-cards" v-loading="loading" style="margin-top: 20px;">
        <el-empty v-if="!qualificationList || qualificationList.length === 0" description="暂无资质证书" />
        <div v-else class="cards-container">
          <el-card 
            v-for="item in qualificationList" 
            :key="item.id" 
            class="qualification-card"
            shadow="hover"
            @click="handleCardClick(item)"
          >
            <div class="card-content">
              <div class="card-header">
                <div class="personnel-name">{{ item.personnel_name }}</div>
                <el-tag :type="item.certificate_status === '有效' ? 'success' : 'danger'" size="small">
                  {{ item.certificate_status }}
                </el-tag>
              </div>
              
              <div class="card-body">
                <div class="info-row">
                  <span class="label">证书类型：</span>
                  <span class="value">{{ item.certificate_type }}</span>
                </div>
                <div class="info-row">
                  <span class="label">岗位名称：</span>
                  <span class="value">{{ item.certificate_title }}</span>
                </div>
                <div class="info-row">
                  <span class="label">证书等级：</span>
                  <span class="value">{{ item.certificate_level }}</span>
                </div>
                <div class="info-row">
                  <span class="label">发证日期：</span>
                  <span class="value">{{ item.issue_date }}</span>
                </div>
              </div>
              
              <div class="card-actions" @click.stop>
                <el-button type="primary" size="small" @click="handleEdit(item)">
                  修改
                </el-button>
                <el-button type="danger" size="small" @click="handleDelete(item.id)">
                  删除
                </el-button>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </el-dialog>
    
    <!-- 新增/编辑资质证书对话框 -->
    <el-dialog
      draggable
      :title="qualificationDialogType === 'add' ? '新增资质证书' : '编辑资质证书'"
      v-model="state.isShowQualificationDialog"
      width="800px"
      @close="handleQualificationClose"
    >
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
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleQualificationClose">取 消</el-button>
          <el-button type="primary" @click="handleQualificationSubmit">保 存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="QualificationDialog">
import {reactive, ref} from 'vue';
import {ElMessage, ElMessageBox} from 'element-plus';
import {useQualificationApi} from '/@/api/useSystemApi/personnel';
import {useRouter} from 'vue-router';

interface QualificationItem {
  id: number;
  personnel_id: number;
  personnel_name: string;
  certificate_type: string;
  certificate_title: string;
  certificate_full_name: string;
  certificate_no: string;
  certificate_level: string;
  certificate_profession: string;
  issue_organization: string;
  issue_date: string;
  valid_until: string;
  certificate_status: string;
  profession_validity: string;
  training_institution: string;
  certificate_path: string;
  remark: string;
}

const qualificationFormRef = ref();
const qualificationApi = useQualificationApi();
const router = useRouter();

const state = reactive({
  isShowDialog: false,
  isShowQualificationDialog: false,
  currentPersonnel: {} as any
});

const loading = ref(false);
const qualificationDialogType = ref('add');
const qualificationList = ref<QualificationItem[]>([]);

const createQualificationForm = () => {
  return {
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
  };
};

const qualificationForm = reactive(createQualificationForm());

const qualificationRules = {
  certificate_type: [{required: true, message: '请输入证书类型', trigger: 'blur'}],
  certificate_title: [{required: true, message: '请输入岗位名称', trigger: 'blur'}]
};

const openDialog = (personnel: any) => {
  state.currentPersonnel = personnel;
  state.isShowDialog = true;
  getQualificationList();
};

const getQualificationList = async () => {
  loading.value = true;
  try {
    const params = {
      personnel_id: state.currentPersonnel.id,
      page: 1,
      page_size: 100
    };
    const res = await qualificationApi.getList(params);
    qualificationList.value = res.data.list || [];
  } catch (error) {
    ElMessage.error('获取资质证书列表失败');
    console.error('获取资质证书列表失败:', error);
  } finally {
    loading.value = false;
  }
};

const handleAdd = () => {
  qualificationDialogType.value = 'add';
  const newForm = createQualificationForm();
  Object.assign(qualificationForm, newForm);
  qualificationForm.personnel_id = state.currentPersonnel.id;
  qualificationForm.personnel_name = state.currentPersonnel.name;
  state.isShowQualificationDialog = true;
};

const handleEdit = (item: any) => {
  router.push({
    path: '/personnel/qualification-edit',
    query: {
      id: item.id,
      personnel_id: item.personnel_id
    }
  });
};

const handleDelete = (id: number) => {
  ElMessageBox.confirm('确定要删除这条记录吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await qualificationApi.delete(id);
      ElMessage.success('删除成功');
      getQualificationList();
    } catch (error) {
      ElMessage.error('删除失败');
      console.error('删除失败:', error);
    }
  }).catch(() => {
    // 取消删除
  });
};

const handleCardClick = (item: any) => {
  router.push({
    path: '/personnel/qualification-detail',
    query: {
      id: item.id,
      personnel_id: item.personnel_id
    }
  });
};

const handleQualificationClose = () => {
  state.isShowQualificationDialog = false;
};

const handleQualificationSubmit = async () => {
  if (!qualificationFormRef.value) return;
  await qualificationFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        const submitData = {...qualificationForm};
        if (qualificationDialogType.value === 'add') {
          await qualificationApi.create(submitData);
          ElMessage.success('新增成功');
        } else {
          await qualificationApi.update(submitData);
          ElMessage.success('编辑成功');
        }
        state.isShowQualificationDialog = false;
        getQualificationList();
      } catch (error) {
        ElMessage.error(qualificationDialogType.value === 'add' ? '新增失败' : '编辑失败');
        console.error('提交失败:', error);
      }
    }
  });
};

const handleClose = () => {
  state.isShowDialog = false;
};

defineExpose({
  openDialog
});
</script>

<style scoped lang="scss">
.qualification-dialog-container {
  .dialog-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    
    .dialog-title {
      font-size: 18px;
      font-weight: 500;
      color: #303133;
    }
  }
  
  .qualification-cards {
    width: 100%;
    min-height: 200px;
  }
  
  .cards-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
  
  .qualification-card {
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
    
    .card-content {
      display: flex;
      flex-direction: column;
      height: 100%;
    }
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 15px;
      padding-bottom: 10px;
      border-bottom: 1px solid #ebeef5;
      
      .personnel-name {
        font-size: 16px;
        font-weight: bold;
        color: #303133;
      }
    }
    
    .card-body {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-bottom: 15px;
      
      .info-row {
        display: flex;
        align-items: center;
        
        .label {
          color: #909399;
          font-size: 14px;
          min-width: 80px;
        }
        
        .value {
          color: #303133;
          font-size: 14px;
          flex: 1;
        }
      }
    }
    
    .card-actions {
      display: flex;
      gap: 10px;
      padding-top: 10px;
      border-top: 1px solid #ebeef5;
      
      .el-button {
        flex: 1;
      }
    }
  }
  
  :deep(.el-dialog__body) {
    max-height: 700px;
    overflow-y: auto;
  }
}
</style>
