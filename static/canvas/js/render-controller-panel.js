/// <reference path="../types/controller-panel.d.ts" />

import { registerStateChangeListener } from "./state.js";

/**TODO[lery]: 테스트용으로 추가한 함수입니다. 이후 노드 유형 구분 시 별도 구현 예정입니다.
 *
 * @type {RenderNormalNodePanelFn}
 */
function renderNormalNodePanel(node) {
  const panel = document.getElementById("controller-panel-body");
  if (!panel) {
    return;
  }

  panel.innerHTML = `
    <h2>Node</h2>
    <p>Node ID: ${node.id}</p>
    <p>Node label: ${node.label}</p>
  `;
}

/** @type {RenderControllerPanelFn} */
export function renderControllerPanel(node) {
  if (!node) {
    return;
  }

  renderNormalNodePanel(node);
}

registerStateChangeListener("selectedNode", renderControllerPanel);
