declare enum NodeType {
  DRAFT = "DRAFT",
  DATA = "DATA",
  TRANSFORMER = "TRANSFORMER",
  PRESENTATION = "PRESENTATION",
}

type BaseNodeId = string;

type BaseNode = {
  id: BaseNodeId;
  name: string;
  type: NodeType;
};
