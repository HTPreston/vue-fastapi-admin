<template>
	<div class="icon-selector-warp-row">
		<el-scrollbar ref="selectorScrollbarRef">
			<el-row :gutter="15" v-if="props.list.length > 0">
				<el-col :xs="4" :sm="3" :md="3" :lg="3" :xl="3" v-for="(v, k) in list" :key="k">
					<div class="icon-selector-warp-item" :class="{ 'icon-selector-active': prefix === v }" @click="onColClick(v)">
						<SvgIcon :name="v" />
					</div>
				</el-col>
			</el-row>
			<el-empty :image-size="100" v-if="list.length <= 0" :description="empty"></el-empty>
		</el-scrollbar>
	</div>
</template>

<script setup lang="ts" name="iconSelectorList">
// 定义父组件传过来的值
const props = defineProps({
	// 图标列表数据
	list: {
		type: Array,
		default: () => [],
	},
	// 自定义空状态描述文字
	empty: {
		type: String,
		default: () => '无相关图标',
	},
	// 高亮当前选中图标
	prefix: {
		type: String,
		default: () => '',
	},
});

// 定义子组件向父组件传值/事件
const emit = defineEmits(['get-icon']);



// 当前 icon 图标点击时
const onColClick = (v: unknown | string) => {
	emit('get-icon', v);
};
</script>

<style scoped lang="scss">
.icon-selector-warp-row {
	height: 250px;
	overflow: hidden;
	.el-row {
		padding: 15px;
		margin-bottom: 10px;
	}
	.el-scrollbar__bar.is-horizontal {
		display: none;
	}
	.icon-selector-warp-item {
		display: flex;
		justify-content: center;
		align-items: center;
		border: 1px solid var(--el-border-color);
		border-radius: 8px;
		margin-bottom: 12px;
		height: 45px;
		transition: all 0.3s ease;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
		i {
			font-size: 24px;
			color: var(--el-text-color-regular);
			transition: all 0.3s ease;
		}
		&:hover {
			cursor: pointer;
			background-color: var(--el-color-primary-light-9);
			border: 1px solid var(--el-color-primary);
			transform: translateY(-2px);
			box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
			i {
				color: var(--el-color-primary);
				transform: scale(1.1);
			}
		}
	}
	.icon-selector-active {
		background-color: var(--el-color-primary-light-9);
		border: 2px solid var(--el-color-primary);
		box-shadow: 0 0 0 2px rgba(103, 194, 58, 0.2);
		i {
			color: var(--el-color-primary);
			font-weight: bold;
		}
	}
}
</style>
