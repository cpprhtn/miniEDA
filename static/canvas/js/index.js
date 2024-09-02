import "./controller-panel/index.js";
import "./render-canvas.js";

import { callAllStateChangeListener } from "./state.js";
import { useState } from "./state.js";
import { createDraftNode } from "./nodes.js";
import { run } from "./runner.js";

function initListeners() {
  const createNodeButton = document.getElementById("create-node");
  if (createNodeButton) {
    createNodeButton.onclick = createDraftNode;
  }

  const runTaskButton = document.getElementById("run-task");
  if (runTaskButton) {
    runTaskButton.onclick = run;
  }
}

window.onload = () => {
  callAllStateChangeListener();
  initListeners();
};

/**
 * @param {string} nodeId
 */
window["onClickNode"] = (nodeId) => {
  const [diagram] = useState("diagram");
  const [, setSelectedNode] = useState("selectedNode");

  const node = diagram.nodes.find((node) => node.id === nodeId);
  if (!node) return;

  setSelectedNode(node);
};
