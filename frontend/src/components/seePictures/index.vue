<template>
  <div>
    <el-dialog title="更换头像"
               destroy-on-close
               v-model="state.isShowDialog"
               width="769px">
      <template #header>
        <div style="display:flex;">
          <span style="margin-right: 10px">更换头像</span>
          <slot>
            <el-upload :before-upload="beforeUpload" :showUploadList='false'>
              <el-button type="primary">选择图片</el-button>
            </el-upload>
          </slot>
        </div>
      </template>
      <div class="cropper-warp">
        <div class="cropper-warp-left">
          <img :src="state.cropperImg" class="cropper-warp-left-img" id="AvatarRef"/>
        </div>
        <div class="cropper-warp-right">
          <div class="cropper-warp-right-title">预览</div>
          <div class="cropper-warp-right-item">
            <div class="cropper-warp-right-value">
              <img :src="state.cropperImgBase64" class="cropper-warp-right-value-img"/>
            </div>
            <div class="cropper-warp-right-label">100 x 100</div>
          </div>
          <div class="cropper-warp-right-item">
            <div class="cropper-warp-right-value">
              <img :src="state.cropperImgBase64" class="cropper-warp-right-value-img cropper-size"/>
            </div>
            <div class="cropper-warp-right-label">50 x 50</div>
          </div>
        </div>
      </div>
      <template #footer>
				<span class="dialog-footer">
					<el-button @click="onCancel" size="default">取 消</el-button>
					<el-button type="primary" @click="onSubmit" size="default">更 换</el-button>
				</span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="cropper">
import {reactive, nextTick, ref, onBeforeUnmount} from 'vue';
import Cropper from 'cropperjs';
import 'cropperjs/dist/cropper.css';

const emit = defineEmits(['updateAvatar'])

const AvatarRef = ref()
const state = reactive({
  isShowDialog: false,
  cropperImg: '',
  cropperImgBase64: '',
  cropper: null as Cropper | null,
});

const openDialog = (imgs: string) => {
  /**
   * 打开头像裁剪弹窗
   * 
   * @param {string} imgs - 初始图片URL
   */
  state.cropperImg = imgs;
  state.isShowDialog = true;
  nextTick(() => {
    initCropper();
  });
};

const closeDialog = () => {
  /**
   * 关闭头像裁剪弹窗
   * 
   * 销毁cropper实例并隐藏弹窗
   */
  destroyCropper();
  state.isShowDialog = false;
};

const onCancel = () => {
  /**
   * 取消操作
   * 
   * 关闭弹窗不保存更改
   */
  closeDialog();
};

const onSubmit = () => {
  /**
   * 提交裁剪后的头像
   * 
   * 生成裁剪后的图片Base64数据并触发更新事件
   */
  if (!state.cropper) {
    console.error('Cropper instance not initialized');
    return;
  }
  
  try {
    state.cropperImgBase64 = state.cropper.getCroppedCanvas().toDataURL('image/jpeg', 0.9);
    emit("updateAvatar", state.cropperImgBase64);
    closeDialog();
  } catch (error) {
    console.error('Failed to crop image:', error);
  }
};

const initCropper = () => {
  /**
   * 初始化图片裁剪器
   * 
   * 创建Cropper实例并配置裁剪参数
   */
  destroyCropper();
  
  const imgElement = AvatarRef.value as HTMLImageElement;
  if (!imgElement) {
    console.error('AvatarRef element not found');
    return;
  }
  
  state.cropper = new Cropper(imgElement, {
    viewMode: 1,
    dragMode: 'none',
    initialAspectRatio: 1,
    aspectRatio: 1,
    preview: '.cropper-warp-right-value',
    background: false,
    autoCropArea: 0.6,
    zoomOnWheel: true,
    crop: () => {
      /**
       * 裁剪事件回调
       * 
       * 实时更新预览图片
       */
      try {
        if (state.cropper) {
          state.cropperImgBase64 = state.cropper.getCroppedCanvas().toDataURL('image/jpeg', 0.9);
        }
      } catch (error) {
        console.error('Failed to preview cropped image:', error);
      }
    },
  });
};

const destroyCropper = () => {
  /**
   * 销毁图片裁剪器
   * 
   * 释放cropper实例资源
   */
  if (state.cropper) {
    state.cropper.destroy();
    state.cropper = null;
  }
};

const beforeUpload = (file: File) => {
  /**
   * 上传前文件验证
   * 
   * 验证文件类型和大小，并将图片加载到裁剪器中
   * 
   * @param {File} file - 上传的文件对象
   * @returns {boolean} 是否阻止默认上传行为
   */
  if (!file.type.startsWith('image/')) {
    console.error('Please select an image file');
    return false;
  }
  
  if (file.size > 5 * 1024 * 1024) {
    console.error('Image size should be less than 5MB');
    return false;
  }
  
  if (!state.cropper) {
    console.error('Cropper instance not initialized');
    return false;
  }
  
  try {
    const objectUrl = URL.createObjectURL(file);
    state.cropper.replace(objectUrl);
  } catch (error) {
    console.error('Failed to load image:', error);
  }
  
  return false;
};

onBeforeUnmount(() => {
  /**
   * 组件卸载前清理
   * 
   * 销毁cropper实例防止内存泄漏
   */
  destroyCropper();
});

defineExpose({
  openDialog,
  state,
});
</script>

<style scoped lang="scss">
.cropper-warp {
  display: flex;

  .cropper-warp-left {
    position: relative;
    display: inline-block;
    height: 350px;
    flex: 1;
    border: 1px solid var(--el-border-color);
    background: var(--el-color-white);
    overflow: hidden;
    background-repeat: no-repeat;
    cursor: move;
    border-radius: var(--el-border-radius-base);

    .cropper-warp-left-img {
      width: 100%;
      height: 100%;
    }
  }

  .cropper-warp-right {
    width: 150px;
    height: 350px;

    .cropper-warp-right-title {
      text-align: center;
      height: 20px;
      line-height: 20px;
    }

    .cropper-warp-right-item {
      margin: 15px 0;

      .cropper-warp-right-value {
        overflow: hidden;
        margin: auto;
        border-radius: var(--el-border-radius-circle);

        .cropper-warp-right-value-img {
          margin: auto;
          width: 100px;
          height: 100px;
        }

        .cropper-size {
          width: 50px;
          height: 50px;
        }
      }

      .cropper-warp-right-label {
        text-align: center;
        font-size: 12px;
        color: var(--el-text-color-primary);
        height: 30px;
        line-height: 30px;
      }
    }
  }
}
</style>
