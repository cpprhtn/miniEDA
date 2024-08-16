import "./render-controller-panel.js";
import "./render-canvas.js";

import { callAllStateChangeListener } from "./state.js";
import { createId, createRandomString } from "./util.js";
import { useState } from "./state.js";

function createNode() {
  const [diagram, setDiagram] = useState("diagram");

  const id = createId();
  const label = `새로운 노드(${createRandomString(3)})`;

  setDiagram({
    ...diagram,
    nodes: [...diagram.nodes, { id, label }],
  });
}

function initListeners() {
  const createNodeButton = document.getElementById("create-node");
  if (createNodeButton) {
    createNodeButton.onclick = createNode;
  }
}

window.onload = () => {
  callAllStateChangeListener();
  initListeners();
};

window.onClickNode = (nodeId) => {
  const [diagram] = useState("diagram");
  const [, setSelectedNode] = useState("selectedNode");

  const node = diagram.nodes.find((node) => node.id === nodeId);
  if (!node) return;

  setSelectedNode(node);
};
