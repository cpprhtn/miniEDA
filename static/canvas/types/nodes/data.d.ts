/// <reference path="./common.d.ts" />

type DataNode = BaseNode<"DATA">;

type LoadFileNode = DataNode & {
  filePath: string | null;
};
