<template>
  <div class="app-container" @keydown="handleKeyDown">
    <div class="top-toolbar">
      <div class="toolbar-left">
        <el-form inline>
          <el-form-item>
            <ElButton type="primary" @click="handleSave">保存流程</ElButton>
          </el-form-item>
          <el-form-item>
            <ElButton @click="handleLoad">加载流程</ElButton>
          </el-form-item>
          <el-form-item>
            <ElButton @click="handleImport">导入JSON</ElButton>
          </el-form-item>
          <el-form-item>
            <ElButton @click="handleExport">导出JSON</ElButton>
          </el-form-item>
          <el-form-item>
            <ElDropdown trigger="click" @command="handleTemplateSelect">
              <ElButton>
                流程模板
                <ElIcon class="el-icon--right"><ArrowDown /></ElIcon>
              </ElButton>
              <template #dropdown>
                <ElDropdownMenu>
                  <ElDropdownItem
                    v-for="template in templates"
                    :key="template.id"
                    :command="template.id"
                  >
                    {{ template.name }}
                  </ElDropdownItem>
                </ElDropdownMenu>
              </template>
            </ElDropdown>
          </el-form-item>
          <el-form-item>
            <ElButton @click="handleValidate">验证流程</ElButton>
          </el-form-item>
          <el-form-item>
            <ElButton @click="handleClear">清空画布</ElButton>
          </el-form-item>
        </el-form>
      </div>
      <div class="toolbar-right">
        <el-form inline>
          <el-form-item>
            <ElButton @click="toggleGrid">{{ showGrid ? "隐藏网格" : "显示网格" }}</ElButton>
          </el-form-item>
          <el-form-item>
            <ElButton @click="handleZoomIn">放大</ElButton>
          </el-form-item>
          <el-form-item>
            <ElButton @click="handleZoomOut">缩小</ElButton>
          </el-form-item>
          <el-form-item>
            <ElButton @click="handleFitView">适应视图</ElButton>
          </el-form-item>
          <el-form-item>
            <div class="zoom-level">缩放: {{ Math.round(zoomLevel * 100) }}%</div>
          </el-form-item>
        </el-form>
      </div>
    </div>

    <div class="main-layout">
      <div class="left-panel">
        <div class="panel-section">
          <div class="section-title">基础节点</div>
          <div class="flex-center">
            <div
              class="drag-item text-center start-item"
              draggable="true"
              @dragstart="onDragStart($event, '开始')"
              @dragend="onDragEnd"
            >
              <span>开始</span>
            </div>
            <div
              class="drag-item text-center end-item ml-2"
              draggable="true"
              @dragstart="onDragStart($event, '结束')"
              @dragend="onDragEnd"
            >
              <span>结束</span>
            </div>
          </div>
        </div>

        <div class="panel-section">
          <div class="section-title">流程节点</div>
          <div
            v-for="item in processNodes"
            :key="item.type"
            class="drag-item text-center w-full mt-2"
            :class="item.class"
            draggable="true"
            @dragstart="onDragStart($event, item)"
            @dragend="onDragEnd"
          >
            <span>{{ item.label }}</span>
          </div>
        </div>

        <div class="panel-section">
          <div class="section-title">自定义节点</div>
          <div
            v-for="(item, index) in customNodes"
            :key="index"
            class="drag-item text-center w-full mt-2"
            draggable="true"
            @dragstart="onDragStart($event, item)"
            @dragend="onDragEnd"
          >
            <span>{{ item.name }}</span>
          </div>
        </div>

        <div class="panel-section">
          <div class="section-title">流程统计</div>
          <div class="stats-list">
            <div class="stat-item">
              <span class="stat-label">总节点数:</span>
              <span class="stat-value">{{ stats.totalNodes }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">任务节点:</span>
              <span class="stat-value">{{ stats.taskNodes }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">审批节点:</span>
              <span class="stat-value">{{ stats.approvalNodes }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">条件节点:</span>
              <span class="stat-value">{{ stats.conditionNodes }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">连线数:</span>
              <span class="stat-value">{{ stats.totalEdges }}</span>
            </div>
          </div>
        </div>

        <div class="panel-section">
          <div class="section-title">快捷键说明</div>
          <div class="shortcut-list">
            <div class="shortcut-item">
              <span class="key">Delete</span>
              <span>删除选中</span>
            </div>
            <div class="shortcut-item">
              <span class="key">Ctrl+C</span>
              <span>复制节点</span>
            </div>
            <div class="shortcut-item">
              <span class="key">Ctrl+V</span>
              <span>粘贴节点</span>
            </div>
            <div class="shortcut-item">
              <span class="key">Ctrl+Z</span>
              <span>撤销</span>
            </div>
            <div class="shortcut-item">
              <span class="key">Ctrl+Y</span>
              <span>重做</span>
            </div>
            <div class="shortcut-item">
              <span class="key">Ctrl+S</span>
              <span>保存流程</span>
            </div>
          </div>
        </div>
      </div>

      <div class="canvas-container">
        <VueFlow
          :nodes="nodes"
          :edges="edges"
          class="basic-flow"
          :default-viewport="{ zoom: 1 }"
          :min-zoom="0.2"
          :max-zoom="4"
          :node-types="nodeTypes"
          :default-edge-options="defaultEdgeOptions"
          :connect-on-click="true"
          @node-click="onNodeClick"
          @edge-click="onEdgeClick"
          @drop="onDrop"
          @dragover="onDragOver"
          @move="handleMove"
        >
          <Controls />
          <Background v-if="showGrid" pattern-color="#aaa" :gap="16" />
          <MiniMap />
        </VueFlow>
      </div>

      <div v-if="updateState" class="right-panel">
        <NodeConfigPanel
          v-if="updateState === 'node'"
          :node="selectedNode"
          @close="handleClosePanel"
          @save="handleSaveNode"
          @delete="handleDeleteNode"
        />
        <EdgeConfigPanel
          v-if="updateState === 'edge'"
          :edge="selectedEdge"
          @close="handleClosePanel"
          @save="handleSaveEdge"
          @delete="handleDeleteEdge"
        />
      </div>
    </div>

    <input
      ref="fileInput"
      type="file"
      accept=".json"
      style="display: none"
      @change="handleFileChange"
    />
  </div>
</template>

<script setup>
defineOptions({
  name: "Workflow",
  inheritAttrs: false,
});

import { VueFlow, useVueFlow } from "@vue-flow/core";
import { Background } from "@vue-flow/background";
import { Controls } from "@vue-flow/controls";
import { MiniMap } from "@vue-flow/minimap";
import "@vue-flow/core/dist/style.css";
import "@vue-flow/core/dist/theme-default.css";
import "@vue-flow/controls/dist/style.css";
import { ArrowDown } from "@element-plus/icons-vue";
import "element-plus/dist/index.css";

import ConditionNode from "./nodes/ConditionNode.vue";
import ParallelNode from "./nodes/ParallelNode.vue";
import TaskNode from "./nodes/TaskNode.vue";
import ApprovalNode from "./nodes/ApprovalNode.vue";
import NotificationNode from "./nodes/NotificationNode.vue";
import TimerNode from "./nodes/TimerNode.vue";
import NodeConfigPanel from "./components/NodeConfigPanel.vue";
import EdgeConfigPanel from "./components/EdgeConfigPanel.vue";

const {
  onInit,
  onNodeDragStop,
  onConnect,
  addEdges,
  getNodes,
  getEdges,
  setEdges,
  setNodes,
  screenToFlowCoordinate,
  onNodesInitialized,
  updateNode,
  addNodes,
  fitView,
  zoomIn,
  zoomOut,
  onMove,
} = useVueFlow();

const defaultEdgeOptions = {
  type: "smoothstep",
  animated: true,
  markerEnd: {
    type: "arrowclosed",
    color: "black",
  },
};

const nodes = ref([
  {
    id: "start",
    type: "input",
    data: { label: "开始" },
    position: { x: 400, y: 50 },
    class: "round-start",
  },
  {
    id: "task1",
    type: "task",
    data: { label: "提交申请", assignee: "张三", priority: "high" },
    position: { x: 350, y: 150 },
  },
  {
    id: "approval1",
    type: "approval",
    data: { label: "经理审批", approver: "经理A", approvalType: "single" },
    position: { x: 350, y: 250 },
  },
  {
    id: "condition1",
    type: "condition",
    data: { label: "金额判断", condition: "amount > 10000" },
    position: { x: 350, y: 370 },
  },
  {
    id: "task2",
    type: "task",
    data: { label: "总监审批", assignee: "李四", priority: "high" },
    position: { x: 200, y: 500 },
  },
  {
    id: "notification1",
    type: "notification",
    data: { label: "发送通知", notifyType: "email", recipients: "user@example.com" },
    position: { x: 500, y: 500 },
  },
  {
    id: "timer1",
    type: "timer",
    data: { label: "延迟处理", delay: 30 },
    position: { x: 350, y: 620 },
  },
  {
    id: "end",
    type: "output",
    data: { label: "结束" },
    position: { x: 400, y: 750 },
    class: "round-stop",
  },
]);

const nodeTypes = ref({
  condition: markRaw(ConditionNode),
  parallel: markRaw(ParallelNode),
  task: markRaw(TaskNode),
  approval: markRaw(ApprovalNode),
  notification: markRaw(NotificationNode),
  timer: markRaw(TimerNode),
});

const edges = ref([
  {
    id: "e-start-task1",
    type: "smoothstep",
    source: "start",
    target: "task1",
    label: "开始",
  },
  {
    id: "e-task1-approval1",
    type: "smoothstep",
    source: "task1",
    target: "approval1",
    label: "提交",
  },
  {
    id: "e-approval1-condition1",
    type: "smoothstep",
    source: "approval1",
    target: "condition1",
    label: "通过",
  },
  {
    id: "e-condition1-task2",
    type: "smoothstep",
    source: "condition1",
    target: "task2",
    label: "大额",
  },
  {
    id: "e-condition1-notification1",
    type: "smoothstep",
    source: "condition1",
    target: "notification1",
    label: "小额",
  },
  {
    id: "e-task2-timer1",
    type: "smoothstep",
    source: "task2",
    target: "timer1",
    label: "完成",
  },
  {
    id: "e-notification1-timer1",
    type: "smoothstep",
    source: "notification1",
    target: "timer1",
    label: "已发送",
  },
  {
    id: "e-timer1-end",
    type: "smoothstep",
    source: "timer1",
    target: "end",
    label: "结束",
  },
]);

const processNodes = [
  { type: "task", label: "任务节点", class: "task-drag-item" },
  { type: "approval", label: "审批节点", class: "approval-drag-item" },
  { type: "condition", label: "条件节点", class: "condition-drag-item" },
  { type: "parallel", label: "并行节点", class: "parallel-drag-item" },
  { type: "notification", label: "通知节点", class: "notification-drag-item" },
  { type: "timer", label: "定时节点", class: "timer-drag-item" },
];

const customNodes = ref([{ name: "测试1" }, { name: "测试2" }, { name: "测试3" }]);

const updateState = ref("");
const selectedEdge = ref({});
const selectedNode = ref({});
const showGrid = ref(true);
const zoomLevel = ref(1);
const fileInput = ref(null);

const history = ref([]);
const historyIndex = ref(-1);
const maxHistory = 50;

const clipboard = ref(null);

const stats = computed(() => {
  const allNodes = nodes.value;
  return {
    totalNodes: allNodes.length,
    taskNodes: allNodes.filter((n) => n.type === "task").length,
    approvalNodes: allNodes.filter((n) => n.type === "approval").length,
    conditionNodes: allNodes.filter((n) => n.type === "condition").length,
    totalEdges: edges.value.length,
  };
});

const templates = [
  {
    id: "approval",
    name: "审批流程",
    nodes: [
      {
        id: "start",
        type: "input",
        data: { label: "开始" },
        position: { x: 400, y: 50 },
        class: "round-start",
      },
      {
        id: "task1",
        type: "task",
        data: { label: "提交申请", assignee: "申请人", priority: "medium" },
        position: { x: 350, y: 150 },
      },
      {
        id: "approval1",
        type: "approval",
        data: { label: "部门审批", approver: "部门经理", approvalType: "single" },
        position: { x: 350, y: 250 },
      },
      {
        id: "end",
        type: "output",
        data: { label: "结束" },
        position: { x: 400, y: 350 },
        class: "round-stop",
      },
    ],
    edges: [
      { id: "e-start-task1", type: "smoothstep", source: "start", target: "task1", label: "开始" },
      {
        id: "e-task1-approval1",
        type: "smoothstep",
        source: "task1",
        target: "approval1",
        label: "提交",
      },
      {
        id: "e-approval1-end",
        type: "smoothstep",
        source: "approval1",
        target: "end",
        label: "通过",
      },
    ],
  },
  {
    id: "parallel",
    name: "并行处理",
    nodes: [
      {
        id: "start",
        type: "input",
        data: { label: "开始" },
        position: { x: 400, y: 50 },
        class: "round-start",
      },
      {
        id: "parallel1",
        type: "parallel",
        data: { label: "并行分支", branchCount: 3 },
        position: { x: 350, y: 150 },
      },
      {
        id: "task1",
        type: "task",
        data: { label: "任务A", assignee: "张三", priority: "high" },
        position: { x: 200, y: 280 },
      },
      {
        id: "task2",
        type: "task",
        data: { label: "任务B", assignee: "李四", priority: "high" },
        position: { x: 350, y: 280 },
      },
      {
        id: "task3",
        type: "task",
        data: { label: "任务C", assignee: "王五", priority: "high" },
        position: { x: 500, y: 280 },
      },
      {
        id: "end",
        type: "output",
        data: { label: "结束" },
        position: { x: 400, y: 400 },
        class: "round-stop",
      },
    ],
    edges: [
      {
        id: "e-start-parallel1",
        type: "smoothstep",
        source: "start",
        target: "parallel1",
        label: "开始",
      },
      {
        id: "e-parallel1-task1",
        type: "smoothstep",
        source: "parallel1",
        target: "task1",
        label: "分支1",
      },
      {
        id: "e-parallel1-task2",
        type: "smoothstep",
        source: "parallel1",
        target: "task2",
        label: "分支2",
      },
      {
        id: "e-parallel1-task3",
        type: "smoothstep",
        source: "parallel1",
        target: "task3",
        label: "分支3",
      },
      { id: "e-task1-end", type: "smoothstep", source: "task1", target: "end", label: "完成" },
      { id: "e-task2-end", type: "smoothstep", source: "task2", target: "end", label: "完成" },
      { id: "e-task3-end", type: "smoothstep", source: "task3", target: "end", label: "完成" },
    ],
  },
  {
    id: "notification",
    name: "通知流程",
    nodes: [
      {
        id: "start",
        type: "input",
        data: { label: "开始" },
        position: { x: 400, y: 50 },
        class: "round-start",
      },
      {
        id: "task1",
        type: "task",
        data: { label: "处理任务", assignee: "处理人", priority: "high" },
        position: { x: 350, y: 150 },
      },
      {
        id: "notification1",
        type: "notification",
        data: { label: "发送邮件", notifyType: "email", recipients: "user@example.com" },
        position: { x: 350, y: 250 },
      },
      {
        id: "timer1",
        type: "timer",
        data: { label: "延迟5秒", delay: 5 },
        position: { x: 350, y: 350 },
      },
      {
        id: "end",
        type: "output",
        data: { label: "结束" },
        position: { x: 400, y: 450 },
        class: "round-stop",
      },
    ],
    edges: [
      { id: "e-start-task1", type: "smoothstep", source: "start", target: "task1", label: "开始" },
      {
        id: "e-task1-notification1",
        type: "smoothstep",
        source: "task1",
        target: "notification1",
        label: "完成",
      },
      {
        id: "e-notification1-timer1",
        type: "smoothstep",
        source: "notification1",
        target: "timer1",
        label: "已发送",
      },
      { id: "e-timer1-end", type: "smoothstep", source: "timer1", target: "end", label: "结束" },
    ],
  },
];

onInit((vueFlowInstance) => {
  vueFlowInstance.fitView();
  saveToHistory();
});

onNodeDragStop(({ event, nodes, node }) => {
  console.log("Node Drag Stop", { event, nodes, node });
  saveToHistory();
});

onConnect((connection) => {
  addEdges(connection);
  saveToHistory();
});

onMove(({ zoom }) => {
  zoomLevel.value = zoom;
});

function saveToHistory() {
  const state = {
    nodes: JSON.parse(JSON.stringify(nodes.value)),
    edges: JSON.parse(JSON.stringify(edges.value)),
  };

  if (historyIndex.value < history.value.length - 1) {
    history.value = history.value.slice(0, historyIndex.value + 1);
  }

  history.value.push(state);

  if (history.value.length > maxHistory) {
    history.value.shift();
  } else {
    historyIndex.value++;
  }
}

function undo() {
  if (historyIndex.value > 0) {
    historyIndex.value--;
    const state = history.value[historyIndex.value];
    nodes.value = JSON.parse(JSON.stringify(state.nodes));
    edges.value = JSON.parse(JSON.stringify(state.edges));
    ElMessage.success("撤销成功");
  } else {
    ElMessage.warning("没有可撤销的操作");
  }
}

function redo() {
  if (historyIndex.value < history.value.length - 1) {
    historyIndex.value++;
    const state = history.value[historyIndex.value];
    nodes.value = JSON.parse(JSON.stringify(state.nodes));
    edges.value = JSON.parse(JSON.stringify(state.edges));
    ElMessage.success("重做成功");
  } else {
    ElMessage.warning("没有可重做的操作");
  }
}

function handleKeyDown(event) {
  if (event.ctrlKey || event.metaKey) {
    switch (event.key.toLowerCase()) {
      case "s":
        event.preventDefault();
        handleSave();
        break;
      case "c":
        if (selectedNode.value.id) {
          event.preventDefault();
          handleCopy();
        }
        break;
      case "v":
        if (clipboard.value) {
          event.preventDefault();
          handlePaste();
        }
        break;
      case "z":
        event.preventDefault();
        if (event.shiftKey) {
          redo();
        } else {
          undo();
        }
        break;
      case "y":
        event.preventDefault();
        redo();
        break;
    }
  } else if (event.key === "Delete" || event.key === "Backspace") {
    if (selectedNode.value.id && updateState.value === "node") {
      event.preventDefault();
      handleDeleteNode();
    } else if (selectedEdge.value.id && updateState.value === "edge") {
      event.preventDefault();
      handleDeleteEdge();
    }
  }
}

function handleCopy() {
  if (selectedNode.value.id) {
    clipboard.value = JSON.parse(JSON.stringify(selectedNode.value));
    ElMessage.success("节点已复制");
  }
}

function handlePaste() {
  if (clipboard.value) {
    const newNode = {
      ...clipboard.value,
      id: `node-${Date.now()}`,
      position: {
        x: clipboard.value.position.x + 50,
        y: clipboard.value.position.y + 50,
      },
    };
    addNodes(newNode);
    selectedNode.value = newNode;
    updateState.value = "node";
    saveToHistory();
    ElMessage.success("节点已粘贴");
  }
}

function handleExport() {
  const workflowData = {
    nodes: nodes.value,
    edges: edges.value,
    metadata: {
      version: "1.0.0",
      createdAt: new Date().toISOString(),
      exportedAt: new Date().toISOString(),
    },
  };

  const dataStr = JSON.stringify(workflowData, null, 2);
  const dataBlob = new Blob([dataStr], { type: "application/json" });
  const url = URL.createObjectURL(dataBlob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `workflow-${Date.now()}.json`;
  link.click();
  URL.revokeObjectURL(url);
  ElMessage.success("流程导出成功");
}

function handleImport() {
  fileInput.value.click();
}

function handleFileChange(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result);
        if (data.nodes && data.edges) {
          nodes.value = data.nodes;
          edges.value = data.edges;
          saveToHistory();
          ElMessage.success("流程导入成功");
        } else {
          ElMessage.error("无效的流程文件格式");
        }
      } catch {
        ElMessage.error("文件解析失败");
      }
    };
    reader.readAsText(file);
  }
  event.target.value = "";
}

function handleTemplateSelect(templateId) {
  const template = templates.find((t) => t.id === templateId);
  if (template) {
    ElMessageBox.confirm("加载模板将清空当前画布，确定继续吗？", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    }).then(() => {
      nodes.value = JSON.parse(JSON.stringify(template.nodes));
      edges.value = JSON.parse(JSON.stringify(template.edges));
      saveToHistory();
      fitView();
      ElMessage.success(`已加载模板: ${template.name}`);
    });
  }
}

function handleValidate() {
  const errors = [];
  const warnings = [];

  const allNodes = getNodes.value;
  const allEdges = getEdges.value;

  if (allNodes.length === 0) {
    errors.push("流程中没有节点");
  }

  const startNodes = allNodes.filter((n) => n.type === "input");
  const endNodes = allNodes.filter((n) => n.type === "output");

  if (startNodes.length === 0) {
    errors.push("流程缺少开始节点");
  } else if (startNodes.length > 1) {
    warnings.push("流程有多个开始节点");
  }

  if (endNodes.length === 0) {
    errors.push("流程缺少结束节点");
  } else if (endNodes.length > 1) {
    warnings.push("流程有多个结束节点");
  }

  const nodeIds = new Set(allNodes.map((n) => n.id));
  allEdges.forEach((edge) => {
    if (!nodeIds.has(edge.source)) {
      errors.push(`连线 ${edge.label || edge.id} 的源节点不存在`);
    }
    if (!nodeIds.has(edge.target)) {
      errors.push(`连线 ${edge.label || edge.id} 的目标节点不存在`);
    }
  });

  const orphanNodes = allNodes.filter(
    (node) => !allEdges.some((e) => e.source === node.id || e.target === node.id)
  );

  if (orphanNodes.length > 0) {
    warnings.push(
      `有 ${orphanNodes.length} 个孤立节点: ${orphanNodes.map((n) => n.data.label).join(", ")}`
    );
  }

  if (errors.length > 0) {
    ElMessageBox.alert(
      `<div style="max-height: 300px; overflow-y: auto;">
        <strong>错误 (${errors.length}):</strong>
        <ul>${errors.map((e) => `<li style="color: #f56c6c;">${e}</li>`).join("")}</ul>
        ${
          warnings.length > 0
            ? `<strong>警告 (${warnings.length}):</strong>
        <ul>${warnings.map((w) => `<li style="color: #e6a23c;">${w}</li>`).join("")}</ul>`
            : ""
        }
      </div>`,
      "流程验证结果",
      {
        confirmButtonText: "确定",
        dangerouslyUseHTMLString: true,
      }
    );
  } else if (warnings.length > 0) {
    ElMessageBox.alert(
      `<div style="max-height: 300px; overflow-y: auto;">
        <strong>流程验证通过，但有警告 (${warnings.length}):</strong>
        <ul>${warnings.map((w) => `<li style="color: #e6a23c;">${w}</li>`).join("")}</ul>
      </div>`,
      "流程验证结果",
      {
        confirmButtonText: "确定",
        dangerouslyUseHTMLString: true,
      }
    );
  } else {
    ElMessage.success("流程验证通过，没有发现问题");
  }
}

function toggleGrid() {
  showGrid.value = !showGrid.value;
}

function handleMove({ zoom }) {
  zoomLevel.value = zoom;
}

const onEdgeClick = ({ edge }) => {
  selectedEdge.value = edge;
  updateState.value = "edge";
};

const onNodeClick = ({ node }) => {
  selectedNode.value = node;
  updateState.value = "node";
};

const dragItem = ref(null);

function onDragStart(event, item) {
  if (typeof item === "string") {
    dragItem.value = {
      id: `node-${Date.now()}`,
      data: { label: item },
      type: item === "开始" ? "input" : item === "结束" ? "output" : "custom",
      position: { x: event.clientX, y: event.clientY },
      class: item === "开始" ? "round-start" : item === "结束" ? "round-stop" : "light",
    };
  } else {
    dragItem.value = {
      id: `node-${Date.now()}`,
      data: {
        label: item.label || item.name,
        assignee: item.type === "task" ? "未指定" : undefined,
        priority: item.type === "task" ? "medium" : undefined,
        approver: item.type === "approval" ? "待指定" : undefined,
        approvalType: item.type === "approval" ? "single" : undefined,
        notifyType: item.type === "notification" ? "email" : undefined,
        recipients: item.type === "notification" ? "" : undefined,
        delay: item.type === "timer" ? 0 : undefined,
        condition: item.type === "condition" ? "" : undefined,
        branchCount: item.type === "parallel" ? 2 : undefined,
      },
      type: item.type || "custom",
      position: { x: event.clientX, y: event.clientY },
      class: item.class || "light",
    };
  }
}

function onDragEnd() {
  dragItem.value = null;
}

function onDragOver(event) {
  event.preventDefault();
}

function onDrop(event) {
  const position = screenToFlowCoordinate({
    x: event.clientX,
    y: event.clientY,
  });

  const newNode = {
    ...dragItem.value,
    position,
  };

  const { off } = onNodesInitialized(() => {
    updateNode(dragItem.value?.id, (node) => ({
      position: {
        x: node.position.x - node.dimensions.width / 2,
        y: node.position.y - node.dimensions.height / 2,
      },
    }));

    off();
  });

  dragItem.value = null;
  addNodes(newNode);
  saveToHistory();
}

function handleClosePanel() {
  updateState.value = "";
  selectedNode.value = {};
  selectedEdge.value = {};
}

function handleSaveNode(data) {
  const allNodes = getNodes.value;
  setNodes([
    ...allNodes.filter((n) => n.id !== selectedNode.value.id),
    {
      ...selectedNode.value,
      data: { ...selectedNode.value.data, ...data },
    },
  ]);
  saveToHistory();
}

function handleDeleteNode() {
  ElMessageBox.confirm("确定要删除该节点吗？", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(() => {
    const allNodes = getNodes.value;
    setNodes(allNodes.filter((n) => n.id !== selectedNode.value.id));

    const allEdges = getEdges.value;
    setEdges(
      allEdges.filter(
        (e) => e.source !== selectedNode.value.id && e.target !== selectedNode.value.id
      )
    );

    ElMessage.success("节点删除成功");
    handleClosePanel();
    saveToHistory();
  });
}

function handleSaveEdge(data) {
  const allEdges = getEdges.value;
  setEdges([
    ...allEdges.filter((e) => e.id !== selectedEdge.value.id),
    {
      ...selectedEdge.value,
      label: data.label,
      type: data.type,
      animated: data.animated,
      style: {
        stroke: data.color,
        strokeWidth: data.strokeWidth,
      },
      data: {
        condition: data.condition,
        description: data.description,
      },
    },
  ]);
  saveToHistory();
}

function handleDeleteEdge() {
  ElMessageBox.confirm("确定要删除该连线吗？", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(() => {
    const allEdges = getEdges.value;
    setEdges(allEdges.filter((e) => e.id !== selectedEdge.value.id));
    ElMessage.success("连线删除成功");
    handleClosePanel();
    saveToHistory();
  });
}

function handleSave() {
  const workflowData = {
    nodes: nodes.value,
    edges: edges.value,
  };
  localStorage.setItem("workflowData", JSON.stringify(workflowData));
  ElMessage.success("流程保存成功");
}

function handleLoad() {
  const savedData = localStorage.getItem("workflowData");
  if (savedData) {
    try {
      const workflowData = JSON.parse(savedData);
      nodes.value = workflowData.nodes;
      edges.value = workflowData.edges;
      saveToHistory();
      ElMessage.success("流程加载成功");
    } catch {
      ElMessage.error("流程加载失败");
    }
  } else {
    ElMessage.warning("没有保存的流程数据");
  }
}

function handleClear() {
  ElMessageBox.confirm("确定要清空画布吗？", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(() => {
    nodes.value = [];
    edges.value = [];
    saveToHistory();
    ElMessage.success("画布已清空");
  });
}

function handleZoomIn() {
  zoomIn();
}

function handleZoomOut() {
  zoomOut();
}

function handleFitView() {
  fitView();
}
</script>

<style>
.top-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 4rem;
  padding: 0 4px;
  border-bottom: 1px solid #e5e7eb;
}

.toolbar-left,
.toolbar-right {
  display: flex;
  align-items: center;
}

.toolbar-divider {
  width: 1px;
  height: 24px;
  margin: 0 4px;
}

.zoom-level {
  display: inline-flex;
  align-items: center;
  color: #6b7280;
  white-space: nowrap;
  border-radius: 6px;
}

.main-layout {
  display: flex;
  flex: 1;
  height: calc(100vh - 14rem);
}

.left-panel {
  z-index: 988;
  width: 12rem;
  padding: 4px;
  overflow-y: auto;
  border-right: 1px solid #e5e7eb;
}

.left-panel::-webkit-scrollbar {
  width: 6px;
}

.left-panel::-webkit-scrollbar-track {
  border-radius: 3px;
}

.left-panel::-webkit-scrollbar-thumb {
  border-radius: 3px;
}

.panel-section {
  padding: 12px;
  margin-bottom: 20px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.section-title {
  padding-bottom: 8px;
  margin-bottom: 12px;
  font-size: 11px;
  font-weight: 700;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  border-bottom: 1px solid #f3f4f6;
}

.stats-list {
  font-size: 12px;
}

.stat-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 0;
  color: #6b7280;
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  flex: 1;
  font-weight: 500;
}

.stat-value {
  padding: 2px 8px;
  font-size: 11px;
  font-weight: 600;
  color: #ffffff;
  border-radius: 10px;
}

.shortcut-list {
  font-size: 11px;
}

.shortcut-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 5px 0;
  color: #6b7280;
}

.shortcut-item .key {
  padding: 3px 8px;
  font-family: "Courier New", monospace;
  font-size: 10px;
  font-weight: 600;
  color: #4b5563;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.canvas-container {
  position: relative;
  flex: 1;
  overflow: hidden;
  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.02);
}

.right-panel {
  z-index: 988;
  width: 20rem;
  padding: 16px;
  overflow-y: auto;
  border-left: 1px solid #e5e7eb;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.03);
}

.right-panel::-webkit-scrollbar {
  width: 6px;
}

.right-panel::-webkit-scrollbar-track {
  border-radius: 3px;
}

.right-panel::-webkit-scrollbar-thumb {
  border-radius: 3px;
}

.basic-flow {
  width: 100%;
  height: 100%;
}

.round-start {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  font-size: 12px;
  font-weight: 600;
  color: white;
  text-align: center;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.round-stop {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  font-size: 12px;
  font-weight: 600;
  color: white;
  text-align: center;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.drag-item {
  padding: 10px 16px;
  font-size: 12px;
  font-weight: 500;
  color: white;
  cursor: grab;
  user-select: none;
  background: linear-gradient(135deg, #4a5568 0%, #374151 100%);
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.drag-item:hover {
  transform: translateY(-2px) scale(1.02);
}

.drag-item:active {
  cursor: grabbing;
  transform: translateY(0) scale(0.98);
}

.start-item {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.end-item {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
}

.task-drag-item {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.approval-drag-item {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.condition-drag-item {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
}

.parallel-drag-item {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3);
}

.notification-drag-item {
  background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
  box-shadow: 0 2px 8px rgba(236, 72, 153, 0.3);
}

.timer-drag-item {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
}

.module-top .vue-flow__controls .vue-flow__controls-button {
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.module-top .vue-flow__controls .vue-flow__controls-button:hover {
  transform: scale(1.1);
}

.module-top .vue-flow__controls .vue-flow__controls-button svg {
  width: 1.5rem;
  height: 1.5rem;
  padding-top: 2px;
  padding-left: -1px;
  margin-top: 2px;
}

.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

.ml-2 {
  margin-left: 8px;
}

.mt-2 {
  margin-top: 8px;
}

.w-full {
  width: 100%;
}

.text-center {
  text-align: center;
}

.float-right {
  float: right;
}

.m-2 {
  margin: 8px;
}

.mb-2 {
  margin-bottom: 8px;
}

.gap-y-2 {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

@media (max-width: 1400px) {
  .left-panel {
    width: 14rem;
  }

  .right-panel {
    width: 18rem;
  }
}

@media (max-width: 1024px) {
  .top-toolbar {
    flex-direction: column;
    gap: 12px;
    height: auto;
    padding: 12px;
  }

  .toolbar-left,
  .toolbar-right {
    flex-wrap: wrap;
    justify-content: center;
  }

  .main-layout {
    height: calc(100vh - auto);
  }
}
</style>
