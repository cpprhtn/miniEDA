/// <reference path="../types/diagram.d.ts" />

import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";
import { createId, createRandomString } from "./util.js";

mermaid.initialize({ startOnLoad: false });

/** @type {WorkflowGraph} */
const diagram = data;

async function draw() {
  const diagramCanvas = document.getElementById("diagram-canvas");
  if (!diagramCanvas) {
    throw new Error("Diagram canvas not found");
  }

  let mermaidText = `flowchart LR`;

  diagram.nodes?.forEach((vertex) => {
    mermaidText += `
      ${vertex.id}["${vertex.label}"]
    `;
  });
  diagram.edges?.forEach((edge) => {
    mermaidText += `
      ${edge.source} --> ${edge.target}
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
window.draw = draw;
