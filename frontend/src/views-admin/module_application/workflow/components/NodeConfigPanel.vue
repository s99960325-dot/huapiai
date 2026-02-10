<template>
  <div class="node-config-panel">
    <div class="panel-header">
      <span>节点配置</span>
      <ElButton type="text" class="close-btn" @click="handleClose">
        <ElIcon><Close /></ElIcon>
      </ElButton>
    </div>

    <div class="panel-content">
      <ElForm :model="formData" label-width="80px" size="small">
        <ElFormItem label="节点名称">
          <ElInput v-model="formData.label" placeholder="请输入节点名称" />
        </ElFormItem>

        <ElFormItem v-if="nodeType === 'task'" label="执行人">
          <ElSelect v-model="formData.assignee" placeholder="请选择执行人">
            <ElOption label="张三" value="zhangsan" />
            <ElOption label="李四" value="lisi" />
            <ElOption label="王五" value="wangwu" />
          </ElSelect>
        </ElFormItem>

        <ElFormItem v-if="nodeType === 'task'" label="优先级">
          <ElSelect v-model="formData.priority" placeholder="请选择优先级">
            <ElOption label="高" value="high" />
            <ElOption label="中" value="medium" />
            <ElOption label="低" value="low" />
          </ElSelect>
        </ElFormItem>

        <ElFormItem v-if="nodeType === 'approval'" label="审批人">
          <ElSelect v-model="formData.approver" placeholder="请选择审批人">
            <ElOption label="经理A" value="manager1" />
            <ElOption label="经理B" value="manager2" />
            <ElOption label="总监" value="director" />
          </ElSelect>
        </ElFormItem>

        <ElFormItem v-if="nodeType === 'approval'" label="审批类型">
          <ElSelect v-model="formData.approvalType" placeholder="请选择审批类型">
            <ElOption label="单人审批" value="single" />
            <ElOption label="会签" value="all" />
            <ElOption label="或签" value="any" />
          </ElSelect>
        </ElFormItem>

        <ElFormItem v-if="nodeType === 'notification'" label="通知类型">
          <ElSelect v-model="formData.notifyType" placeholder="请选择通知类型">
            <ElOption label="邮件" value="email" />
            <ElOption label="短信" value="sms" />
            <ElOption label="站内信" value="message" />
          </ElSelect>
        </ElFormItem>

        <ElFormItem v-if="nodeType === 'notification'" label="接收人">
          <ElInput v-model="formData.recipients" placeholder="请输入接收人" />
        </ElFormItem>

        <ElFormItem v-if="nodeType === 'timer'" label="延迟时间">
          <ElInputNumber v-model="formData.delay" :min="0" :max="3600" />
          <span style="margin-left: 8px">秒</span>
        </ElFormItem>

        <ElFormItem v-if="nodeType === 'condition'" label="条件表达式">
          <ElInput
            v-model="formData.condition"
            type="textarea"
            :rows="3"
            placeholder="请输入条件表达式"
          />
        </ElFormItem>

        <ElFormItem v-if="nodeType === 'parallel'" label="分支数量">
          <ElInputNumber v-model="formData.branchCount" :min="2" :max="10" />
        </ElFormItem>

        <ElFormItem label="描述">
          <ElInput
            v-model="formData.description"
            type="textarea"
            :rows="2"
            placeholder="请输入描述信息"
          />
        </ElFormItem>
      </ElForm>

      <div class="panel-actions">
        <ElButton type="primary" size="small" @click="handleSave">保存</ElButton>
        <ElButton type="danger" size="small" @click="handleDelete">删除节点</ElButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import {
  ElButton,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElInputNumber,
  ElMessage,
  ElIcon,
} from "element-plus";
import { Close } from "@element-plus/icons-vue";

const props = defineProps({
  node: {
    type: Object,
    default: () => ({}),
  },
});

const emit = defineEmits(["close", "save", "delete"]);

const nodeType = ref(props.node?.type || "custom");
const formData = ref({
  label: props.node?.data?.label || "",
  assignee: props.node?.data?.assignee || "",
  priority: props.node?.data?.priority || "medium",
  approver: props.node?.data?.approver || "",
  approvalType: props.node?.data?.approvalType || "single",
  notifyType: props.node?.data?.notifyType || "email",
  recipients: props.node?.data?.recipients || "",
  delay: props.node?.data?.delay || 0,
  condition: props.node?.data?.condition || "",
  branchCount: props.node?.data?.branchCount || 2,
  description: props.node?.data?.description || "",
});

watch(
  () => props.node,
  (newNode) => {
    if (newNode) {
      nodeType.value = newNode.type || "custom";
      formData.value = {
        label: newNode.data?.label || "",
        assignee: newNode.data?.assignee || "",
        priority: newNode.data?.priority || "medium",
        approver: newNode.data?.approver || "",
        approvalType: newNode.data?.approvalType || "single",
        notifyType: newNode.data?.notifyType || "email",
        recipients: newNode.data?.recipients || "",
        delay: newNode.data?.delay || 0,
        condition: newNode.data?.condition || "",
        branchCount: newNode.data?.branchCount || 2,
        description: newNode.data?.description || "",
      };
    }
  },
  { deep: true }
);

function handleClose() {
  emit("close");
}

function handleSave() {
  emit("save", formData.value);
  ElMessage.success("保存成功");
}

function handleDelete() {
  emit("delete");
}
</script>

<style scoped>
.node-config-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  font-weight: 600;
  border-bottom: 1px solid #e5e7eb;
}

.close-btn {
  padding: 4px;
}

.panel-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.panel-actions {
  display: flex;
  gap: 8px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.panel-actions .el-button {
  flex: 1;
}
</style>
