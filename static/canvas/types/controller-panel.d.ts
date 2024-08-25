/// <reference path="./state.d.ts" />
/// <reference path="./nodes/index.d.ts" />

type RenderControllerPanelFn = StateChangeListener<"selectedNode">;

type ControllerPanelHtmlElement =
  | ControllerPanelHtmlTitle
  | ControllerPanelHtmlText
  | ControllerPanelHtmlSelect
  | ControllerPanelHtmlFile;

type ControllerPanelHtmlTitle = {
  type: "title";
  value: string;
};

type ControllerPanelHtmlText = {
  type: "text";
  label: string;
  value: string;
};

type ControllerPanelHtmlSelect = {
  type: "select";
  id: string;
  label: string;
  options: string[];
};

type ControllerPanelHtmlFile = {
  type: "file";
  id: string;
  label: string;
  file: File | null;
};
