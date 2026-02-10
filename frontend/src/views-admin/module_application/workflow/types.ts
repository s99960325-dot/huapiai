import type { CSSProperties } from "vue";

export type NodeType =
  | "input"
  | "output"
  | "task"
  | "approval"
  | "condition"
  | "parallel"
  | "notification"
  | "timer"
  | "default";

export type EdgeType = "default" | "straight" | "step" | "smoothstep" | "bezier";

export type HandlePosition = "left" | "right" | "top" | "bottom";

export interface TaskNodeData {
  label: string;
  assignee?: string;
  priority?: "low" | "medium" | "high";
  description?: string;
}

export interface ApprovalNodeData {
  label: string;
  approver?: string;
  approvalType?: "single" | "multi" | "sequential" | "parallel";
  description?: string;
}

export interface ConditionNodeData {
  label: string;
  condition?: string;
  description?: string;
}

export interface ParallelNodeData {
  label: string;
  branchCount?: number;
  description?: string;
}

export interface NotificationNodeData {
  label: string;
  notifyType?: "email" | "sms" | "push" | "webhook";
  recipients?: string;
  description?: string;
}

export interface TimerNodeData {
  label: string;
  delay?: number;
  unit?: "seconds" | "minutes" | "hours" | "days";
  description?: string;
}

export type NodeData =
  | TaskNodeData
  | ApprovalNodeData
  | ConditionNodeData
  | ParallelNodeData
  | NotificationNodeData
  | TimerNodeData
  | Record<string, any>;

export interface Marker {
  type: "arrow" | "arrowclosed";
  color?: string;
  width?: number;
  height?: number;
  orient?: "auto" | "auto-start-reverse";
}

export interface Node {
  id: string;
  position: { x: number; y: number };
  type?: NodeType;
  data?: NodeData;
  label?: string;
  style?: CSSProperties;
  class?: string | string[];
  sourcePosition?: HandlePosition;
  targetPosition?: HandlePosition;
  hidden?: boolean;
  selected?: boolean;
  draggable?: boolean;
  connectable?: boolean;
  deletable?: boolean;
  selectable?: boolean;
  focusable?: boolean;
  dragHandle?: string;
  extent?: "parent" | [number, number] | [[number, number], [number, number]];
  parentNode?: string;
  expandParent?: boolean;
  zIndex?: number;
}

export interface Edge {
  id?: string;
  source: string;
  target: string;
  sourceHandle?: string;
  targetHandle?: string;
  type?: EdgeType;
  label?: string;
  labelStyle?: CSSProperties;
  labelShowBg?: boolean;
  labelBgStyle?: CSSProperties;
  labelBgPadding?: [number, number];
  labelBgBorderRadius?: number;
  style?: CSSProperties;
  class?: string | string[];
  animated?: boolean;
  hidden?: boolean;
  selected?: boolean;
  deletable?: boolean;
  selectable?: boolean;
  focusable?: boolean;
  updatable?: boolean | "source" | "target";
  markerStart?: Marker | string;
  markerEnd?: Marker | string;
  pathOptions?: {
    offset?: number;
    borderRadius?: number;
    curvature?: number;
  };
  interactionWidth?: number;
}

export interface WorkflowTemplate {
  id: string;
  name: string;
  description?: string;
  nodes: Node[];
  edges: Edge[];
}

export interface WorkflowStats {
  totalNodes: number;
  totalEdges: number;
  nodeTypes: Record<NodeType, number>;
}

export interface NodeConfig {
  id: string;
  type: NodeType;
  data: NodeData;
}

export interface EdgeConfig {
  id: string;
  source: string;
  target: string;
  label?: string;
  type?: EdgeType;
  animated?: boolean;
}
