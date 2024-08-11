type DataNode = {
  id: string;
  label: string;
};

type Edge = {
  from: DataNode;
  to: DataNode;
};

type WorkflowGraph = {
  nodes: DataNode[];
  edges: Edge[];
};
