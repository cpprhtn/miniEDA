/// <reference path="./state.d.ts" />

type RenderNormalNodePanelFn = (node: BaseNode) => void;

type RenderControllerPanelFn = StateChangeListener<"selectedNode">;
