declare type NodeType = "DRAFT" | "DATA" | "TRANSFORMER" | "PRESENTATION";

type BaseNodeId = string;

type BaseNode<TNode extends NodeType = NodeType> = {
  id: BaseNodeId;
  name: string;
  type: TNode;
};
