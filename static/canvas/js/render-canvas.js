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
      ${node.id}["${node.name}"]:::${node.type}
    `;
  });

  diagram.nodes?.forEach((node) => {
    mermaidText += `
      click ${node.id} href "javascript:onClickNode('${node.id}')"
    `;
  });

  diagram.nodes.forEach((node) => {
    if (node.type === "TRANSFORMER") {
      const transformerNode = /** @type {DataTransformerNode} */ (node);

      if (transformerNode.fromNodeId) {
        mermaidText += `
          ${transformerNode.fromNodeId} --> ${transformerNode.id}
        `;
      }
    } else if (node.type === "PRESENTATION") {
      const presentationNode = /** @type {PresentationNode} */ (node);

      if (presentationNode.fromNodeId) {
        mermaidText += `
          ${presentationNode.fromNodeId} --> ${presentationNode.id}
        `;
      }
    }
  });

  const colorDefinitions = {
    DRAFT: "#FFD700",
    DATA: "#FFA07A",
    TRANSFORMER: "#98FB98",
    PRESENTATION: "#87CEFA",
  };
  Object.entries(colorDefinitions).forEach(([type, color]) => {
    mermaidText += `
      classDef ${type} fill:${color},stroke:#333,stroke-width:2px;
    `;
  });

  const mermaidElement = document.getElementById("diagram-canvas");
  mermaidElement.removeAttribute("data-processed");

  diagramCanvas.textContent = mermaidText;

  mermaid.run();
}

registerStateChangeListener("diagram", draw);
