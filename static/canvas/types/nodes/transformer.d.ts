/// <reference path="./common.d.ts" />

declare enum TransformAction {
  FILL_WITH_ZERO = "FILL_WITH_ZERO",
}

type DataTransformerNode = BaseNode & {
  type: NodeType.TRANSFORMER;
  action: TransformAction;
  from: BaseNodeId;
};

type FillMissingValueWithZeroTransformerNode = DataTransformerNode & {
  action: TransformAction.FILL_WITH_ZERO;
};
