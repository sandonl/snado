# Snado

Sandon’s personal website: a little about me, the projects I’m building, and posts on software, AI and language learning.

Built with React, TypeScript, TanStack Start and Vite. Styling uses Tailwind CSS, and posts are written in MDX and compiled with Content Collections.

## Run locally

Use [Bun](https://bun.sh/) 1.4.3 (pinned in `package.json`) and Node.js compatible with Vite 7.

```bash
bun install
bun run dev
```

Open the local URL printed by Vite.

## Useful commands

```bash
bun run build       # Build the site
bun run preview     # Preview the production build locally
bun run type-check  # Check TypeScript types
```

Commit `bun.lock` when dependencies change. For a reproducible install, use `bun install --frozen-lockfile`.

## Where things live

- `src/routes/` — home, projects and post pages.
- `src/posts/` — MDX posts.
- `src/components/` — shared UI and visual effects.
- `src/app/globals.css` — global styles.
- `public/` — images, icons and other static files.
- `content-collections.ts` — post metadata and MDX compilation.

## Add a post

Create an `.mdx` file in `src/posts/` with this frontmatter, followed by the post content:

```mdx
---
title: "My new post"
summary: "A short description for the posts page."
createdAt: "2026-11-04"
author: "Sandon L"
tags: ["Software"]
slug: "my-new-post"
---

Write the post here.
```

The post appears at `/posts/my-new-post`. Use a unique slug; the posts page lists entries newest first.

## Search and AI discovery

The public site redirects to `https://www.sandonl.dev`. Its canonical origin and shared description live in `src/lib/seo.ts`.

- Each page defines its own title, description, canonical URL and social sharing metadata.
- JSON-LD describes Sandon, the website and individual blog posts using their existing metadata.
- `/robots.txt` allows all crawlers and points to `/sitemap.xml`. This includes AI crawlers; it does not distinguish search from model training.
- `/sitemap.xml` lists the home page, projects, posts index and every published post.
- `/llms.txt` provides a short site overview and links to the pages and posts for AI readers.

The sitemap and llms.txt are server routes generated from Content Collections, so new posts are included automatically on the next build. They are not manually maintained files in `public/`. Update the llms.txt page descriptions if the project list changes.

The site already serves article text in its HTML, so crawlers can read it without running JavaScript. Keep post summaries accurate and headings descriptive. Structured data should describe the visible content.

`llms.txt` is a [proposed format](https://llmstxt.org/), not a promise of indexing or AI citations. [Google's guidance](https://developers.google.com/search/docs/appearance/ai-features) recommends the same sound SEO foundations for its AI search features.

After deployment, submit `https://www.sandonl.dev/sitemap.xml` in Google Search Console and Bing Webmaster Tools. Account verification and sitemap submission are separate from these code changes.
