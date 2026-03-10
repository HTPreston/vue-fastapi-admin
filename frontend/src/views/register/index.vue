<template>
  <div class="register-container">
    <div class="register-box">
      <div class="register-title">用户注册</div>
      <el-form
        ref="registerFormRef"
        :model="state.form"
        :rules="state.rules"
        size="large"
        class="register-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="state.form.username"
            placeholder="请输入用户名"
            clearable
            autocomplete="off"
          >
            <template #prefix>
              <el-icon class="el-input__icon">
                <ele-User />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="phone">
          <el-input
            v-model="state.form.phone"
            placeholder="请输入手机号"
            clearable
            autocomplete="off"
          >
            <template #prefix>
              <el-icon class="el-input__icon">
                <ele-Phone />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="state.form.password"
            type="password"
            placeholder="请输入密码"
            clearable
            autocomplete="off"
          >
            <template #prefix>
              <el-icon class="el-input__icon">
                <ele-Unlock />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="confirmPassword">
          <el-input
            v-model="state.form.confirmPassword"
            type="password"
            placeholder="请确认密码"
            clearable
            autocomplete="off"
          >
            <template #prefix>
              <el-icon class="el-input__icon">
                <ele-Unlock />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            class="register-submit"
            round
            v-waves
            @click="onRegister"
            :loading="state.loading"
          >
            <span>注 册</span>
          </el-button>
        </el-form-item>

        <el-form-item>
          <div class="register-footer">
            <span>已有账号？</span>
            <el-button link type="primary" @click="goToLogin">立即登录</el-button>
          </div>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts" name="registerIndex">
import { reactive, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, FormInstance, FormRules } from 'element-plus';
import { useUserApi } from '/@/api/useSystemApi/user';
import { Session } from '/@/utils/storage';

const router = useRouter();
const registerFormRef = ref<FormInstance>();

// 页面加载时清除可能过期的 token，避免影响注册请求
onMounted(() => {
  Session.remove('token');
});

const state = reactive({
  loading: false,
  form: {
    username: '',
    phone: '',
    password: '',
    confirmPassword: '',
  },
  rules: {
    username: [
      { required: true, message: '请输入用户名', trigger: 'blur' },
      { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' },
    ],
    phone: [
      { required: true, message: '请输入手机号', trigger: 'blur' },
      { pattern: /^\d{11}$/, message: '请输入正确的手机号', trigger: 'blur' },
    ],
    password: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' },
    ],
    confirmPassword: [
      { required: true, message: '请确认密码', trigger: 'blur' },
      {
        validator: (rule: any, value: string, callback: Function) => {
          if (value !== state.form.password) {
            callback(new Error('两次输入的密码不一致'));
          } else {
            callback();
          }
        },
        trigger: 'blur',
      },
    ],
  } as FormRules,
});

// 注册
const onRegister = async () => {
  if (!registerFormRef.value) return;

  await registerFormRef.value.validate((valid) => {
    if (valid) {
      state.loading = true;
      // 强制清除 token，确保注册请求不带 token
      Session.remove('token');
      useUserApi()
        .register({
          username: state.form.username,
          phone: state.form.phone,
          password: state.form.password,
        })
        .then((res: any) => {
          ElMessage.success('注册成功');
          // 自动登录：保存 token 和用户信息
          if (res.data && res.data.token) {
            Session.set('token', res.data.token);
            Session.set('userInfo', res.data);
          }
          router.push('/home');
        })
        .catch((error) => {
          console.error('注册失败:', error);
          console.error('错误数据:', error.data);
          // 处理不同格式的错误响应
          let errorMsg = '注册失败';
          if (error.data && error.data.msg) {
            // 拦截器返回的 response.data 格式
            errorMsg = error.data.msg;
          } else if (error.response && error.response.data && error.response.data.msg) {
            // axios 标准错误格式
            errorMsg = error.response.data.msg;
          } else if (error.msg) {
            errorMsg = error.msg;
          } else if (typeof error === 'string') {
            errorMsg = error;
          }
          ElMessage.error(errorMsg);
        })
        .finally(() => {
          state.loading = false;
        });
    }
  });
};

// 跳转到登录页
const goToLogin = () => {
  router.push('/login');
};
</script>

<style scoped lang="scss">
.register-container {
  width: 100%;
  height: 100vh;
  background: url('/@/assets/login-bg.png') no-repeat center center;
  background-size: cover;
  display: flex;
  align-items: center;
  justify-content: center;

  .register-box {
    width: 400px;
    padding: 40px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 10px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

    .register-title {
      font-size: 24px;
      font-weight: bold;
      text-align: center;
      margin-bottom: 30px;
      color: var(--el-text-color-primary);
    }

    .register-form {
      .register-submit {
        width: 100%;
        letter-spacing: 2px;
        font-weight: 300;
      }

      .register-footer {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        color: var(--el-text-color-regular);
      }
    }
  }
}
</style>
