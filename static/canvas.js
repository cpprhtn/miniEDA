import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";
mermaid.initialize({ startOnLoad: false });

/// <reference path="../types/diagram.d.ts" />

/** @type {WorkflowGraph} */
const diagram = data;

function draw() {
  const diagramCanvas = document.getElementById("diagram-canvas");
  if (!diagramCanvas) {
    throw new Error("Diagram canvas not found");
  }

  let mermaidText = `flowchart LR`;

  diagram.vertices?.forEach((vertex) => {
    mermaidText += `
      ${vertex.id}[${vertex.label}]
    `;
  });
  diagram.edges?.forEach((edge) => {
    mermaidText += `
      ${edge.source} --> ${edge.target}
    `;
  });

  diagramCanvas.textContent = mermaidText;
  mermaid.run();
}

window.onload = () => {
  draw();
};
