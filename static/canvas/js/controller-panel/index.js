/// <reference path="../../types/controller-panel.d.ts" />

import { registerStateChangeListener, useState } from "../state.js";
import { ControllerPanelHtmlBuilder } from "./html-builder.js";
import { InputController } from "./input-controller.js";

/**
 * @param {DraftNode} node
 */
function renderDraftNodePanel(node) {
  const panel = document.getElementById("controller-panel-body");
  if (!panel) {
    return;
  }

  const [graph, setGraph] = useState("diagram");
  const inputController = new InputController();

  ControllerPanelHtmlBuilder.builder()
    .title("Node")
    .text("Node ID", node.id)
    .text("Node name", node.name)
    .select("Change type", ["DRAFT", "LOAD_FILE"], inputController)
    .build(panel);

  inputController.get().addEventListener("change", (ev) => {
    if (ev.target["value"] === "LOAD_FILE") {
      /** @type {LoadFileNode} */
      const newNode = {
        id: node.id,
        name: node.name,
        type: "DATA",
        dataType: "LOAD_FILE",
        file: null,
      };

      setGraph({
        nodes: [...graph.nodes.filter((v) => v.id !== node.id), newNode],
      });
      renderControllerPanel(newNode);
    }
  });
}

/**
 * @param {DataNode} node
 */
function renderDataNodePanel(node) {
  switch (node.dataType) {
    case "LOAD_FILE":
      const loadFileNode = /** @type {LoadFileNode} */ (node);
      renderLoadFileNodePanel(loadFileNode);
      break;
  }
}

/**
 * @param {LoadFileNode} node
 */
function renderLoadFileNodePanel(node) {
  const panel = document.getElementById("controller-panel-body");
  if (!panel) {
    return;
  }

  const [graph, setGraph] = useState("diagram");
  const fileController = new InputController();

  ControllerPanelHtmlBuilder.builder()
    .title("Node")
    .text("Node ID", node.id)
    .text("Node name", node.name)
    .file("File", node.file, fileController)
    .build(panel);

  fileController.get().addEventListener("change", (ev) => {
    const target = /** @type {HTMLInputElement} */ (ev.target);
    if (target.files && target.files[0]) {
      /** @type {LoadFileNode} */
      const newNode = {
        id: node.id,
        name: node.name,
        type: "DATA",
        dataType: "LOAD_FILE",
        file: target.files[0],
      };

      setGraph({
        nodes: [...graph.nodes.filter((v) => v.id !== node.id), newNode],
      });
      renderControllerPanel(newNode);
    }
  });
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
    case "DATA":
      const dataNode = /** @type {DataNode} */ (node);
      renderDataNodePanel(dataNode);
      break;
  }
}

registerStateChangeListener("selectedNode", renderControllerPanel);
