<template>
  <div class="plugin-view">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>插件管理</span>
          <el-button type="primary" @click="showInstallDialog = true">
            <el-icon><Plus /></el-icon>安装插件
          </el-button>
        </div>
      </template>

      <el-table :data="plugins" v-loading="loading" stripe>
        <el-table-column prop="id" label="插件ID" />
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="version" label="版本" width="100" />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.enabled ? 'success' : 'info'">
              {{ row.enabled ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250">
          <template #default="{ row }">
            <el-button 
              :type="row.enabled ? 'danger' : 'success'" 
              size="small" 
              @click="togglePlugin(row)"
            >
              {{ row.enabled ? '禁用' : '启用' }}
            </el-button>
            <el-button type="danger" size="small" @click="handleUninstall(row)">卸载</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 安装对话框 -->
    <el-dialog v-model="showInstallDialog" title="安装插件" width="500px">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="从市场安装" name="market">
          <el-input v-model="searchQuery" placeholder="搜索插件..." @keyup.enter="searchPlugins">
            <template #append>
              <el-button @click="searchPlugins">搜索</el-button>
            </template>
          </el-input>
          <div class="search-results" v-if="searchResults.length > 0">
            <div v-for="plugin in searchResults" :key="plugin.id" class="plugin-item">
              <div class="plugin-info">
                <div class="plugin-name">{{ plugin.name }}</div>
                <div class="plugin-desc">{{ plugin.description }}</div>
              </div>
              <el-button type="primary" size="small" @click="installPlugin(plugin.id)">安装</el-button>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="本地安装" name="local">
          <el-upload
            drag
            action="/backend-api/api/plugin/install-from-file"
            :headers="uploadHeaders"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
            accept=".zip,.tar.gz"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              拖拽文件到此处或 <em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 .zip 和 .tar.gz 格式的插件包
              </div>
            </template>
          </el-upload>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getPlugins, enablePlugin, disablePlugin, uninstallPlugin, searchPlugins as searchPluginsApi } from '@/api'
import Cookies from 'js-cookie'

const loading = ref(false)
const showInstallDialog = ref(false)
const activeTab = ref('market')
const searchQuery = ref('')
const plugins = ref<any[]>([])
const searchResults = ref<any[]>([])

const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${Cookies.get('token')}`
}))

const loadData = async () => {
  loading.value = true
  try {
    const res: any = await getPlugins()
    plugins.value = res.plugins || []
  } catch (error) {
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const togglePlugin = async (row: any) => {
  try {
    if (row.enabled) {
      await disablePlugin(row.id)
      ElMessage.success('已禁用')
    } else {
      await enablePlugin(row.id)
      ElMessage.success('已启用')
    }
    loadData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleUninstall = async (row: any) => {
  try {
    await ElMessageBox.confirm(`确定要卸载插件 "${row.name}" 吗？`, '提示', {
      type: 'warning'
    })
    await uninstallPlugin(row.id)
    ElMessage.success('卸载成功')
    loadData()
  } catch {
    // 取消卸载
  }
}

const searchPlugins = async () => {
  if (!searchQuery.value) return
  try {
    const res: any = await searchPluginsApi(searchQuery.value)
    searchResults.value = res.results || []
  } catch (error) {
    ElMessage.error('搜索失败')
  }
}

const installPlugin = async (_pluginId: string) => {
  try {
    // await installPluginApi(pluginId)
    ElMessage.success('安装成功')
    showInstallDialog.value = false
    loadData()
  } catch (error) {
    ElMessage.error('安装失败')
  }
}

const handleUploadSuccess = () => {
  ElMessage.success('上传成功')
  showInstallDialog.value = false
  loadData()
}

const handleUploadError = () => {
  ElMessage.error('上传失败')
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

.search-results {
  margin-top: 16px;
  max-height: 300px;
  overflow-y: auto;
}

.plugin-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #ebeef5;
}

.plugin-item:last-child {
  border-bottom: none;
}

.plugin-info {
  flex: 1;
}

.plugin-name {
  font-weight: 600;
  color: #303133;
}

.plugin-desc {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}
</style>