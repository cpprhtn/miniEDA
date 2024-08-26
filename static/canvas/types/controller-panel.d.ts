/// <reference path="./state.d.ts" />
/// <reference path="./nodes/index.d.ts" />

type RenderControllerPanelFn = StateChangeListener<"selectedNode">;

type ControllerPanelHtmlElement =
  | ControllerPanelHtmlTitle
  | ControllerPanelHtmlText
  | ControllerPanelHtmlSelect
  | ControllerPanelHtmlFile
  | ControllerPanelHtmlTextField;

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
  onChange?: (value: string) => void;
};

type ControllerPanelHtmlFile = {
  type: "file";
  id: string;
  label: string;
  file: File | null;
};

type ControllerPanelHtmlTextField = {
  type: "text-field";
  id: string;
  label: string;
  value: string;
  onConfirm?: (value: string) => void;
};
