/// <reference path="./common.d.ts" />

type PresentationAction = "SAVE_TO_FILE";

type PresentationNode<TAction extends PresentationAction = PresentationAction> =
  BaseNode<"PRESENTATION"> & {
    action: TAction;
    from: BaseNodeId | null;
  };

type SaveToFileNode = PresentationNode<"SAVE_TO_FILE"> & {
  filePath: string | null;
};
