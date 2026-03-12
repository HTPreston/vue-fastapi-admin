<template>
  <div class="personal layout-pd">
    <el-row :gutter="20">
      <!-- 个人信息 -->
      <el-col :xs="24" :sm="8" style="padding: 0 10px">
        <z-card class="personal-card" shadow="hover">
          <div class="personal-user">
            <div class="personal-user-avatar" @click="onCropperDialogOpen">
              <el-avatar 
                :size="100"
                :src="state.userInfoForm.avatar"
                title="点击更换头像"
                :style="state.userInfoForm.avatar ? {'--el-avatar-bg-color': 'transparent'} : {}"
                style="cursor: pointer;"
              >
                <span style="font-size: 40px">{{ state.userInfoForm.username ? state.userInfoForm.username.slice(0, 1).toUpperCase() : '' }}</span>
              </el-avatar>
            </div>
            <div class="personal-user-right">
              <el-row>
                <el-col :span="24">
                  <div class="personal-user-name">
                    <strong>{{ state.userInfoForm.username }}</strong>
                  </div>
                </el-col>
                <el-col :span="24">
                  <div class="personal-user-description">
                    <div>
                      <span>{{ state.userInfoForm.remarks }}</span>
                    </div>
                  </div>
                </el-col>
                <el-col :span="24">
                  <el-divider content-position="left">个人信息</el-divider>
                </el-col>

                <el-col :span="24">
                  <div class="personal-item">
                    <div class="personal-item-label">用户名：</div>
                    <div class="personal-item-value">{{ state.userInfoForm.username }}</div>
                  </div>
                </el-col>

                <el-col :span="24">
                  <div class="personal-item">
                    <div class="personal-item-label">手机号：</div>
                    <div class="personal-item-value">{{ userInfos.phone }}</div>
                  </div>
                </el-col>
                
                <el-col :span="24">
                  <div class="personal-item">
                    <div class="personal-item-label">登录时间：</div>
                    <div class="personal-item-value">{{ userInfos.login_time }}</div>
                  </div>
                </el-col>
                <el-col :span="24">
                  <el-button type="primary" @click="state.showEditPage = !state.showEditPage">
                    <el-icon>
                      <ele-Position/>
                    </el-icon>
                    个人信息
                  </el-button>
                </el-col>
                <el-col :span="24">
                  <el-divider content-position="left">个性标签</el-divider>
                </el-col>
                <el-col :span="24">
                  <div class="personal-item-tag">
                    <el-tag
                      v-for="tag in state.userInfoForm.tags"
                      :key="tag"
                      size="default"
                      type="success"
                      :style="{ marginLeft: '0.25rem', marginRight: '0.25rem' }"
                      :disable-transitions="false"
                    >{{ tag }}</el-tag>
                  </div>
                </el-col>
              </el-row>
            </div>
          </div>
        </z-card>
      </el-col>
      <!-- 登录记录 -->
      <el-col :xs="24" :sm="16" class="pl15 personal-info">
        <z-card class="personal-card" shadow="hover">
          <template #header>
            <span>登录记录</span>
          </template>
          <div class="login-record-box">
            <el-table :data="state.loginRecords" style="width: 100%" size="small" v-loading="state.loading">
              <el-table-column prop="user_name" label="用户名" width="120">
                <template #default="{ row }">
                  {{ row.user_name || '未知用户' }}
                </template>
              </el-table-column>
              <el-table-column prop="phone" label="手机号" width="120">
                <template #default="{ row }">
                  {{ row.phone || '未知手机号' }}
                </template>
              </el-table-column>
              <el-table-column prop="login_time" label="登录时间" width="160">
                <template #default="{ row }">
                  {{ row.login_time || '未知时间' }}
                </template>
              </el-table-column>
              <el-table-column prop="login_ip" label="IP地址" width="130">
                <template #default="{ row }">
                  {{ row.login_ip || '未知IP' }}
                </template>
              </el-table-column>
              <el-table-column prop="login_type" label="登录方式" width="100">
                <template #default="{ row }">
                  <el-tag size="small" :type="row.login_type === '账号密码' ? 'primary' : 'success'">
                    {{ row.login_type || '账号密码' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="ret_code" label="状态" width="80">
                <template #default="{ row }">
                  <el-tag size="small" :type="row.ret_code === '0' ? 'success' : 'danger'">
                    {{ row.ret_code === '0' ? '成功' : '失败' }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
            <div class="pagination-container" v-if="state.loginRecordsTotal > 0">
              <el-pagination
                small
                background
                layout="prev, pager, next"
                :total="state.loginRecordsTotal"
                :page-size="state.loginRecordsPageSize"
                :current-page="state.loginRecordsPage"
                @current-change="handleLoginRecordsPageChange"
              />
            </div>
            <el-empty v-if="!state.loading && state.loginRecords.length === 0" description="暂无登录记录" />
          </div>
        </z-card>
      </el-col>
    </el-row>
    <!-- 更新信息 -->
    <el-dialog title="更新个人信息" destroy-on-close v-model="state.showEditPage" :close-on-click-modal="true" width="30%">
      <z-card class="personal-edit">
        <div class="personal-edit-title">基本信息</div>
        <el-form :model="state.userInfoForm" size="default" label-width="auto" class="mt35 mb35">
          <el-row :gutter="35">

            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
              <el-form-item label="用户名">
                <el-input v-model="state.userInfoForm.username" placeholder="请输入用户名" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
              <el-form-item label="手机号">
                <el-input v-model="state.userInfoForm.phone" placeholder="请输入手机号" disabled></el-input>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
              <el-form-item label="邮箱">
                <el-input v-model="state.userInfoForm.email" :placeholder="state.userInfoForm.email ? '' : '未绑定'" disabled></el-input>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
              <el-form-item label="签名">
                <el-input v-model="state.userInfoForm.remarks" placeholder="请输入签名" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
              <el-form-item label="个性标签">
                <el-tag
                  v-for="tag in state.userInfoForm.tags"
                  :key="tag"
                  size="default"
                  type="success"
                  closable
                  :style="{ marginLeft: '0.25rem', marginRight: '0.25rem' }"
                  :disable-transitions="false"
                  @close="removeTag(tag)"
                >{{ tag }}</el-tag>
                <el-input
                  v-if="state.editTag"
                  ref="UserTagInputRef"
                  v-model="state.tagValue"
                  class="ml-1 w-20"
                  size="small"
                  @keyup.enter="addTag"
                  @blur="addTag"
                  style="width: 100px"
                />
                <el-button v-else size="small" @click="showEditTag">+ New Tag</el-button>
              </el-form-item>
            </el-col>
          </el-row>
          <div class="personal-edit-footer">
            <el-button type="primary" @click="save">更新</el-button>
          </div>
        </el-form>
        <div class="personal-edit-title mt35">账户安全</div>
        <div class="personal-security-buttons">
          <el-button type="primary" @click="updatePassword">修改密码</el-button>
          <el-button type="warning" @click="updatePhone">修改手机号</el-button>
          <el-button :type="state.userInfoForm.email ? 'warning' : 'success'" @click="updateEmail">
            {{ state.userInfoForm.email ? '修改邮箱' : '绑定邮箱' }}
          </el-button>
        </div>
      </z-card>
    </el-dialog>
    
    <el-dialog title="修改手机号" destroy-on-close v-model="state.showPhoneDialog" width="400px">
      <el-form :model="state.phoneForm" :rules="state.phoneRules" ref="phoneFormRef" size="default" label-width="80px">
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="state.phoneForm.phone" placeholder="请输入新手机号" clearable></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="state.showPhoneDialog = false">取 消</el-button>
        <el-button type="primary" @click="savePhone">确 定</el-button>
      </template>
    </el-dialog>

    <el-dialog :title="state.userInfoForm.email ? '修改邮箱' : '绑定邮箱'" destroy-on-close v-model="state.showEmailDialog" width="400px">
      <el-form :model="state.emailForm" :rules="state.emailRules" ref="emailFormRef" size="default" label-width="80px">
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="state.emailForm.email" placeholder="请输入邮箱" clearable></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="state.showEmailDialog = false">取 消</el-button>
        <el-button type="primary" @click="saveEmail">确 定</el-button>
      </template>
    </el-dialog>
    
    <SeePictures ref="SeePicturesRef" @updateAvatar="updateAvatar"></SeePictures>
    <ResetPassword ref="ResetPasswordRef"></ResetPassword>
  </div>
</template>

<script setup lang="ts" name="personal">
import {defineAsyncComponent, nextTick, onMounted, reactive, ref} from 'vue';
import {useUserStore} from "/@/stores/user";
import {useIdCenterApi} from "/@/api/useSystemApi/idCenter";
import {ElMessage} from "element-plus";
import {storeToRefs} from "pinia";
import ResetPassword from "/@/views/system/personal/ResetPassword.vue";

const SeePictures = defineAsyncComponent(() => import("/@/components/seePictures/index.vue"))
const SeePicturesRef = ref();
const UserTagInputRef = ref();
const phoneFormRef = ref();
const emailFormRef = ref();
const ResetPasswordRef = ref();

const userStores = useUserStore()
const {userInfos} = storeToRefs(userStores);

interface LoginRecord {
  login_time: string;
  login_ip: string;
  login_type: string;
  ret_code: string;
  user_name: string;
  phone: string;
}

const state = reactive({
  loginRecords: [] as LoginRecord[],
  loginRecordsTotal: 0,
  loginRecordsPage: 1,
  loginRecordsPageSize: 10,
  loading: false,
  userInfoForm: {
    id: null as number | null,
    username: '',
    phone: '',
    avatar: '',
    remarks: '',
    email: '',
    tags: [] as string[],
  },
  editTag: false,
  tagValue: "",
  showEditPage: false,
  showPhoneDialog: false,
  showEmailDialog: false,
  cropperImg: '',
  phoneForm: {
    phone: ''
  },
  phoneRules: {
    phone: [{required: true, message: '请输入手机号', trigger: 'blur'}]
  },
  emailForm: {
    email: ''
  },
  emailRules: {
    email: [
      {required: true, message: '请输入邮箱', trigger: 'blur'},
      {type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur'}
    ]
  }
});

const getUserInfo = async () => {
  try {
    let {data} = await useIdCenterApi().getUserInfo()
    if (data) {
      state.userInfoForm = {
        id: data.id || null,
        username: data.username || '',
        phone: data.phone || '',
        avatar: data.avatar || '',
        remarks: data.remarks || '',
        email: data.email || '',
        tags: data.tags || [],
      }
    }
  } catch (error) {
    console.error('获取个人信息失败:', error)
    ElMessage.error('获取个人信息失败')
  }
}

const onCropperDialogOpen = () => {
  SeePicturesRef.value.openDialog(state.userInfoForm.avatar);
};

const showEditTag = () => {
  state.editTag = true
  nextTick(() => {
    UserTagInputRef.value?.input.focus()
  })
}

const removeTag = (tag: string) => {
  state.userInfoForm.tags.splice(state.userInfoForm.tags.indexOf(tag), 1)
}

const addTag = () => {
  if (state.editTag && state.tagValue) {
    if (!state.userInfoForm.tags) state.userInfoForm.tags = []
    state.userInfoForm.tags.push(state.tagValue)
  }
  state.editTag = false
  state.tagValue = ''
}

const save = async () => {
  try {
    await useIdCenterApi().updateProfile({
      username: state.userInfoForm.username,
      phone: state.userInfoForm.phone,
      email: state.userInfoForm.email,
      avatar: state.userInfoForm.avatar,
      remarks: state.userInfoForm.remarks,
      tags: state.userInfoForm.tags,
    })
    ElMessage.success("更新成功!╰(*°▽°*)╯😍")
    state.showEditPage = false
    await getUserInfo()
    await userStores.setUserInfos(true)
  } catch (error) {
    console.error('更新失败:', error)
    ElMessage.error('更新失败，请重试')
  }
}

const updateAvatar = async (img: string) => {
  try {
    state.userInfoForm.avatar = img
    await useIdCenterApi().updateAvatar({avatar: img})
    userInfos.value.avatar = img
    await userStores.updateUserInfo(userInfos.value)
    ElMessage.success("更新成功!╰(*°▽°*)╯😍")
  } catch (error) {
    console.error('更新头像失败:', error)
    ElMessage.error('更新头像失败，请重试')
  }
}

const updatePassword = () => {
  ResetPasswordRef.value.openDialog(userInfos.value)
}

const updatePhone = () => {
  state.phoneForm.phone = userInfos.value.phone || ''
  state.showPhoneDialog = true
}

const savePhone = async () => {
  try {
    await phoneFormRef.value.validate()
    await useIdCenterApi().updatePhone({phone: state.phoneForm.phone})
    userInfos.value.phone = state.phoneForm.phone
    await userStores.updateUserInfo(userInfos.value)
    ElMessage.success("更新成功!╰(*°▽°*)╯😍")
    state.showPhoneDialog = false
  } catch (error) {
    console.error('更新手机号失败:', error)
    ElMessage.error('更新手机号失败，请重试')
  }
}

const updateEmail = () => {
  state.emailForm.email = userInfos.value.email || ''
  state.showEmailDialog = true
}

const saveEmail = async () => {
  try {
    await emailFormRef.value.validate()
    await useIdCenterApi().updateEmail({email: state.emailForm.email})
    userInfos.value.email = state.emailForm.email
    state.userInfoForm.email = state.emailForm.email
    await userStores.updateUserInfo(userInfos.value)
    ElMessage.success("更新成功!╰(*°▽°*)╯😍")
    state.showEmailDialog = false
  } catch (error) {
    console.error('更新邮箱失败:', error)
    ElMessage.error('更新邮箱失败，请重试')
  }
}

const getLoginRecords = async () => {
  state.loading = true
  try {
    const {data} = await useIdCenterApi().getLoginRecords({
      page: state.loginRecordsPage,
      pageSize: state.loginRecordsPageSize
    })
    if (data) {
      state.loginRecords = data.rows || []
      state.loginRecordsTotal = data.rowTotal || 0
    }
  } catch (error) {
    console.error('获取登录记录失败:', error)
  } finally {
    state.loading = false
  }
}

const handleLoginRecordsPageChange = (page: number) => {
  state.loginRecordsPage = page
  getLoginRecords()
}

onMounted(() => {
  nextTick(() => {
    getUserInfo()
    getLoginRecords()
  })
})
</script>

<style scoped lang="scss">
@import '../../../theme/mixins/index.scss';

.personal {
  .personal-card {
    height: 100%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
  }

  :deep(.el-card__header) {
    flex-shrink: 0;
  }

  :deep(.el-card__body) {
    flex: 1;
    overflow: auto;
  }

  .personal-user {
    align-items: center;
    padding: 20px;

    .personal-user-avatar {
      width: 100px;
      height: 100px;
      margin: auto;
      border-radius: 3px;
      margin-bottom: 20px;

      img {
        cursor: pointer;
        width: 100%;
        height: 100%;
        border-radius: 50%;
      }
    }

    .personal-user-right {
      flex: 1;
      padding: 0 15px;

      .personal-user-name {
        text-align: center;
        font-size: 20px;
        margin-bottom: 10px;
      }

      .personal-user-description {
        text-align: center;
      }

      .personal-title {
        font-size: 18px;
        @include text-ellipsis(1);
      }

      .personal-item {
        display: flex;
        align-items: center;
        font-size: 13px;
        height: 30px;
        width: 100%;
        flex-flow: wrap;

        .personal-item-label {
          color: var(--el-text-color-secondary);
          @include text-ellipsis(1);
        }

        .personal-item-value {
          @include text-ellipsis(1);
        }
      }

      .personal-item-tag {
        .personal-item-tag-item {
          margin: 5px;
          float: left;
        }
      }
    }
  }

  .personal-info {
    .personal-info-box {
      height: 130px;
      overflow: hidden;

      .personal-info-ul {
        list-style: none;

        .personal-info-li {
          font-size: 13px;
          padding-bottom: 10px;

          .personal-info-li-title {
            display: inline-block;
            @include text-ellipsis(1);
            color: var(--el-text-color-secondary);
            text-decoration: none;
          }

          & a:hover {
            color: var(--el-color-primary);
            cursor: pointer;
          }
        }
      }
    }

    .login-record-box {
      min-height: 300px;

      .pagination-container {
        margin-top: 15px;
        display: flex;
        justify-content: flex-end;
      }
    }
  }

  .personal-edit {
    .personal-edit-title {
      position: relative;
      padding-left: 10px;
      color: var(--el-text-color-regular);

      &::after {
        content: '';
        width: 2px;
        height: 16px;
        background-color: var(--el-color-primary);
        position: absolute;
        left: 0;
        top: 2px;
      }
    }

    .personal-security-buttons {
      margin-top: 20px;
      display: flex;
      gap: 10px;
    }

    .personal-edit-footer {
      margin-top: 20px;
      display: flex;
      justify-content: center;
    }
  }
}
</style>
