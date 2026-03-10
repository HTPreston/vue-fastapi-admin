<template>
  <el-form size="large" class="login-content-form">
    <el-form-item class="login-animation1">
      <el-input text placeholder="请输入手机号" v-model="state.ruleForm.phone" clearable
                autocomplete="off">
        <template #prefix>
          <el-icon class="el-input__icon">
            <ele-User/>
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item class="login-animation2">
      <el-input :type="state.isShowPassword ? 'text' : 'password'" placeholder="请输入密码"
                v-model="state.ruleForm.password" autocomplete="off">
        <template #prefix>
          <el-icon class="el-input__icon">
            <ele-Unlock/>
          </el-icon>
        </template>
        <template #suffix>
          <i
              class="iconfont el-input__icon login-content-password"
              :class="state.isShowPassword ? 'icon-yincangmima' : 'icon-xianshimima'"
              @click="state.isShowPassword = !state.isShowPassword"
          >
          </i>
        </template>
      </el-input>
    </el-form-item>
    <!-- 验证码功能已注释掉
    <el-form-item class="login-animation3">
      <el-col :span="15">
        <el-input text maxlength="4" placeholder="请输入验证码" v-model="state.ruleForm.code" clearable
                  autocomplete="off">
          <template #prefix>
            <el-icon class="el-input__icon">
              <ele-Position/>
            </el-icon>
          </template>
        </el-input>
      </el-col>
      <el-col :span="1"></el-col>
      <el-col :span="8">
        <el-button class="login-content-code" v-waves>1234</el-button>
      </el-col>
    </el-form-item>
    -->
    <el-form-item class="login-animation3">
      <el-row :gutter="10" style="width: 100%;">
        <el-col :span="12">
          <el-button type="primary" class="login-content-submit" round v-waves @click="onSignIn"
                     :loading="state.loading.signIn">
            <span>登 录</span>
          </el-button>
        </el-col>
        <el-col :span="12">
          <el-button class="login-content-submit" round v-waves @click="onRegister">
            <span>注 册</span>
          </el-button>
        </el-col>
      </el-row>
    </el-form-item>
  </el-form>
</template>

<script setup lang="ts" name="loginAccount">
import {computed, reactive} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {ElMessage} from 'element-plus';
import {storeToRefs} from 'pinia';
import {useThemeConfig} from '/@/stores/themeConfig';
import {initBackEndControlRoutes} from '/@/router/backEnd';
import {Session} from '/@/utils/storage';
import {formatAxis} from '/@/utils/formatTime';
import {NextLoading} from '/@/utils/loading';
import {useUserApi} from "/@/api/useSystemApi/user";
import {useUserStore} from "/@/stores/user";

// 定义变量内容
const storesThemeConfig = useThemeConfig();
const {themeConfig} = storeToRefs(storesThemeConfig);
const route = useRoute();
const router = useRouter();
const state = reactive({
  isShowPassword: false,
  ruleForm: {
    phone: '',
    password: '',
    // code: '1234',  // 验证码功能已注释掉
  },
  loading: {
    signIn: false,
  },
});

// 时间获取
const currentTime = computed(() => {
  return formatAxis(new Date());
});
// 登录
const onSignIn = async () => {
  // 表单验证
  if (!state.ruleForm.phone) {
    ElMessage.warning('请输入手机号');
    return;
  }
  if (!state.ruleForm.password) {
    ElMessage.warning('请输入密码');
    return;
  }
  
  state.loading.signIn = true;
  useUserApi().signIn({phone: state.ruleForm.phone, password: state.ruleForm.password})
      .then(async res => {
        Session.set('token', res.data.token);
        // 清除之前的用户信息缓存，确保获取最新的权限数据
        Session.remove('userInfo');
        // 强制刷新用户信息，获取最新的按钮权限
        await useUserStore().setUserInfos(true);
        await initBackEndControlRoutes();
        // await initFrontEndControlRoutes();
        signInSuccess(false);
      })
      .catch((e) => {
        console.log('错误信息： ', e)
        state.loading.signIn = false;
      })
  // // 存储 token 到浏览器缓存
  // Session.set('token', Math.random().toString(36).substr(0));
  // // 模拟数据，对接接口时，记得删除多余代码及对应依赖的引入。用于 `/src/stores/userInfo.ts` 中不同用户登录判断（模拟数据）
  // Cookies.set('userName', state.ruleForm.userName);
  // if (!themeConfig.value.isRequestRoutes) {
  //   // 前端控制路由，2、请注意执行顺序
  //   const isNoPower = await initFrontEndControlRoutes();
  //   signInSuccess(isNoPower);
  // } else {
  //   // 模拟后端控制路由，isRequestRoutes 为 true，则开启后端控制路由
  //   // 添加完动态路由，再进行 router 跳转，否则可能报错 No match found for location with path "/"
  //   const isNoPower = await initBackEndControlRoutes();
  //   // 执行完 initBackEndControlRoutes，再执行 signInSuccess
  //   signInSuccess(isNoPower);
  // }
};
// 登录成功后的跳转
const signInSuccess = (isNoPower: boolean) => {
  if (isNoPower) {
    ElMessage.warning('抱歉，您没有登录权限');
    Session.clear();
  } else {
    // 初始化登录成功时间问候语
    let currentTimeInfo = currentTime.value;
    // 登录成功，固定跳转到首页
    router.push('/home');
    // 登录成功提示
    const signInText = '欢迎回来！';
    ElMessage.success(`${currentTimeInfo}，${signInText}`);
    // 添加 loading，防止第一次进入界面时出现短暂空白
    NextLoading.start();
  }
  state.loading.signIn = false;
};

// 跳转到注册页面
const onRegister = () => {
  router.push('/register');
};
</script>

<style scoped lang="scss">
.login-content-form {
  margin-top: 20px;

  @for $i from 1 through 4 {
    .login-animation#{$i} {
      opacity: 0;
      animation-name: error-num;
      animation-duration: 0.5s;
      animation-fill-mode: forwards;
      animation-delay: calc($i/10) + s;
    }
  }

  .login-content-password {
    cursor: pointer;
  }

  .login-content-code {
    width: 100%;
    padding: 0;
  }

  .login-content-submit {
    width: 100%;
    letter-spacing: 2px;
    font-weight: 300;
    margin-top: 15px;
  }
}
</style>
