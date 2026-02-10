<template>
  <div class="llm-view">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>大语言模型管理</span>
          <el-button type="primary" @click="showCreateDialog = true">
            <el-icon><Plus /></el-icon>添加后端
          </el-button>
        </div>
      </template>

      <el-table :data="backends" v-loading="loading" stripe>
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="adapter" label="适配器" />
        <el-table-column prop="enable" label="状态">
          <template #default="{ row }">
            <el-tag :type="row.enable ? 'success' : 'danger'">
              {{ row.enable ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="模型数量">
          <template #default="{ row }">
            {{ row.models?.length || 0 }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 创建/编辑对话框 -->
    <el-dialog v-model="showCreateDialog" title="添加LLM后端" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="请输入后端名称" />
        </el-form-item>
        <el-form-item label="适配器">
          <el-select v-model="form.adapter" placeholder="选择适配器类型">
            <el-option v-for="type in adapterTypes" :key="type" :label="type" :value="type" />
          </el-select>
        </el-form-item>
        <el-form-item label="API Key">
          <el-input v-model="form.config.api_key" type="password" show-password />
        </el-form-item>
        <el-form-item label="API Base">
          <el-input v-model="form.config.api_base" placeholder="https://api.example.com/v1" />
        </el-form-item>
        <el-form-item label="启用">
          <el-switch v-model="form.enable" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate" :loading="saving">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getBackends, getLLMAdapterTypes, createBackend, deleteBackend } from '@/api'

const loading = ref(false)
const saving = ref(false)
const showCreateDialog = ref(false)
const backends = ref<any[]>([])
const adapterTypes = ref<string[]>([])

const form = ref({
  name: '',
  adapter: '',
  config: {
    api_key: '',
    api_base: ''
  },
  enable: true,
  models: []
})

const loadData = async () => {
  loading.value = true
  try {
    const backendsRes: any = await getBackends()
    const typesRes: any = await getLLMAdapterTypes()
    backends.value = backendsRes.data?.backends || []
    adapterTypes.value = typesRes.types || []
  } catch (error) {
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const handleCreate = async () => {
  saving.value = true
  try {
    await createBackend(form.value)
    ElMessage.success('创建成功')
    showCreateDialog.value = false
    loadData()
  } catch (error) {
    ElMessage.error('创建失败')
  } finally {
    saving.value = false
  }
}

const handleEdit = (_row: any) => {
  ElMessage.info('编辑功能开发中')
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm(`确定要删除后端 "${row.name}" 吗？`, '提示', {
      type: 'warning'
    })
    await deleteBackend(row.name)
    ElMessage.success('删除成功')
    loadData()
  } catch {
    // 取消删除
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>