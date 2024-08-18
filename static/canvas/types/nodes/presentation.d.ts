/// <reference path="./common.d.ts" />

type PresentationNode = BaseNode & {
  type: NodeType.PRESENTATION;
  from: BaseNodeId;
};

type SaveToFileNode = BaseNode & {
  filePath: string;
};
