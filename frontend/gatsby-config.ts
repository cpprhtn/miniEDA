import type { GatsbyConfig } from "gatsby";

const config: GatsbyConfig = {
  siteMetadata: {
    title: `mini-eda-frontend-generator`,
  },
  pathPrefix: "/app",
  graphqlTypegen: true,
  plugins: [],
};

export default config;
