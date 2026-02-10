<template>
  <div class="im-view">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>消息平台管理</span>
          <el-button type="primary" @click="showCreateDialog = true">
            <el-icon><Plus /></el-icon>添加适配器
          </el-button>
        </div>
      </template>

      <el-table :data="adapters" v-loading="loading" stripe>
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="adapter" label="适配器类型" />
        <el-table-column label="运行状态">
          <template #default="{ row }">
            <el-tag :type="row.is_running ? 'success' : 'info'">
              {{ row.is_running ? '运行中' : '已停止' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="300">
          <template #default="{ row }">
            <el-button 
              :type="row.is_running ? 'danger' : 'success'" 
              size="small" 
              @click="toggleAdapter(row)"
            >
              {{ row.is_running ? '停止' : '启动' }}
            </el-button>
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 创建对话框 -->
    <el-dialog v-model="showCreateDialog" title="添加IM适配器" width="600px">
      <el-form :model="form" label-width="120px">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="请输入适配器名称" />
        </el-form-item>
        <el-form-item label="适配器类型">
          <el-select v-model="form.adapter" placeholder="选择适配器类型">
            <el-option v-for="type in adapterTypes" :key="type" :label="type" :value="type" />
          </el-select>
        </el-form-item>
        <el-form-item label="配置">
          <el-input v-model="configJson" type="textarea" :rows="5" placeholder="JSON格式配置" />
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
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAdapters, getIMAdapterTypes, createAdapter, deleteAdapter, startAdapter, stopAdapter } from '@/api'

const loading = ref(false)
const saving = ref(false)
const showCreateDialog = ref(false)
const adapters = ref<any[]>([])
const adapterTypes = ref<string[]>([])

const form = ref({
  name: '',
  adapter: '',
  config: {}
})

const configJson = computed({
  get: () => JSON.stringify(form.value.config, null, 2),
  set: (val) => {
    try {
      form.value.config = JSON.parse(val)
    } catch {}
  }
})

const loadData = async () => {
  loading.value = true
  try {
    const adaptersRes: any = await getAdapters()
    const typesRes: any = await getIMAdapterTypes()
    adapters.value = adaptersRes.adapters || []
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
    await createAdapter(form.value)
    ElMessage.success('创建成功')
    showCreateDialog.value = false
    loadData()
  } catch (error) {
    ElMessage.error('创建失败')
  } finally {
    saving.value = false
  }
}

const toggleAdapter = async (row: any) => {
  try {
    if (row.is_running) {
      await stopAdapter(row.name)
      ElMessage.success('已停止')
    } else {
      await startAdapter(row.name)
      ElMessage.success('已启动')
    }
    loadData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleEdit = (_row: any) => {
  ElMessage.info('编辑功能开发中')
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm(`确定要删除适配器 "${row.name}" 吗？`, '提示', {
      type: 'warning'
    })
    await deleteAdapter(row.name)
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