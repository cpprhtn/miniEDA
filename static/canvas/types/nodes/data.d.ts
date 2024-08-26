/// <reference path="./common.d.ts" />

type DataNodeType = "LOAD_FILE";

type DataNode<TData extends DataNodeType = DataNodeType> = BaseNode<"DATA"> & {
  dataType: TData;
};

type LoadFileNode = DataNode<"LOAD_FILE"> & {
  file: File | null;
};
