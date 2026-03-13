<template>
  <div class="qualification-dialog-container">
    <el-dialog
      draggable
      title="资质证书管理"
      v-model="state.isShowDialog"
      width="1000px"
      @close="handleClose"
    >
      <div class="personnel-info">
        <el-descriptions :column="3" border>
          <el-descriptions-item label="姓名">{{ state.currentPersonnel.name }}</el-descriptions-item>
          <el-descriptions-item label="性别">{{ state.currentPersonnel.gender }}</el-descriptions-item>
          <el-descriptions-item label="手机号码">{{ state.currentPersonnel.phone }}</el-descriptions-item>
        </el-descriptions>
      </div>
      
      <div class="qualification-actions" style="margin: 20px 0;">
        <el-button type="primary" @click="handleAdd">
          <el-icon>
            <ele-Plus/>
          </el-icon>
          新增资质证书
        </el-button>
      </div>
      
      <div class="qualification-table">
        <el-table :data="qualificationList" style="width: 100%" v-loading="loading">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="certificate_type" label="证书类型" width="120" />
          <el-table-column prop="certificate_title" label="岗位名称" width="120" />
          <el-table-column prop="certificate_full_name" label="证书全称" width="200" />
          <el-table-column prop="certificate_no" label="证书编号" width="150" />
          <el-table-column prop="certificate_level" label="证书等级" width="100" />
          <el-table-column prop="certificate_profession" label="证书专业" width="120" />
          <el-table-column prop="issue_organization" label="发证机构" width="150" />
          <el-table-column prop="issue_date" label="发证日期" width="120" />
          <el-table-column prop="valid_until" label="有效期至" width="120" />
          <el-table-column prop="certificate_status" label="证书状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.certificate_status === '有效' ? 'success' : 'danger'">
                {{ scope.row.certificate_status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleEdit(scope.row)">
                编辑
              </el-button>
              <el-button type="danger" size="small" @click="handleDelete(scope.row.id)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
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

const qualificationFormRef = ref();
const qualificationApi = useQualificationApi();

const state = reactive({
  isShowDialog: false,
  isShowQualificationDialog: false,
  currentPersonnel: {} as any
});

const loading = ref(false);
const qualificationDialogType = ref('add');
const qualificationList = ref([]);

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

const handleEdit = (row: any) => {
  qualificationDialogType.value = 'edit';
  const copiedRow = JSON.parse(JSON.stringify(row));
  Object.assign(qualificationForm, copiedRow);
  state.isShowQualificationDialog = true;
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
  .personnel-info {
    margin-bottom: 20px;
  }
  
  .qualification-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .qualification-table {
    width: 100%;
  }
  
  :deep(.el-dialog__body) {
    max-height: 600px;
    overflow-y: auto;
  }
}
</style>
