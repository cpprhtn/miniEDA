import { useState } from "./state.js";

/**
 * @param {File} file
 * @returns {Promise<string | null>}
 */
async function registerFile(file) {
  if (!file) {
    return null;
  }

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("/canvas/file", {
    method: "POST",
    body: formData,
  });

  /** @type { { fileId: string } } */
  const data = await response.json();

  return data.fileId;
}

export async function run() {
  const [diagram] = useState("diagram");

  const requestBody = {
    nodes: [],
  };

  for (const node of diagram.nodes) {
    if (node.type !== "DATA") {
      requestBody.nodes.push(node);
      continue;
    }

    const dataNode = /** @type {DataNode} */ (node);
    if (dataNode.dataType !== "LOAD_FILE") {
      requestBody.nodes.push(node);
      continue;
    }

    const { file, ...rest } = /** @type {LoadFileNode} */ (dataNode);
    const fileId = await registerFile(file);
    requestBody.nodes.push({ ...rest, fileId });
  }

  await fetch("/canvas/run", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  });
}
