<template>
  <div class="workflow-view">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>工作流管理</span>
          <el-button type="primary" @click="showCreateDialog = true">
            <el-icon><Plus /></el-icon>创建工作流
          </el-button>
        </div>
      </template>

      <el-table :data="workflows" v-loading="loading" stripe>
        <el-table-column prop="group_id" label="分组" width="120" />
        <el-table-column prop="workflow_id" label="ID" width="150" />
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column prop="block_count" label="Block数量" width="100" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 创建对话框 -->
    <el-dialog v-model="showCreateDialog" title="创建工作流" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="分组">
          <el-input v-model="form.group_id" placeholder="例如: chat" />
        </el-form-item>
        <el-form-item label="ID">
          <el-input v-model="form.workflow_id" placeholder="例如: normal" />
        </el-form-item>
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="工作流名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
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
import { getWorkflows, createWorkflow, deleteWorkflow } from '@/api'

const loading = ref(false)
const saving = ref(false)
const showCreateDialog = ref(false)
const workflows = ref<any[]>([])

const form = ref({
  group_id: '',
  workflow_id: '',
  name: '',
  description: ''
})

const loadData = async () => {
  loading.value = true
  try {
    const res: any = await getWorkflows()
    workflows.value = res.workflows || []
  } catch (error) {
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const handleCreate = async () => {
  saving.value = true
  try {
    await createWorkflow(form.value)
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
    await ElMessageBox.confirm(`确定要删除工作流 "${row.name}" 吗？`, '提示', {
      type: 'warning'
    })
    await deleteWorkflow(row.group_id, row.workflow_id)
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