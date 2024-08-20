// @ts-ignore
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";

import { registerStateChangeListener } from "./state.js";

mermaid.initialize({ startOnLoad: false, securityLevel: "loose" });

/** @param {WorkflowGraph} diagram */
function draw(diagram) {
  const diagramCanvas = document.getElementById("diagram-canvas");
  if (!diagramCanvas) {
    throw new Error("Diagram canvas not found");
  }

  let mermaidText = `flowchart LR`;

  diagram.nodes?.forEach((node) => {
    mermaidText += `
      ${node.id}["${node.name}"]
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

registerStateChangeListener("diagram", draw);
