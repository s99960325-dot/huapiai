<template>
  <div class="parallel-node">
    <div class="node-header">{{ data.label }}</div>
    <div class="node-body">
      <div class="branch-label">并行分支</div>
    </div>
    <Handle :id="'top-' + id" type="source" position="top" :style="{ background: '#8b5cf6' }" />
    <Handle :id="'left-' + id" type="source" position="left" :style="{ background: '#8b5cf6' }" />
    <Handle :id="'right-' + id" type="source" position="right" :style="{ background: '#8b5cf6' }" />
    <Handle
      :id="'bottom-' + id"
      type="source"
      position="bottom"
      :style="{ background: '#8b5cf6' }"
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
.parallel-node {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 140px;
  height: 80px;
  color: white;
  background-color: #8b5cf6;
  border: 2px solid #7c3aed;
  border-radius: 8px;
}

.node-header {
  margin-bottom: 5px;
  font-size: 14px;
  font-weight: bold;
}

.node-body {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.9);
}

.branch-label {
  display: flex;
  gap: 5px;
  align-items: center;
}
</style>
