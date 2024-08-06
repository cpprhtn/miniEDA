import * as React from "react";
import type { HeadFC, PageProps } from "gatsby";

import MermaidRenderer from "../components/MermaidRenderer";

const IndexPage: React.FC<PageProps> = () => {
  const chart = `
  flowchart TD
    Start --> Stop
  `;

  return (
    <main>
      <MermaidRenderer chart={chart} />
    </main>
  );
};

export default IndexPage;

export const Head: HeadFC = () => <title>Home Page</title>;
