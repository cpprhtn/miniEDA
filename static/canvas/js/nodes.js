/// <reference path="../types/nodes/draft.d.ts" />

import { createId, createRandomString } from "./util.js";
import { useState } from "./state.js";

export function createDraftNode() {
  const [diagram, setDiagram] = useState("diagram");

  /** @type {DraftNode} */
  const draftNode = {
    id: createId(),
    name: `새로운 노드(${createRandomString(3)})`,
    type: "DRAFT",
    preview: null,
  };

  setDiagram({
    ...diagram,
    nodes: [...diagram.nodes, draftNode],
  });
}
