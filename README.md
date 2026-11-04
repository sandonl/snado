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
