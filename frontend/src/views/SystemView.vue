<template>
  <div class="system-view">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>系统配置</span>
              <el-button type="primary" @click="saveConfig" :loading="saving">保存</el-button>
            </div>
          </template>
          <el-form :model="config" label-width="150px">
            <el-divider>Web服务</el-divider>
            <el-form-item label="监听地址">
              <el-input v-model="config.web.host" />
            </el-form-item>
            <el-form-item label="端口">
              <el-input-number v-model="config.web.port" :min="1" :max="65535" />
            </el-form-item>
            
            <el-divider>系统设置</el-divider>
            <el-form-item label="时区">
              <el-input v-model="config.system.timezone" />
            </el-form-item>
            
            <el-divider>更新配置</el-divider>
            <el-form-item label="PyPI镜像">
              <el-input v-model="config.update.pypi_registry" />
            </el-form-item>
            <el-form-item label="NPM镜像">
              <el-input v-model="config.update.npm_registry" />
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>系统操作</span>
            </div>
          </template>
          <div class="action-list">
            <div class="action-item">
              <div class="action-info">
                <div class="action-title">检查更新</div>
                <div class="action-desc">检查系统是否有新版本可用</div>
              </div>
              <el-button type="primary" @click="checkUpdate" :loading="checking">检查</el-button>
            </div>
            
            <el-divider />
            
            <div class="action-item">
              <div class="action-info">
                <div class="action-title">重启系统</div>
                <div class="action-desc">重启整个应用程序</div>
              </div>
              <el-button type="warning" @click="restartSystem" :loading="restarting">重启</el-button>
            </div>
            
            <el-divider />
            
            <div class="action-item">
              <div class="action-info">
                <div class="action-title">查看日志</div>
                <div class="action-desc">实时查看系统运行日志</div>
              </div>
              <el-button @click="showLogs = true">查看</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 日志对话框 -->
    <el-dialog v-model="showLogs" title="系统日志" width="800px" fullscreen>
      <div class="log-container">
        <pre class="logs">{{ logs }}</pre>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getSystemConfig, updateSystemConfig, checkUpdate as checkUpdateApi, restartSystem as restartSystemApi, getLogs } from '@/api'

const loading = ref(false)
const saving = ref(false)
const checking = ref(false)
const restarting = ref(false)
const showLogs = ref(false)
const logs = ref('')

const config = ref<any>({
  web: { host: '127.0.0.1', port: 8080 },
  system: { timezone: 'Asia/Shanghai' },
  update: { pypi_registry: '', npm_registry: '' }
})

const loadConfig = async () => {
  loading.value = true
  try {
    const res: any = await getSystemConfig()
    config.value = res
  } catch (error) {
    ElMessage.error('加载配置失败')
  } finally {
    loading.value = false
  }
}

const saveConfig = async () => {
  saving.value = true
  try {
    await updateSystemConfig(config.value)
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const checkUpdate = async () => {
  checking.value = true
  try {
    const res: any = await checkUpdateApi()
    if (res.has_update) {
      ElMessage.warning(`发现新版本: ${res.latest_version}`)
    } else {
      ElMessage.success('当前已是最新版本')
    }
  } catch (error) {
    ElMessage.error('检查失败')
  } finally {
    checking.value = false
  }
}

const restartSystem = async () => {
  try {
    await ElMessageBox.confirm('确定要重启系统吗？', '提示', {
      type: 'warning'
    })
    restarting.value = true
    await restartSystemApi()
    ElMessage.success('系统正在重启...')
  } catch {
    // 取消重启
  } finally {
    restarting.value = false
  }
}

const loadLogs = async () => {
  try {
    const res: any = await getLogs()
    logs.value = res.logs || '暂无日志'
  } catch (error) {
    logs.value = '加载日志失败'
  }
}

onMounted(() => {
  loadConfig()
  loadLogs()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.action-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-info {
  flex: 1;
}

.action-title {
  font-weight: 600;
  color: #303133;
}

.action-desc {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.log-container {
  background-color: #1e1e1e;
  color: #d4d4d4;
  padding: 16px;
  border-radius: 4px;
  max-height: 600px;
  overflow-y: auto;
}

.logs {
  margin: 0;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>