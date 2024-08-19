/// <reference path="../../types/controller-panel.d.ts" />

import { registerStateChangeListener } from "../state.js";
import { ControllerPanelHtmlBuilder } from "./html-builder.js";

/**
 * @param {DraftNode} node
 */
function renderDraftNodePanel(node) {
  const panel = document.getElementById("controller-panel-body");
  if (!panel) {
    return;
  }

  panel.innerHTML = ControllerPanelHtmlBuilder.builder()
    .title("Node")
    .text("Node ID", node.id)
    .text("Node name", node.name)
    .build();
}

/** @type {RenderControllerPanelFn} */
export function renderControllerPanel(node) {
  if (!node) {
    return;
  }

  switch (node.type) {
    case "DRAFT":
      const draftNode = /** @type {DraftNode} */ (node);
      renderDraftNodePanel(draftNode);
      break;
  }
}

registerStateChangeListener("selectedNode", renderControllerPanel);
