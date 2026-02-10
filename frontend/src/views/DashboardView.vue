<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6" v-for="stat in stats" :key="stat.title">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" :style="{ backgroundColor: stat.color }">
              <el-icon size="32" color="#fff">
                <component :is="stat.icon" />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-title">{{ stat.title }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>系统状态</span>
            </div>
          </template>
          <div v-if="systemStatus" class="status-list">
            <div class="status-item">
              <span class="label">运行时间</span>
              <span class="value">{{ formatUptime(systemStatus.uptime) }}</span>
            </div>
            <div class="status-item">
              <span class="label">CPU 使用率</span>
              <el-progress :percentage="systemStatus.cpu_usage" />
            </div>
            <div class="status-item">
              <span class="label">内存使用</span>
              <el-progress :percentage="systemStatus.memory_usage" />
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>版本信息</span>
            </div>
          </template>
          <div v-if="versionInfo" class="version-info">
            <div class="version-item">
              <span class="label">当前版本</span>
              <el-tag>{{ versionInfo.current_version }}</el-tag>
            </div>
            <div class="version-item">
              <span class="label">最新版本</span>
              <el-tag :type="versionInfo.has_update ? 'warning' : 'success'">
                {{ versionInfo.latest_version }}
              </el-tag>
            </div>
            <div v-if="versionInfo.has_update" class="update-tip">
              <el-alert
                title="发现新版本"
                type="warning"
                :closable="false"
                show-icon
              />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getSystemStatus, getVersion } from '@/api'

const stats = ref([
  { title: 'LLM 后端', value: 0, icon: 'ChatDotRound', color: '#409EFF' },
  { title: 'IM 适配器', value: 0, icon: 'Message', color: '#67C23A' },
  { title: '工作流', value: 0, icon: 'Connection', color: '#E6A23C' },
  { title: '插件', value: 0, icon: 'Box', color: '#F56C6C' }
])

const systemStatus = ref<any>(null)
const versionInfo = ref<any>(null)

const formatUptime = (seconds: number) => {
  const days = Math.floor(seconds / 86400)
  const hours = Math.floor((seconds % 86400) / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  return `${days}天 ${hours}小时 ${minutes}分钟`
}

const loadData = async () => {
  try {
    const statusRes: any = await getSystemStatus()
    const versionRes: any = await getVersion()
    systemStatus.value = statusRes
    versionInfo.value = versionRes
    
    // 更新统计数据
    stats.value[0].value = statusRes.llm_backends || 0
    stats.value[1].value = statusRes.im_adapters || 0
    stats.value[2].value = statusRes.workflows || 0
    stats.value[3].value = statusRes.plugins || 0
  } catch (error) {
    ElMessage.error('加载数据失败')
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.stat-card {
  margin-bottom: 20px;
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.stat-title {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.card-header {
  font-weight: 600;
}

.status-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.status-item .label {
  width: 100px;
  color: #606266;
}

.status-item .value {
  flex: 1;
  color: #303133;
}

.version-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.version-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.version-item .label {
  color: #606266;
}

.update-tip {
  margin-top: 8px;
}
</style>