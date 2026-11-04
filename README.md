# Snado

Sandon’s personal website: a little about me, the projects I’m building, and posts on software, AI and language learning.

Built with React, TypeScript, TanStack Start and Vite. Styling uses Tailwind CSS, and posts are written in MDX and compiled with Content Collections.

## Run locally

Use Node.js compatible with Vite 7 and pnpm 10.14.0 (pinned in `package.json`).

```bash
pnpm install
pnpm dev
```

Open the local URL printed by Vite.

## Useful commands

```bash
pnpm build       # Build the site
pnpm preview     # Preview the production build locally
pnpm type-check  # Check TypeScript types
```

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
