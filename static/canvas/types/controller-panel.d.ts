/// <reference path="./state.d.ts" />

type RenderNormalNodePanelFn = (node: DataNode) => void;

type RenderControllerPanelFn = StateChangeListener<"selectedNode">;
