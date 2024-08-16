/// <reference path="./node.d.ts" />

type Edge = {
  from: DataNode;
  to: DataNode;
};

type WorkflowGraph = {
  nodes: DataNode[];
  edges: Edge[];
};

type OnNodeClickedListener = (node: DataNode) => void;
