<template>
  <div class="icon-selector w100 h100">
    <el-input
        v-model="state.fontIconSearch"
        :placeholder="state.fontIconPlaceholder"
        :clearable="clearable"
        :disabled="disabled"
        :size="size"
        ref="inputWidthRef"
        @clear="onClearFontIcon"
        @focus="onIconFocus"
        @blur="onIconBlur"
        class="icon-selector-input"
    >
      <template #prepend>
        <SvgIcon
            :name="state.fontIconPrefix === '' ? prepend : state.fontIconPrefix"
            class="font16"
            v-if="state.fontIconPrefix === '' ? prepend?.indexOf('ele-') > -1 : state.fontIconPrefix?.indexOf('ele-') > -1"
        />
        <i v-else :class="state.fontIconPrefix === '' ? prepend : state.fontIconPrefix" class="font16"></i>
      </template>
    </el-input>
    <el-popover
        placement="bottom"
        :width="state.fontIconWidth"
        transition="el-zoom-in-top"
        popper-class="icon-selector-popper"
        trigger="click"
        :virtual-ref="inputWidthRef"
        virtual-triggering
    >
      <template #default>
        <div class="icon-selector-warp">
          <div class="icon-selector-content">
            <div class="icon-categories">
              <el-tabs v-model="state.currentCategory" @tab-click="onCategoryChange">
                <el-tab-pane label="全部" name="all"></el-tab-pane>
                <el-tab-pane label="方向性图标" name="directional"></el-tab-pane>
                <el-tab-pane label="提示性图标" name="notification"></el-tab-pane>
                <el-tab-pane label="操作类图标" name="operation"></el-tab-pane>
                <el-tab-pane label="设备类图标" name="device"></el-tab-pane>
                <el-tab-pane label="其他图标" name="other"></el-tab-pane>
              </el-tabs>
            </div>
            <IconList :list="fontIconSheetsFilterList" :empty="emptyDescription" :prefix="state.fontIconPrefix"
                      @get-icon="onColClick"/>
          </div>
        </div>
      </template>
    </el-popover>
  </div>
</template>

<script setup lang="ts" name="iconSelector">
import {defineAsyncComponent, ref, reactive, onMounted, nextTick, computed, watch} from 'vue';
import initIconfont from '/@/utils/getStyleSheets';
import '/@/theme/iconSelector.scss';
// 定义父组件传过来的值
const props = defineProps({

  // 输入框前置内容
  prepend: {
    type: String,
    default: () => 'ele-Pointer',
  },
  // 输入框占位文本
  placeholder: {
    type: String,
    default: () => '请选择图标',
  },
  // 输入框占位文本
  size: {
    type: String,
    default: () => 'default',
  },
  // 禁用
  disabled: {
    type: Boolean,
    default: () => false,
  },
  // 是否可清空
  clearable: {
    type: Boolean,
    default: () => true,
  },
  // 自定义空状态描述文字
  emptyDescription: {
    type: String,
    default: () => '无相关图标',
  },
  // 双向绑定值，默认为 modelValue，
  // 参考：https://v3.cn.vuejs.org/guide/migration/v-model.html#%E8%BF%81%E7%A7%BB%E7%AD%96%E7%95%A5
  // 参考：https://v3.cn.vuejs.org/guide/component-custom-events.html#%E5%A4%9A%E4%B8%AA-v-model-%E7%BB%91%E5%AE%9A
  modelValue: String,
});

// 定义子组件向父组件传值/事件
const emit = defineEmits(['update:modelValue', 'get', 'clear']);

// 引入组件
const IconList = defineAsyncComponent(() => import('/@/components/iconSelector/list.vue'));

// 定义变量内容
const inputWidthRef = ref();
const state = reactive({
  fontIconPrefix: '',
  fontIconWidth: 0,
  fontIconSearch: '',
  fontIconPlaceholder: '',
  currentCategory: 'all',
  fontIconList: {
    all: [],
    categories: {
      directional: [], // 方向性图标
      notification: [], // 提示性图标
      operation: [], // 操作类图标
      device: [], // 设备类图标
      other: [] // 其他图标
    }
  },
});

// 处理 input 获取焦点时，modelValue 有值时，改变 input 的 placeholder 值
const onIconFocus = () => {
  if (!props.modelValue) return false;
  state.fontIconSearch = '';
  state.fontIconPlaceholder = props.modelValue;
};
// 处理 input 失去焦点时，为空将清空 input 值，为点击选中图标时，将取原先值
const onIconBlur = () => {
  const list = fontIconTabNameList();
  setTimeout(() => {
    const icon = list.filter((icon: string) => icon === state.fontIconSearch);
    if (icon.length <= 0) state.fontIconSearch = '';
  }, 300);
};
// 图标搜索及图标数据显示
const fontIconSheetsFilterList = computed(() => {
  const list = fontIconTabNameList();
  if (!state.fontIconSearch) return list;
  let search = state.fontIconSearch.trim().toLowerCase();
  return list.filter((item: string) => {
    if (item.toLowerCase().indexOf(search) !== -1) return item;
  });
});
// 根据当前分类返回对应的图标列表
const fontIconTabNameList = () => {
  if (state.currentCategory === 'all') {
    return state.fontIconList.all;
  } else {
    return state.fontIconList.categories[state.currentCategory as keyof typeof state.fontIconList.categories] || [];
  }
};
// 处理 icon 双向绑定数值回显
const initModeValueEcho = () => {
  if (props.modelValue === '') return ((<string | undefined>state.fontIconPlaceholder) = props.placeholder);
  (<string | undefined>state.fontIconPlaceholder) = props.modelValue;
  (<string | undefined>state.fontIconPrefix) = props.modelValue;
};
// 处理 icon 类型，用于初始化数据
const initFontIconName = () => {
  return 'ele';
};
// 初始化数据
const initFontIconData = async (name: string) => {
  // element plus 图标
  if (state.fontIconList.all.length > 0) return;
  await initIconfont.ele().then((res: any) => {
    state.fontIconList.all = res.all;
    state.fontIconList.categories = res.categories;
  });
  // 初始化 input 的 placeholder
  // 参考（单项数据流）：https://cn.vuejs.org/v2/guide/components-props.html?#%E5%8D%95%E5%90%91%E6%95%B0%E6%8D%AE%E6%B5%81
  state.fontIconPlaceholder = props.placeholder;
  // 初始化双向绑定回显
  initModeValueEcho();
};
// 图标点击切换（保留函数结构以保持兼容性）
const onIconClick = () => {
  initFontIconData('ele');
  inputWidthRef.value.focus();
};

// 分类切换事件处理
const onCategoryChange = () => {
  inputWidthRef.value.focus();
};
// 获取当前点击的 icon 图标
const onColClick = (v: string) => {
  state.fontIconPlaceholder = v;
  state.fontIconPrefix = v;
  emit('get', state.fontIconPrefix);
  emit('update:modelValue', state.fontIconPrefix);
  inputWidthRef.value.focus();
};
// 清空当前点击的 icon 图标
const onClearFontIcon = () => {
  state.fontIconPrefix = '';
  emit('clear', state.fontIconPrefix);
  emit('update:modelValue', state.fontIconPrefix);
};
// 获取 input 的宽度
const getInputWidth = () => {
  nextTick(() => {
    state.fontIconWidth = inputWidthRef.value.$el.offsetWidth;
  });
};
// 监听页面宽度改变
const initResize = () => {
  window.addEventListener('resize', () => {
    getInputWidth();
  });
};
// 页面加载时
onMounted(() => {
  initFontIconData(initFontIconName());
  initResize();
  getInputWidth();
});
// 监听双向绑定 modelValue 的变化
watch(
    () => props.modelValue,
    () => {
      initModeValueEcho();
      initFontIconName();
    }
  );
</script>

<style scoped lang="scss">
.icon-selector {
  .icon-selector-input {
    border-radius: 8px;
    border: 1px solid var(--el-border-color);
    transition: all 0.3s ease;
    
    &:hover {
      border-color: var(--el-color-primary);
      box-shadow: 0 0 0 2px rgba(103, 194, 58, 0.1);
    }
    
    &:focus-within {
      border-color: var(--el-color-primary);
      box-shadow: 0 0 0 2px rgba(103, 194, 58, 0.2);
    }
    
    .el-input__prefix {
      padding: 0 8px;
      
      .font16 {
        font-size: 16px;
        color: var(--el-text-color-primary);
      }
    }
    
    .el-input__inner {
      padding: 10px 12px;
      font-size: 14px;
    }
    
    .el-input__suffix {
      padding: 0 8px;
      
      .el-input__clear {
        font-size: 14px;
        
        &:hover {
          color: var(--el-color-primary);
        }
      }
    }
  }
}
</style>
