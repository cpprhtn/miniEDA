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

  /** @type {(value: string) => void} */
  const onChangeType = (value) => {
    let newNode = null;

    if (value === "LOAD_FILE") {
      /** @type {LoadFileNode} */
      const loadFileNode = {
        id: node.id,
        name: node.name,
        type: "DATA",
        preview: null,
        dataType: "LOAD_FILE",
        file: null,
      };
      newNode = loadFileNode;
    } else if (value === "FILL_MISSING_WITH_ZERO") {
      /** @type {FillMissingValueWithZeroTransformerNode} */
      const fillMissingValueWithZeroTransformerNode = {
        id: node.id,
        name: node.name,
        type: "TRANSFORMER",
        preview: null,
        action: "FILL_WITH_ZERO",
        fromNodeId: null,
      };
      newNode = fillMissingValueWithZeroTransformerNode;
    } else if (value === "SAVE_TO_FILE") {
      /** @type {SaveToFileNode} */
      const saveToFileNode = {
        id: node.id,
        name: node.name,
        type: "PRESENTATION",
        preview: null,
        action: "SAVE_TO_FILE",
        fromNodeId: null,
        filePath: null,
      };
      newNode = saveToFileNode;
    }

    setGraph({
      nodes: [...graph.nodes.filter((v) => v.id !== node.id), newNode],
    });
    renderControllerPanel(newNode.id);
  };

  ControllerPanelHtmlBuilder.builder()
    .title("Draft node")
    .text("Node ID", node.id)
    .text("Node name", node.name)
    .select(
      "Change type",
      ["DRAFT", "LOAD_FILE", "FILL_MISSING_WITH_ZERO", "SAVE_TO_FILE"],
      onChangeType
    )
    .build(panel);
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
    .title("Load file node")
    .text("Node ID", node.id)
    .text("Node name", node.name)
    .file("File", node.file, fileController)
    .title("Preview")
    .preview(node.preview)
    .build(panel);

  fileController.get().addEventListener("change", (ev) => {
    const target = /** @type {HTMLInputElement} */ (ev.target);
    if (target.files && target.files[0]) {
      /** @type {LoadFileNode} */
      const newNode = {
        ...node,
        file: target.files[0],
      };

      setGraph({
        nodes: [...graph.nodes.filter((v) => v.id !== node.id), newNode],
      });
      renderControllerPanel(newNode.id);
    }
  });
}

/**
 * @param {DataTransformerNode} node
 */
function renderTransformerNodePanel(node) {
  switch (node.action) {
    case "FILL_WITH_ZERO":
      const fillWithZeroNode =
        /** @type {FillMissingValueWithZeroTransformerNode} */ (node);
      renderFillWithZeroNodePanel(fillWithZeroNode);
      break;
  }
}

/**
 * @param {FillMissingValueWithZeroTransformerNode} node
 */
function renderFillWithZeroNodePanel(node) {
  const panel = document.getElementById("controller-panel-body");
  if (!panel) {
    return;
  }

  const [graph, setGraph] = useState("diagram");
  const fromNodeInputController = new InputController();

  /** @type {(fromNodeId: string) => void } */
  const onConfirmFromNode = (fromNodeId) => {
    if (node.id === fromNodeId) {
      alert("Cannot connect to itself");
      return;
    }

    const fromNode = graph.nodes.find((v) => v.id === fromNodeId);
    if (!fromNode) {
      alert("Node not found");
      return;
    }

    if (!["DATA", "TRANSFORMER"].includes(fromNode.type)) {
      alert("Invalid type for connection");
      return;
    }

    /** @type {FillMissingValueWithZeroTransformerNode} */
    const newNode = {
      ...node,
      fromNodeId: fromNodeId,
    };

    setGraph({
      nodes: [...graph.nodes.filter((v) => v.id !== node.id), newNode],
    });
    renderControllerPanel(newNode.id);
  };

  ControllerPanelHtmlBuilder.builder()
    .title("Fill with zero node")
    .text("Node ID", node.id)
    .text("Node name", node.name)
    .textField(
      "From (Node ID)",
      node.fromNodeId ?? "",
      fromNodeInputController,
      onConfirmFromNode
    )
    .title("Preview")
    .preview(node.preview)
    .build(panel);
}

/**
 * @param {PresentationNode} node
 */
function renderPresentationNodePanel(node) {
  switch (node.action) {
    case "SAVE_TO_FILE":
      const saveToFileNode = /** @type {SaveToFileNode} */ (node);
      renderSaveToFileNodePanel(saveToFileNode);
      break;
  }
}

/**
 * @param {SaveToFileNode} node
 */
function renderSaveToFileNodePanel(node) {
  const panel = document.getElementById("controller-panel-body");
  if (!panel) {
    return;
  }

  const [graph, setGraph] = useState("diagram");

  /** @type {<K extends keyof SaveToFileNode>(key: K, value: SaveToFileNode[K]) => void} */
  const applyChange = (key, value) => {
    /** @type {SaveToFileNode} */
    const newNode = {
      ...node,
      [key]: value,
    };

    setGraph({
      nodes: [...graph.nodes.filter((v) => v.id !== node.id), newNode],
    });
    renderControllerPanel(newNode.id);
  };

  /** @type {(fromNodeId: string) => void } */
  const onConfirmFromNode = (fromNodeId) => {
    if (node.id === fromNodeId) {
      alert("Cannot connect to itself");
      return;
    }

    const fromNode = graph.nodes.find((v) => v.id === fromNodeId);
    if (!fromNode) {
      alert("Node not found");
      return;
    }

    if (!["DATA", "TRANSFORMER"].includes(fromNode.type)) {
      alert("Invalid type for connection");
      return;
    }

    applyChange("fromNodeId", fromNodeId);
  };

  /** @type {(filePath: string) => void } */
  const onConfirmFilePath = (filePath) => {
    applyChange("filePath", filePath);
  };

  ControllerPanelHtmlBuilder.builder()
    .title("Save to file node")
    .text("Node ID", node.id)
    .text("Node name", node.name)
    .textField("From (Node ID)", node.fromNodeId ?? "", null, onConfirmFromNode)
    .textField("File path", node.filePath ?? "", null, onConfirmFilePath)
    .build(panel);
}

/** @type {RenderControllerPanelFn} */
export function renderControllerPanel(nodeId) {
  if (!nodeId) {
    return;
  }

  const [graph] = useState("diagram");
  const node = graph.nodes.find((v) => v.id === nodeId);

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
    case "TRANSFORMER":
      const transformerNode = /** @type {DataTransformerNode} */ (node);
      renderTransformerNodePanel(transformerNode);
      break;
    case "PRESENTATION":
      const presentationNode = /** @type {PresentationNode} */ (node);
      renderPresentationNodePanel(presentationNode);
      break;
  }
}

registerStateChangeListener("selectedNodeId", renderControllerPanel);
