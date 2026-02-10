<template>
  <div class="condition-node">
    <div class="node-content">{{ data.label }}</div>
    <Handle :id="'top-' + id" type="source" position="top" :style="{ background: '#f59e0b' }" />
    <Handle :id="'left-' + id" type="source" position="left" :style="{ background: '#f59e0b' }" />
    <Handle :id="'right-' + id" type="source" position="right" :style="{ background: '#f59e0b' }" />
    <Handle
      :id="'bottom-' + id"
      type="source"
      position="bottom"
      :style="{ background: '#f59e0b' }"
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
.condition-node {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 100px;
  color: white;
  background-color: #f59e0b;
  border-radius: 8px;
  transform: rotate(45deg);
}

.node-content {
  font-size: 12px;
  font-weight: bold;
  text-align: center;
  transform: rotate(-45deg);
}
</style>
