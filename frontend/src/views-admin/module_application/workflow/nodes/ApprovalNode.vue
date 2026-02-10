<template>
  <div class="approval-node">
    <div class="node-header">
      <span class="icon">✓</span>
      <span>{{ data.label }}</span>
    </div>
    <div class="node-body">
      <div class="approval-info">
        <span>审批人: {{ data.approver || "待指定" }}</span>
        <span>类型: {{ data.approvalType || "单人审批" }}</span>
      </div>
    </div>
    <Handle :id="'top-' + id" type="source" position="top" :style="{ background: '#10b981' }" />
    <Handle :id="'left-' + id" type="source" position="left" :style="{ background: '#10b981' }" />
    <Handle :id="'right-' + id" type="source" position="right" :style="{ background: '#10b981' }" />
    <Handle
      :id="'bottom-' + id"
      type="source"
      position="bottom"
      :style="{ background: '#10b981' }"
    />
  </div>
</template>

<script setup>
import { Handle } from "@vue-flow/core";

defineProps({
  id: String,
  data: Object,
});
</script>

<style scoped>
.approval-node {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 150px;
  height: 70px;
  color: white;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: 2px solid #047857;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.node-header {
  display: flex;
  gap: 5px;
  align-items: center;
  margin-bottom: 5px;
  font-size: 14px;
  font-weight: bold;
}

.icon {
  font-size: 16px;
}

.node-body {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.9);
}

.approval-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
</style>
