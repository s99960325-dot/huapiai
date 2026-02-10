<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          AI 服务管理
        </div>
      </template>

      <div class="data-table__toolbar mb-4">
        <el-button type="primary" icon="refresh" @click="fetch">刷新</el-button>
      </div>

      <el-table :data="providers" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="180" />
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="status" label="状态" width="120" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useAIStoreHook } from "@/store/modules/ai.store";

const aiStore = useAIStoreHook();

const providers = computed(() => aiStore.providers);
const loading = computed(() => aiStore.loading);

function fetch() {
  aiStore.fetchProviders();
}

onMounted(() => {
  fetch();
});
</script>

<style scoped>
.card-header {
  font-weight: 600;
}
</style>
