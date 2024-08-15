import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";

import { createId, createRandomString } from "./util.js";
import { useState } from "./state.js";
import "./controller-panel.js";

mermaid.initialize({ startOnLoad: false, securityLevel: "loose" });

function draw() {
  const [diagram] = useState("diagram");

  const diagramCanvas = document.getElementById("diagram-canvas");
  if (!diagramCanvas) {
    throw new Error("Diagram canvas not found");
  }

  let mermaidText = `flowchart LR`;

  diagram.nodes?.forEach((node) => {
    mermaidText += `
      ${node.id}["${node.label}"]
    `;
  });
  diagram.edges?.forEach((edge) => {
    mermaidText += `
      ${edge.source} --> ${edge.target}
    `;
  });

  diagram.nodes?.forEach((node) => {
    mermaidText += `
      click ${node.id} href "javascript:onClickNode('${node.id}')"
    `;
  });

  const mermaidElement = document.getElementById("diagram-canvas");
  mermaidElement.removeAttribute("data-processed");

  diagramCanvas.textContent = mermaidText;

  mermaid.run();
}

function createNode() {
  const id = createId();
  const label = `새로운 노드(${createRandomString(3)})`;
  diagram.nodes.push({ id, label });
  draw();
}

function initListeners() {
  const createNodeButton = document.getElementById("create-node");
  if (createNodeButton) {
    createNodeButton.onclick = createNode;
  }
}

window.onload = () => {
  draw();
  initListeners();
};

window.onClickNode = (nodeId) => {
  const [diagram] = useState("diagram");
  const [, setSelectedNode] = useState("selectedNode");

  const node = diagram.nodes.find((node) => node.id === nodeId);
  if (!node) return;

  setSelectedNode(node);
};
