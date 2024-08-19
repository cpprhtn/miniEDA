/// <reference path="./common.d.ts" />

type DataNode = BaseNode & {
  type: NodeType.DATA;
};

type LoadFileNode = BaseNode & {
  filePath: string;
};
