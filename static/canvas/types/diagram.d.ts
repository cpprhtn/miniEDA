/// <reference path="./nodes/common.d.ts" />

type WorkflowGraph = {
  nodes: BaseNode[];
};

type OnNodeClickedListener = (node: BaseNode) => void;
