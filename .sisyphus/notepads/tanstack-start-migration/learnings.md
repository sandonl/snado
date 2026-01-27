# Learnings - TanStack Start Migration

## Conventions & Patterns
(Subagents will append findings here)

## Exhaustive Codebase Exploration - TanStack Start Migration

### 1. PROJECT STRUCTURE & FILE INVENTORY

#### Root Configuration Files
- `package.json` - Dependencies and scripts
- `next.config.ts` - Next.js configuration with MDX and Content Collections
- `tsconfig.json` - TypeScript configuration with path aliases
- `tailwind.config.ts` - Tailwind CSS theme configuration
- `postcss.config.mjs` - PostCSS configuration
- `eslint.config.mjs` - ESLint configuration (flat config format)
- `content-collections.ts` - Content Collections configuration for MDX posts

#### Source Directory Structure
```
src/
├── app/
│   ├── layout.tsx          (Root layout with ViewTransitions wrapper)
│   ├── page.tsx            (Home page)
│   ├── globals.css         (Global styles with CSS variables)
│   ├── favicon.ico
│   └── posts/
│       ├── page.tsx        (Posts listing page)
│       └── [slug]/
│           └── page.tsx    (Dynamic post page)
├── components/
│   ├── header.tsx          (Navigation header)
│   ├── footer.tsx          (Footer with social links)
│   ├── letter-swap-ping-pong.tsx (Animated text component)
│   ├── mdx-components.tsx  (MDX component mapping)
│   └── ui/
│       ├── badge.tsx       (shadcn/ui Badge component)
│       ├── button.tsx      (shadcn/ui Button component)
│       └── quote.tsx       (Custom Quote component)
├── lib/
│   └── utils.ts            (Utility functions - cn() for class merging)
└── posts/
    └── fluency-illusion.mdx (Sample MDX post with frontmatter)
```

### 2. NEXT.JS DEPENDENCIES & IMPORTS

#### Direct Next.js Imports Found
**In `src/app/layout.tsx`:**
- `next/font/google` - Geist font loading
- `next/navigation` - Type imports (Metadata)

**In `src/app/posts/[slug]/page.tsx`:**
- `next/navigation` - notFound() function

**In `src/components/footer.tsx`:**
- `next/link` - Link component (NOT next-view-transitions)

#### Next.js Features Used
- App Router (src/app directory structure)
- Dynamic routes with `[slug]` pattern
- Metadata API (generateMetadata type)
- Font optimization (next/font/google)
- Navigation utilities (notFound)

### 3. NEXT-VIEW-TRANSITIONS USAGE

#### Files Using next-view-transitions
1. **`src/app/layout.tsx`** - Line 5
   - Imports: `ViewTransitions` component
   - Usage: Wraps entire HTML tree for page transitions

2. **`src/app/page.tsx`** - Line 2
   - Imports: `Link` from next-view-transitions
   - Usage: Navigation links with transition support

3. **`src/app/posts/page.tsx`** - Line 1
   - Imports: `Link` from next-view-transitions
   - Usage: Post listing links

4. **`src/components/header.tsx`** - Line 1
   - Imports: `Link` from next-view-transitions
   - Usage: Navigation menu links

#### Inconsistency Found
- `src/components/footer.tsx` uses `next/link` instead of `next-view-transitions`
- This is an inconsistency that should be addressed during migration

### 4. CLIENT COMPONENTS ("use client" DIRECTIVES)

#### Files with "use client"
1. **`src/components/letter-swap-ping-pong.tsx`** - Line 1
   - Reason: Uses React hooks (useState, useAnimate)
   - Dependencies: motion/react, lodash (debounce)

#### Server Components (Implicit)
- `src/app/layout.tsx` - Server component (uses Metadata)
- `src/app/page.tsx` - Server component
- `src/app/posts/page.tsx` - Server component (uses allPosts from content-collections)
- `src/app/posts/[slug]/page.tsx` - Server component (async params handling)
- `src/components/header.tsx` - Server component
- `src/components/footer.tsx` - Server component
- `src/components/ui/badge.tsx` - Server component
- `src/components/ui/button.tsx` - Server component
- `src/components/ui/quote.tsx` - Server component

### 5. CONTENT COLLECTIONS & MDX SETUP

#### Content Collections Configuration
**File:** `content-collections.ts`
- Collection name: `posts`
- Directory: `src/posts`
- Pattern: `**/*.mdx`
- Parser: `frontmatter-only`
- Schema fields:
  - `title` (string)
  - `summary` (string)
  - `createdAt` (string)
  - `author` (string)
  - `tags` (array of strings)
  - `slug` (string)
- Transform: Creates `mdxContent` import for each post

#### MDX Configuration
**File:** `next.config.ts`
- Uses `@next/mdx` with Content Collections
- Remark plugins: `remark-frontmatter`, `remark-mdx-frontmatter`
- Page extensions: `["js", "jsx", "md", "mdx", "ts", "tsx"]`

#### MDX Component Mapping
**File:** `src/mdx-components.tsx`
- Currently minimal - just re-exports components parameter
- Used in MDX files for custom component rendering

#### MDX Post Example
**File:** `src/posts/fluency-illusion.mdx`
- Frontmatter format: YAML
- Imports custom components: Button, Quote
- Uses standard markdown with custom component integration

### 6. STYLING & THEMING

#### CSS Architecture
**Global Styles:** `src/app/globals.css`
- Tailwind directives: @tailwind base, components, utilities
- CSS custom properties for theming (HSL values)
- Dark mode support with `.dark` class selector
- Color variables: background, foreground, card, primary, secondary, muted, accent, destructive, border, input, ring, chart colors
- Border radius variable: `--radius`

#### Tailwind Configuration
**File:** `tailwind.config.ts`
- Dark mode: class-based
- Content paths: pages, components, app directories
- Theme extensions: Custom color palette using CSS variables
- Plugins: `tailwindcss-animate`, `@tailwindcss/typography`

#### PostCSS Configuration
**File:** `postcss.config.mjs`
- Simple setup with tailwindcss plugin only

### 7. DEPENDENCIES ANALYSIS

#### Production Dependencies
- **Framework:** next@15.5.7, react@19.0.1, react-dom@19.0.1
- **Routing/Transitions:** next-view-transitions@0.1.0
- **MDX:** @mdx-js/loader@3.1.0, @mdx-js/react@3.1.0, @next/mdx@15.1.2
- **UI Components:** @radix-ui/react-slot@1.1.1, lucide-react@0.469.0
- **Styling:** tailwindcss, tailwind-merge@2.5.5, tailwindcss-animate@1.0.7, class-variance-authority@0.7.1
- **Animation:** motion@11.15.0
- **Utilities:** clsx@2.1.1, lodash@4.17.21
- **Analytics:** @vercel/analytics@1.5.0

#### Dev Dependencies
- **Content Collections:** @content-collections/core@0.8.0, @content-collections/markdown@0.1.3, @content-collections/mdx@0.2.0, @content-collections/next@0.2.4
- **Linting:** eslint@9, eslint-config-next@15.1.2, @eslint/eslintrc@3
- **Styling:** @tailwindcss/typography@0.5.15
- **Type Checking:** typescript@5, @types/node@20, @types/react@19, @types/react-dom@19, @types/lodash@4.17.13, @types/mdx@2.0.13
- **Markdown:** remark-frontmatter@5.0.0, remark-mdx-frontmatter@5.0.0
- **PostCSS:** postcss@8

### 8. ROUTING STRUCTURE

#### Current Routes
- `/` - Home page (src/app/page.tsx)
- `/posts` - Posts listing (src/app/posts/page.tsx)
- `/posts/[slug]` - Dynamic post page (src/app/posts/[slug]/page.tsx)

#### Dynamic Route Pattern
- Uses async params with Promise<{ slug: string }>
- Implements notFound() for missing posts
- Renders MDX content via post.mdxContent component

### 9. TYPESCRIPT PATH ALIASES

**File:** `tsconfig.json`
- `@/*` → `./src/*`
- `content-collections` → `./.content-collections/generated`

### 10. ESLINT CONFIGURATION

**File:** `eslint.config.mjs`
- Uses flat config format (ESLint 9+)
- Extends: `next/core-web-vitals`, `next/typescript`
- No custom rules defined

### 11. BUILD SCRIPTS

**From package.json:**
- `dev` - `next dev`
- `build` - `next build`
- `start` - `next start`
- `lint` - `next lint`
- `type-check` - `tsc --noEmit`

### 12. MIGRATION IMPACT SUMMARY

#### Critical Changes Required
1. **Routing System** - App Router → TanStack Start routing
2. **Link Components** - next-view-transitions/Link → TanStack Start Link
3. **Layout System** - Next.js layout.tsx → TanStack Start layout structure
4. **Metadata** - Next.js Metadata API → TanStack Start metadata handling
5. **Font Loading** - next/font/google → Alternative font loading strategy
6. **Navigation Utilities** - next/navigation (notFound) → TanStack Start equivalents

#### Components to Preserve
- All UI components (badge, button, quote) - framework agnostic
- letter-swap-ping-pong animation component - uses motion/react
- MDX component mapping - can be adapted
- Styling system (Tailwind, CSS variables) - fully portable

#### Configuration to Adapt
- content-collections.ts - May need adjustments for TanStack Start
- tailwind.config.ts - Fully portable
- postcss.config.mjs - Fully portable
- tsconfig.json - Path aliases may need adjustment

#### Dependencies to Replace/Adapt
- Remove: next, @next/mdx, next-view-transitions
- Add: TanStack Start and related packages
- Keep: All UI, animation, styling, and utility libraries
- Evaluate: Content Collections compatibility with TanStack Start

### 13. KEY OBSERVATIONS

1. **Minimal Next.js-Specific Code** - Most of the codebase is framework-agnostic
2. **Heavy Use of Animations** - motion/react is core to the design
3. **Content-Driven** - MDX posts are central to the site
4. **Consistent Styling** - Well-organized Tailwind + CSS variables
5. **Type-Safe** - Full TypeScript with strict mode
6. **Link Inconsistency** - footer.tsx uses next/link instead of next-view-transitions
7. **Server-First Architecture** - Most components are server components
8. **Single Client Component** - Only letter-swap-ping-pong uses "use client"


## Vite Configuration Implementation Learnings

### Plugin Order is Critical
- **contentCollections() MUST be first** - This is non-negotiable for proper MDX/content integration
- Plugin order: contentCollections → tanstackStart → viteReact → mdx → tsconfigPaths
- Incorrect order will cause build failures and content collection issues

### TanStack Start Plugin Configuration
- **Simplified plugin config**: tanstackStart() with no options works for basic setup
- Server preset and prerender config belong in app.config.ts, NOT in vite plugin
- The plugin handles routing, SSR, and build optimization automatically

### TypeScript Configuration for Vite
- **"types": ["vite/client"]** is essential for proper IDE support and type checking
- Removing Next.js plugin eliminates all Next.js-specific type definitions
- Path aliases remain unchanged and fully compatible with Vite

### Content Collections with Vite
- **@content-collections/vite** is the correct adapter (not @content-collections/next)
- Must be placed first in plugin array for proper initialization
- Works seamlessly with MDX and TanStack Start

### Migration Patterns
- Configuration split: vite.config.ts (build) + app.config.ts (app-specific)
- This separation allows cleaner configuration and better maintainability
- PostCSS config remains unchanged (needed for Tailwind v3)

### Verification Strategy
- Always verify Vite installation after configuration changes
- Check plugin order in vite.config.ts before proceeding to next phase
- LSP errors in source files are expected until dependencies are installed
