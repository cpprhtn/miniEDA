/// <reference path="./common.d.ts" />

type TransformAction = "FILL_WITH_ZERO";

type DataTransformerNode<TAction extends TransformAction = TransformAction> =
  BaseNode<"TRANSFORMER"> & {
    action: TAction;
    from: BaseNodeId | null;
  };

type FillMissingValueWithZeroTransformerNode =
  DataTransformerNode<"FILL_WITH_ZERO">;
