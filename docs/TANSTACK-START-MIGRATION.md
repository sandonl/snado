# Migrating from Next.js to TanStack Start

## Overview

This document provides a comprehensive guide for migrating the snado blog/portfolio from Next.js 15 to TanStack Start. This migration maintains identical functionality while modernizing the tech stack with Vite-based builds and TanStack's type-safe routing system.

### Why Migrate?

- **Better Type Safety**: TanStack Start provides comprehensive TypeScript support throughout the entire application
- **Unified Ecosystem**: Seamless integration with TanStack Query, Router, and other TanStack libraries
- **Modern Build Tooling**: Vite offers faster development experience with instant HMR
- **Performance**: Streaming SSR and optimized code splitting out of the box

### What Changes

| Aspect | Next.js 15 | TanStack Start |
|--------|------------|----------------|
| Build Tool | Webpack | Vite |
| Routing | App Router (`/app`) | File-based (`/routes`) |
| Metadata | `export const metadata` | `head()` function |
| Fonts | `next/font/google` | Fontsource packages |
| View Transitions | `next-view-transitions` | TanStack Router native |
| Content Collections | `@content-collections/next` | `@content-collections/vite` |

### What Stays the Same

- ✅ All MDX content files (no changes needed)
- ✅ Tailwind CSS configuration and styling
- ✅ shadcn/ui components
- ✅ Motion animations
- ✅ Vercel Analytics
- ✅ Content Collections schema and structure

---

## Prerequisites

### Required Knowledge
- TypeScript fundamentals
- React 19 features
- File-based routing concepts
- Basic Vite configuration

### Required Tools
- Node.js 18+ or 20+
- pnpm (package manager used in this project)
- Git (for version control)

### Recommended Reading
- [TanStack Start Documentation](https://tanstack.com/start/latest/docs)
- [TanStack Router Documentation](https://tanstack.com/router/latest/docs)
- [Vite Documentation](https://vitejs.dev/)

---

## Migration Steps

### 1. Dependencies

#### Remove Next.js Dependencies

```bash
pnpm remove next @next/mdx next-view-transitions @content-collections/next
```

**Packages being removed:**
- `next@15.5.7` - Next.js framework
- `@next/mdx@15.1.2` - Next.js MDX integration
- `next-view-transitions@0.1.0` - View transitions library
- `@content-collections/next@0.2.4` - Next.js adapter for Content Collections

#### Add TanStack Start Dependencies

```bash
# Core TanStack Start packages
pnpm add @tanstack/react-start@1.x.x @tanstack/react-router @tanstack/react-router-devtools

# Vite and build tools
pnpm add -D vite @vitejs/plugin-react vite-tsconfig-paths

# Content Collections Vite adapter
pnpm add -D @content-collections/vite

# MDX support for Vite
pnpm add -D @mdx-js/rollup

# Font packages (replacing next/font/google)
pnpm add @fontsource/geist-sans @fontsource/geist-mono
```

**Note**: Pin `@tanstack/react-start` to an exact version (e.g., `1.0.0-rc.1`) since it's in RC stage.

#### Update package.json Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "start": "vite preview",
    "lint": "next lint",
    "type-check": "tsc --noEmit"
  }
}
```

---

### 2. Configuration Files

#### Create `vite.config.ts`

```typescript
import { defineConfig } from 'vite'
import { tanstackStart } from '@tanstack/react-start/plugin/vite'
import viteReact from '@vitejs/plugin-react'
import contentCollections from '@content-collections/vite'
import mdx from '@mdx-js/rollup'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [
    // IMPORTANT: contentCollections MUST be first!
    contentCollections(),
    
    // TanStack Start plugin
    tanstackStart({
      srcDirectory: 'src',
      router: {
        routesDirectory: 'routes'
      },
      server: {
        preset: 'vercel'  // For Vercel deployment
      },
      prerender: {
        enabled: true  // Enable SSG for static site
      }
    }),
    
    // React plugin
    viteReact(),
    
    // MDX support
    mdx(),
    
    // Path aliases support (@/* imports)
    tsconfigPaths()
  ]
})
```

**Key Configuration Points:**
- `contentCollections()` must be the first plugin
- `server: { preset: 'vercel' }` configures Vercel deployment
- `prerender: { enabled: true }` enables static site generation
- `tsconfigPaths()` enables `@/*` path aliases

#### Create `app.config.ts`

```typescript
import { defineConfig } from '@tanstack/react-start/config'

export default defineConfig({
  routes: {
    directory: 'src/routes'
  },
  prerender: {
    routes: [
      '/',
      '/posts'
      // Dynamic routes will be discovered automatically
    ]
  }
})
```

#### Update `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "paths": {
      "@/*": ["./src/*"],
      "content-collections": ["./.content-collections/generated"]
    },
    "types": ["vite/client"]
  },
  "include": ["**/*.ts", "**/*.tsx", ".content-collections/generated"],
  "exclude": ["node_modules"]
}
```

**Changes from Next.js:**
- Removed `plugins: [{ "name": "next" }]`
- Added `"types": ["vite/client"]`
- Updated `include` to remove `.next/types/**/*.ts`

#### Delete `next.config.ts`

This file is no longer needed. Vite configuration replaces it.

#### Keep `postcss.config.mjs` (for Tailwind v3)

```javascript
/** @type {import('postcss-load-config').Config} */
const config = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}

export default config
```

**Note**: This stays unchanged for Phase 1. Tailwind v4 migration is Phase 2.

---

### 3. Routing Migration

TanStack Start uses file-based routing with different conventions than Next.js App Router.

#### Routing Conventions Comparison

| Next.js App Router | TanStack Start | Purpose |
|-------------------|----------------|---------|
| `app/layout.tsx` | `routes/__root.tsx` | Root layout |
| `app/page.tsx` | `routes/index.tsx` | Home page |
| `app/posts/page.tsx` | `routes/posts/index.tsx` | Posts listing |
| `app/posts/[slug]/page.tsx` | `routes/posts/$slug.tsx` | Dynamic post page |
| `app/not-found.tsx` | `notFoundComponent` in route | 404 handling |

#### Create Entry Files

**`src/client.tsx`** (Client entry point):

```typescript
import { hydrateRoot } from 'react-dom/client'
import { StartClient } from '@tanstack/react-start'
import { createRouter } from './router'

const router = createRouter()

hydrateRoot(document, <StartClient router={router} />)
```

**`src/server.tsx`** (Server entry point):

```typescript
import { renderToString } from 'react-dom/server'
import { StartServer } from '@tanstack/react-start'
import { createRouter } from './router'

export function render(url: string) {
  const router = createRouter()
  return renderToString(<StartServer router={router} url={url} />)
}
```

**`src/router.tsx`** (Router configuration):

```typescript
import { createRouter as createTanStackRouter } from '@tanstack/react-router'
import { routeTree } from './routeTree.gen'

export function createRouter() {
  return createTanStackRouter({
    routeTree,
    defaultViewTransition: true  // Enable view transitions
  })
}

declare module '@tanstack/react-router' {
  interface Register {
    router: ReturnType<typeof createRouter>
  }
}
```

---

### 4. Layout & Metadata

#### Root Layout Transformation

**Before (Next.js `src/app/layout.tsx`):**

```typescript
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Header from "@/components/header";
import Footer from "@/components/footer";
import { ViewTransitions } from "next-view-transitions";
import type { Metadata } from "next";
import { Analytics } from "@vercel/analytics/react";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Sandon Lai",
  description: "Sandon Lai's personal website",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ViewTransitions>
      <html lang="en">
        <body
          className={`${geistSans.variable} ${geistMono.variable} antialiased bg-[#1b1b1b] max-w-2xl mx-auto px-4 selection:bg-sky-300 selection:text-sky-900`}
        >
          <Header />
          {children}
          <Footer />
          <Analytics />
        </body>
      </html>
    </ViewTransitions>
  );
}
```

**After (TanStack Start `src/routes/__root.tsx`):**

```typescript
import { Outlet, createRootRoute } from '@tanstack/react-router'
import { Meta, Scripts } from '@tanstack/react-start'
import Header from '@/components/header'
import Footer from '@/components/footer'
import { Analytics } from '@vercel/analytics/react'

// Import Fontsource fonts
import '@fontsource/geist-sans/400.css'
import '@fontsource/geist-sans/700.css'
import '@fontsource/geist-mono/400.css'

// Import global styles
import '@/app/globals.css'

export const Route = createRootRoute({
  head: () => ({
    meta: [
      { charSet: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { title: 'Sandon Lai' },
      { name: 'description', content: "Sandon Lai's personal website" }
    ]
  }),
  component: RootLayout
})

function RootLayout() {
  return (
    <html lang="en">
      <head>
        <Meta />
      </head>
      <body className="font-sans antialiased bg-[#1b1b1b] max-w-2xl mx-auto px-4 selection:bg-sky-300 selection:text-sky-900">
        <Header />
        <Outlet />
        <Footer />
        <Analytics />
        <Scripts />
      </body>
    </html>
  )
}
```

**Key Changes:**
1. `createRootRoute` instead of default export
2. `head()` function instead of `export const metadata`
3. `<Outlet />` instead of `{children}`
4. `<Meta />` and `<Scripts />` components required
5. Fontsource imports instead of `next/font/google`
6. No `ViewTransitions` wrapper (handled by router)

---

### 5. Font Loading

#### Fontsource Setup

**Install font packages:**

```bash
pnpm add @fontsource/geist-sans @fontsource/geist-mono
```

**Import in `__root.tsx`:**

```typescript
import '@fontsource/geist-sans/400.css'  // Regular weight
import '@fontsource/geist-sans/700.css'  // Bold weight
import '@fontsource/geist-mono/400.css'  // Monospace regular
```

**Update `tailwind.config.ts`:**

```typescript
export default {
  theme: {
    extend: {
      fontFamily: {
        sans: ['Geist Sans', 'sans-serif'],
        mono: ['Geist Mono', 'monospace']
      }
    }
  }
}
```

**Update CSS classes:**

Replace `${geistSans.variable} ${geistMono.variable}` with `font-sans` (Tailwind will use the configured fonts).

---

### 6. View Transitions

TanStack Router has built-in support for the View Transitions API.

#### Enable in Router Config

In `src/router.tsx`:

```typescript
export function createRouter() {
  return createTanStackRouter({
    routeTree,
    defaultViewTransition: true  // Enable view transitions globally
  })
}
```

#### CSS for View Transitions (Optional)

Add to `globals.css` if you want custom transition effects:

```css
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.3s;
}
```

**Note**: The default crossfade transition should match the current `next-view-transitions` behavior.

---

### 7. Content Collections

Content Collections works with both Next.js and TanStack Start - only the adapter changes.

#### Update `content-collections.ts`

**No changes needed!** The configuration stays identical:

```typescript
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
```

#### Vite Plugin Configuration

Already covered in `vite.config.ts` - ensure `contentCollections()` is the first plugin.

---

### 8. Component Updates

#### Link Component Migration

**Before (using `next-view-transitions`):**

```typescript
import { Link } from "next-view-transitions";

<Link href="/posts" className="...">
  Posts
</Link>
```

**After (using TanStack Router):**

```typescript
import { Link } from '@tanstack/react-router'

<Link to="/posts" className="...">
  Posts
</Link>
```

**Key Changes:**
- Import from `@tanstack/react-router`
- `href` prop becomes `to` prop
- External links should remain as `<a>` tags

#### Files to Update

1. **`src/components/header.tsx`**: Replace `next-view-transitions` Link
2. **`src/components/footer.tsx`**: Replace `next/link` with TanStack Router Link (for internal links only)
3. **`src/app/page.tsx`**: Replace Link imports
4. **`src/app/posts/page.tsx`**: Replace Link imports

#### External Links

Keep external links as regular `<a>` tags:

```typescript
<a 
  href="https://github.com/sandonl" 
  target="_blank" 
  rel="noopener noreferrer"
>
  GitHub
</a>
```

---

### 9. Route Pages Migration

#### Home Page (`src/routes/index.tsx`)

**Before (`src/app/page.tsx`):**

```typescript
import LetterSwapPingPong from "@/components/letter-swap-ping-pong";
import { Link } from "next-view-transitions";

export default function Home() {
  return (
    <div className="min-h-48 border-b pb-8">
      {/* ... content ... */}
    </div>
  );
}
```

**After (`src/routes/index.tsx`):**

```typescript
import { createFileRoute } from '@tanstack/react-router'
import { Link } from '@tanstack/react-router'
import LetterSwapPingPong from '@/components/letter-swap-ping-pong'

export const Route = createFileRoute('/')({
  component: HomePage
})

function HomePage() {
  return (
    <div className="min-h-48 border-b pb-8">
      {/* ... same content ... */}
    </div>
  )
}
```

#### Posts Listing (`src/routes/posts/index.tsx`)

**Before (`src/app/posts/page.tsx`):**

```typescript
import { Link } from "next-view-transitions";
import { allPosts } from "content-collections";
import { Badge } from "@/components/ui/badge";

export default function BlogOverview() {
  return (
    <div>
      {allPosts.map((post) => (
        <article key={post.slug}>
          {/* ... */}
        </article>
      ))}
    </div>
  );
}
```

**After (`src/routes/posts/index.tsx`):**

```typescript
import { createFileRoute } from '@tanstack/react-router'
import { Link } from '@tanstack/react-router'
import { allPosts } from 'content-collections'
import { Badge } from '@/components/ui/badge'
import LetterSwapPingPong from '@/components/letter-swap-ping-pong'

export const Route = createFileRoute('/posts/')({
  loader: () => {
    return { posts: allPosts }
  },
  component: PostsPage
})

function PostsPage() {
  const { posts } = Route.useLoaderData()
  
  return (
    <div>
      <div className="flex pb-8">
        <LetterSwapPingPong label="Posts" className="text-3xl font-bold" />
      </div>
      <div className="space-y-8">
        {posts.map((post) => (
          <article key={post.slug} className="border-b pb-8">
            {/* ... same content ... */}
          </article>
        ))}
      </div>
    </div>
  )
}
```

#### Post Detail (`src/routes/posts/$slug.tsx`)

**Before (`src/app/posts/[slug]/page.tsx`):**

```typescript
import { allPosts } from "content-collections";
import { notFound } from "next/navigation";

export default async function PostPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const slug = (await params).slug;
  const post = allPosts.find((post) => post.slug === slug);

  if (!post) {
    notFound();
  }

  return (
    <article className="py-6">
      {/* ... */}
    </article>
  );
}
```

**After (`src/routes/posts/$slug.tsx`):**

```typescript
import { createFileRoute, notFound } from '@tanstack/react-router'
import { allPosts } from 'content-collections'

export const Route = createFileRoute('/posts/$slug')({
  loader: ({ params }) => {
    const post = allPosts.find((p) => p.slug === params.slug)
    
    if (!post) {
      throw notFound()
    }
    
    return { post }
  },
  component: PostPage,
  notFoundComponent: () => <div>Post not found</div>
})

function PostPage() {
  const { post } = Route.useLoaderData()
  
  return (
    <article className="py-6">
      <div className="mb-8">
        <h1 className="mb-2 text-3xl font-bold">{post.title}</h1>
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <time dateTime={post.createdAt}>
            {new Date(post.createdAt).toLocaleDateString("en-US", {
              year: "numeric",
              month: "long",
              day: "numeric",
            })}
          </time>
          <div className="flex gap-2">
            {post.tags.map((tag) => (
              <span
                key={tag}
                className="inline-flex items-center rounded-md bg-secondary px-2 py-1 text-xs"
              >
                {tag}
              </span>
            ))}
          </div>
          <div className="text-xs text-muted-foreground"> - {post.author}</div>
        </div>
      </div>
      <div className="mt-8 prose prose-invert prose-headings:scroll-mt-20 text-sm max-w-none">
        <post.mdxContent />
      </div>
    </article>
  )
}
```

**Key Changes:**
- `createFileRoute` with route path
- `loader` function for data fetching (runs on server)
- `Route.useLoaderData()` to access loaded data
- `notFoundComponent` for 404 handling
- No async params - params available directly in loader

---

### 10. Vercel Deployment

#### Vite Config (Already Set)

Ensure `server: { preset: 'vercel' }` is in your `vite.config.ts`:

```typescript
tanstackStart({
  server: {
    preset: 'vercel'
  }
})
```

#### Create `vercel.json` (Optional)

TanStack Start with Vercel preset should work without additional configuration, but you can add:

```json
{
  "buildCommand": "pnpm build",
  "outputDirectory": ".vercel/output"
}
```

#### Environment Variables

No changes needed - Vercel environment variables work the same way.

#### Deployment Process

1. Push to GitHub branch
2. Vercel automatically detects the build command from `package.json`
3. Preview deployment created automatically
4. Merge to main for production deployment

---

## Routing Differences Reference

### File Structure Mapping

```
Next.js App Router          →  TanStack Start
─────────────────────────────────────────────────
src/app/
├── layout.tsx              →  src/routes/__root.tsx
├── page.tsx                →  src/routes/index.tsx
├── posts/
│   ├── page.tsx            →  src/routes/posts/index.tsx
│   └── [slug]/
│       └── page.tsx        →  src/routes/posts/$slug.tsx
└── not-found.tsx           →  notFoundComponent in routes
```

### API Differences

| Feature | Next.js | TanStack Start |
|---------|---------|----------------|
| **Route Definition** | Default export function | `createFileRoute()` with `component` |
| **Data Fetching** | Async component | `loader` function |
| **Params** | `params: Promise<{}>` | `params` in loader |
| **Metadata** | `export const metadata` | `head()` function |
| **Not Found** | `notFound()` from `next/navigation` | `throw notFound()` in loader |
| **Layout** | `children` prop | `<Outlet />` component |
| **Link** | `<Link href="">` | `<Link to="">` |

### Dynamic Routes

| Next.js | TanStack Start | Example |
|---------|----------------|---------|
| `[slug]` | `$slug` | `/posts/[slug]` → `/posts/$slug` |
| `[...slug]` | `$` | `/docs/[...slug]` → `/docs/$` |
| `[[...slug]]` | `_splat` | `/[[...slug]]` → `/_splat` |

---

## Troubleshooting

### Common Issues

#### 1. "Module not found: @tanstack/react-router"

**Cause**: Dependencies not installed or incorrect version.

**Solution**:
```bash
pnpm install
# Verify installation
pnpm list @tanstack/react-router
```

#### 2. "contentCollections is not a function"

**Cause**: Content Collections plugin not imported correctly.

**Solution**: Ensure import in `vite.config.ts`:
```typescript
import contentCollections from '@content-collections/vite'
```

#### 3. Path aliases (@/*) not working

**Cause**: `vite-tsconfig-paths` plugin missing or misconfigured.

**Solution**:
```bash
pnpm add -D vite-tsconfig-paths
```

Add to `vite.config.ts`:
```typescript
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [
    // ... other plugins
    tsconfigPaths()
  ]
})
```

#### 4. Fonts not loading

**Cause**: Fontsource packages not imported or incorrect CSS class.

**Solution**:
1. Verify imports in `__root.tsx`
2. Check Tailwind config has font families defined
3. Use `font-sans` or `font-mono` classes

#### 5. View transitions not working

**Cause**: `defaultViewTransition` not enabled in router.

**Solution**: Add to `src/router.tsx`:
```typescript
createTanStackRouter({
  routeTree,
  defaultViewTransition: true
})
```

#### 6. Build fails with "Cannot find module 'content-collections'"

**Cause**: Content Collections hasn't generated types yet.

**Solution**:
```bash
# Run dev server once to generate types
pnpm dev
# Then build
pnpm build
```

#### 7. Vercel deployment fails

**Cause**: Build command or output directory misconfigured.

**Solution**: Ensure `package.json` has:
```json
{
  "scripts": {
    "build": "vite build"
  }
}
```

And `vite.config.ts` has:
```typescript
tanstackStart({
  server: { preset: 'vercel' }
})
```

---

## Rollback Procedure

If the migration encounters critical issues and needs to be reverted:

### 1. Return to Main Branch

```bash
# Discard all changes on migration branch
git checkout main

# Verify you're on main
git branch --show-current
```

### 2. Delete Migration Branch

```bash
# Delete local branch
git branch -D migrate/tanstack-start

# Delete remote branch (if pushed)
git push origin --delete migrate/tanstack-start
```

### 3. Verify Next.js Still Works

```bash
# Install dependencies
pnpm install

# Start dev server
pnpm dev

# Build for production
pnpm build
```

### 4. Document Issues

If rollback was necessary, document what went wrong:

1. Create an issue in the repository
2. Include error messages and logs
3. Note which step failed
4. Describe attempted solutions

### Important Notes

- **Main branch is never touched** during migration - it remains stable
- **All work happens on `migrate/tanstack-start` branch**
- **No risk to production** - rollback is instant
- **Migration can be retried** after addressing issues

---

## Next Steps After Migration

### Phase 2: Tailwind v4 Upgrade (Optional)

After the TanStack Start migration is stable and deployed, you can optionally upgrade to Tailwind CSS v4:

1. Run upgrade tool: `npx @tailwindcss/upgrade`
2. Replace PostCSS plugin with `@tailwindcss/vite`
3. Update configuration to CSS-based format
4. Test all styling thoroughly

**Recommendation**: Keep this as a separate PR to reduce migration risk.

### Additional Enhancements (Optional)

Once migration is complete, consider:

- **Dynamic metadata for posts**: Add `head()` function to post routes
- **Image optimization**: Implement image handling if needed
- **Error boundaries**: Add error handling for better UX
- **Loading states**: Add suspense boundaries for data loading

---

## Resources

### Official Documentation
- [TanStack Start](https://tanstack.com/start/latest/docs)
- [TanStack Router](https://tanstack.com/router/latest/docs)
- [Vite](https://vitejs.dev/)
- [Content Collections](https://www.content-collections.dev/)

### Community Resources
- [TanStack Discord](https://discord.com/invite/tanstack)
- [TanStack Start Examples](https://github.com/TanStack/router/tree/main/examples)

### Related Guides
- [Migrating from Next.js to TanStack Start](https://tanstack.com/start/latest/docs/framework/react/guide/migrating-from-nextjs)
- [File-based Routing](https://tanstack.com/router/latest/docs/framework/react/guide/file-based-routing)
- [Data Loading](https://tanstack.com/start/latest/docs/framework/react/data-fetching)

---

## Conclusion

This migration maintains all existing functionality while modernizing the tech stack. The process is designed to be safe, reversible, and well-documented. Take your time with each step, verify thoroughly, and don't hesitate to rollback if issues arise.

Good luck with your migration! 🚀
