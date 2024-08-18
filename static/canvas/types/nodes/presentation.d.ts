/// <reference path="./common.d.ts" />

type PresentationNode = BaseNode & {
  type: NodeType.PRESENTATION;
};

type SaveToFileNode = BaseNode & {
  filePath: string;
};
