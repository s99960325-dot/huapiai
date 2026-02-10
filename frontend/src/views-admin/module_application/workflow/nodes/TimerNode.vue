<template>
  <div class="timer-node">
    <div class="node-header">
      <span class="icon">⏰</span>
      <span>{{ data.label }}</span>
    </div>
    <div class="node-body">
      <div class="timer-info">
        <span>延迟: {{ data.delay || "0" }}秒</span>
      </div>
    </div>
    <Handle :id="'top-' + id" type="source" position="top" :style="{ background: '#6366f1' }" />
    <Handle :id="'left-' + id" type="source" position="left" :style="{ background: '#6366f1' }" />
    <Handle :id="'right-' + id" type="source" position="right" :style="{ background: '#6366f1' }" />
    <Handle
      :id="'bottom-' + id"
      type="source"
      position="bottom"
      :style="{ background: '#6366f1' }"
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
.timer-node {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 150px;
  height: 70px;
  color: white;
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  border: 2px solid #4338ca;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
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

.timer-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
</style>
