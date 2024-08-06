import * as React from "react";
import { HeadFC } from "gatsby";

export default function NotFoundPage() {
  return (
    <main>
      <h1>Not found</h1>
    </main>
  );
}

export const Head: HeadFC = () => <title>Not found</title>;
