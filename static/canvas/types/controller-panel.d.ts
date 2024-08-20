/// <reference path="./state.d.ts" />
/// <reference path="./nodes/index.d.ts" />

type RenderControllerPanelFn = StateChangeListener<"selectedNode">;

type ControllerPanelHtmlElement =
  | ControllerPanelHtmlTitle
  | ControllerPanelHtmlText;

type ControllerPanelHtmlTitle = {
  type: "title";
  value: string;
};

type ControllerPanelHtmlText = {
  type: "text";
  label: string;
  value: string;
};
