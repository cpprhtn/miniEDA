/// <reference path="./common.d.ts" />

type PresentationNode = BaseNode<"PRESENTATION"> & {
  from: BaseNodeId;
};

type SaveToFileNode = PresentationNode & {
  filePath: string;
};
