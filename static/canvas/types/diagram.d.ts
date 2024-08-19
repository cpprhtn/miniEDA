/// <reference path="./nodes/common.d.ts" />

type Edge = {
  from: BaseNode;
  to: BaseNode;
};

type WorkflowGraph = {
  nodes: BaseNode[];
  edges: Edge[];
};

type OnNodeClickedListener = (node: BaseNode) => void;
