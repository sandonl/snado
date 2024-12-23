import {
  createDefaultImport,
  defineCollection,
  defineConfig,
} from "@content-collections/core";
import { MDXContent } from "mdx/types";

const posts = defineCollection({
  name: "posts",
  directory: "src/posts",
  include: "**/*.mdx",
  parser: "frontmatter-only",
  schema: (z) => ({
    title: z.string(),
    summary: z.string(),
    createdAt: z.string(),
    author: z.string(),
    tags: z.array(z.string()),
    slug: z.string(),
  }),
  transform: ({ _meta, ...post }) => {
    const mdxContent = createDefaultImport<MDXContent>(
      `@/posts/${_meta.filePath}`
    );
    return {
      ...post,
      mdxContent,
    };
  },
});

export default defineConfig({
  collections: [posts],
});
