# TanStack Start Migration Plan

## Context

### Original Request
Migrate the current Next.js 15 blog/portfolio site to TanStack Start. Create a separate branch for testing. Write comprehensive migration documentation BEFORE attempting migration. Functionality must remain the same.

### Interview Summary
**Key Discussions**:
- **Tailwind Version**: User chose to upgrade to Tailwind v4 (better Vite integration)
- **View Transitions**: Use TanStack Router's native view transition support
- **Deployment**: Continue deploying to Vercel (keep Vercel Analytics)
- **Documentation**: Comprehensive guide with full explanations

**Research Findings**:
- Content Collections works with both Next.js AND TanStack Start (same library, different adapter)
- MDX content files (`/src/posts/*.mdx`) don't need changes
- shadcn/ui components are framework-agnostic (should work unchanged)
- Motion library is framework-agnostic (should work unchanged)
- TanStack Start is in RC stage - API stable but version should be pinned

### Metis Review
**Identified Gaps** (addressed):
1. **Font Loading**: `next/font/google` has no TanStack equivalent → Use Fontsource packages
2. **Tailwind v4 Risk**: Bundling v4 upgrade with framework migration increases risk → Two-phase approach
3. **Version Pinning**: TanStack Start is RC, need exact version → Pin to specific version
4. **Not Found Handling**: Need `notFoundComponent` for invalid slugs → Include in routing setup
5. **Dynamic Metadata**: Current site lacks dynamic meta for posts → Document as known limitation (OUT OF SCOPE)
6. **Build Mode**: Need SSG with prerendering → Configure `prerender: { enabled: true }`

---

## Work Objectives

### Core Objective
Migrate the snado blog/portfolio from Next.js 15 to TanStack Start while maintaining identical functionality, and create comprehensive documentation to guide the migration process.

### Concrete Deliverables
- Migration branch: `migrate/tanstack-start`
- Comprehensive migration documentation: `docs/TANSTACK-START-MIGRATION.md`
- Working TanStack Start application with all current routes
- Vercel deployment configuration

### Definition of Done
- [ ] `pnpm dev` starts TanStack Start dev server without errors
- [ ] `pnpm build` completes without errors
- [ ] All routes render identically: `/`, `/posts`, `/posts/[slug]`
- [ ] MDX content renders with Quote component
- [ ] LetterSwapPingPong animation works
- [ ] View transitions work between pages
- [ ] Vercel preview deployment succeeds

### Must Have
- All current routes functional: `/`, `/posts`, `/posts/[slug]`
- MDX blog posts render correctly with all components
- Tailwind CSS styling preserved (colors, spacing, typography)
- View transitions between pages
- Vercel Analytics tracking
- Geist fonts (via Fontsource)

### Must NOT Have (Guardrails)
- DO NOT modify MDX content files (`src/posts/*.mdx`)
- DO NOT change shadcn/ui component implementations
- DO NOT add features not in the current site
- DO NOT change Content Collections schema
- DO NOT migrate Tailwind v4 in Phase 1 (separate concern - defer to Phase 2)
- DO NOT remove Next.js files until TanStack version verified working
- DO NOT use dynamic routes where static routes exist

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: NO (no test framework)
- **User wants tests**: Manual-only (visual verification for static site)
- **Framework**: None

### Manual QA Approach
Each TODO includes detailed verification procedures using:
- **Playwright browser automation** for visual verification
- **Terminal commands** for build/dev verification
- **Side-by-side comparison** with current Next.js site

**Evidence Required:**
- Commands run with actual output
- Screenshots for visual verification
- Console checked for errors

---

## Task Flow

```
Task 0 (Branch) 
    ↓
Task 1 (Documentation) 
    ↓
Task 2 (Dependencies) → Task 3 (Vite Config) → Task 4 (Root Layout)
                                                    ↓
                                            Task 5 (Routes)
                                                    ↓
                                            Task 6 (Component Updates)
                                                    ↓
                                            Task 7 (View Transitions)
                                                    ↓
                                            Task 8 (Vercel Config)
                                                    ↓
                                            Task 9 (Final Verification)
                                                    ↓
                                            Task 10 (Phase 2: Tailwind v4) [Optional]
```

## Parallelization

| Group | Tasks | Reason |
|-------|-------|--------|
| Sequential | All | Each task depends on previous (migration is linear) |

| Task | Depends On | Reason |
|------|------------|--------|
| 1 | 0 | Docs should be on branch |
| 2 | 1 | Dependencies need docs reference |
| 3 | 2 | Vite config needs dependencies installed |
| 4 | 3 | Root layout needs Vite working |
| 5 | 4 | Routes need root layout |
| 6 | 5 | Components need routes to test in |
| 7 | 6 | View transitions need working navigation |
| 8 | 7 | Deploy needs complete app |
| 9 | 8 | Verification needs deployment |
| 10 | 9 | Tailwind v4 is optional Phase 2 |

---

## TODOs

### - [ ] 0. Create Migration Branch

**What to do**:
- Create new branch `migrate/tanstack-start` from main
- Push branch to remote for backup

**Must NOT do**:
- Do not delete any files yet
- Do not merge this branch until all verification passes

**Parallelizable**: NO (first task)

**References**:
- Current branch: `main`

**Acceptance Criteria**:

**Manual Execution Verification:**
- [ ] Command: `git checkout -b migrate/tanstack-start`
  - Expected: Branch created and checked out
- [ ] Command: `git push -u origin migrate/tanstack-start`
  - Expected: Branch pushed to remote
- [ ] Verify: `git branch --show-current` → `migrate/tanstack-start`

**Commit**: YES
- Message: `chore: create migration branch for tanstack-start`
- Files: none (branch only)

---

### - [ ] 1. Write Comprehensive Migration Documentation

**What to do**:
- Create `docs/TANSTACK-START-MIGRATION.md`
- Document the full migration process with:
  - Overview and rationale
  - Prerequisites
  - Step-by-step guide with code examples
  - Routing differences (Next.js vs TanStack Start)
  - Content Collections adapter change
  - Metadata handling differences
  - Font loading approach
  - View transitions setup
  - Vercel deployment configuration
  - Troubleshooting section
  - Rollback procedure

**Must NOT do**:
- Do not include Tailwind v4 migration (that's Phase 2, separate doc)
- Do not include features not being implemented

**Parallelizable**: NO (depends on Task 0)

**References**:

**Pattern References** (existing code to follow):
- `src/app/layout.tsx` - Current root layout structure to document transformation
- `src/app/page.tsx` - Home page pattern to document
- `src/app/posts/page.tsx` - Posts listing pattern to document
- `src/app/posts/[slug]/page.tsx` - Dynamic route pattern to document
- `content-collections.ts` - Content Collections config to document adapter change

**Documentation References** (official sources):
- TanStack Start docs: `https://tanstack.com/start/latest/docs`
- TanStack Router docs: `https://tanstack.com/router/latest/docs`
- Content Collections Vite setup: `https://www.content-collections.dev/docs/quickstart/tanstack-start`
- Fontsource: `https://fontsource.org/fonts/geist-sans`

**Acceptance Criteria**:

**Manual Execution Verification:**
- [ ] File exists: `docs/TANSTACK-START-MIGRATION.md`
- [ ] Document contains: Overview section
- [ ] Document contains: Step-by-step guide with code examples
- [ ] Document contains: Routing differences table
- [ ] Document contains: Rollback procedure
- [ ] Using Playwright browser: Open file in VS Code or viewer, verify readable

**Commit**: YES
- Message: `docs: add comprehensive tanstack start migration guide`
- Files: `docs/TANSTACK-START-MIGRATION.md`

---

### - [ ] 2. Update Dependencies

**What to do**:
- Remove Next.js dependencies:
  - `next`, `@next/mdx`
  - `next-view-transitions`
  - `@content-collections/next`
- Add TanStack Start dependencies:
  - `@tanstack/react-start` (pin exact version)
  - `@tanstack/react-router`
  - `@tanstack/react-router-devtools`
- Add Vite dependencies:
  - `vite`
  - `@vitejs/plugin-react`
  - `vite-tsconfig-paths`
- Update Content Collections:
  - `@content-collections/vite`
- Add font packages:
  - `@fontsource/geist-sans`
  - `@fontsource/geist-mono`
- Add MDX support:
  - `@mdx-js/rollup`
- Update package.json scripts:
  - `"dev": "vite"`
  - `"build": "vite build"`
  - `"preview": "vite preview"`

**Must NOT do**:
- Do not remove Tailwind v3 dependencies
- Do not add Tailwind v4 dependencies yet
- Do not remove PostCSS config

**Parallelizable**: NO (depends on Task 1)

**References**:

**Pattern References**:
- `package.json` - Current dependencies to modify

**Documentation References**:
- TanStack Start installation: `https://tanstack.com/start/latest/docs/framework/react/quick-start`
- Content Collections Vite: `https://www.content-collections.dev/docs/adapters/vite`

**Acceptance Criteria**:

**Manual Execution Verification:**
- [ ] Command: `pnpm remove next @next/mdx next-view-transitions @content-collections/next`
  - Expected: Packages removed
- [ ] Command: `pnpm add @tanstack/react-start@1.x.x @tanstack/react-router @tanstack/react-router-devtools` (pin exact version)
  - Expected: Packages installed
- [ ] Command: `pnpm add -D vite @vitejs/plugin-react vite-tsconfig-paths @content-collections/vite @mdx-js/rollup`
  - Expected: Dev packages installed
- [ ] Command: `pnpm add @fontsource/geist-sans @fontsource/geist-mono`
  - Expected: Font packages installed
- [ ] Verify `package.json` has updated scripts section
- [ ] Command: `pnpm install` → No errors

**Commit**: YES
- Message: `chore: swap next.js dependencies for tanstack start`
- Files: `package.json`, `pnpm-lock.yaml`

---

### - [ ] 3. Create Vite Configuration

**What to do**:
- Create `vite.config.ts` with:
  - TanStack Start plugin
  - React plugin
  - Content Collections plugin (MUST be first!)
  - vite-tsconfig-paths for path aliases
  - MDX rollup plugin
  - Tailwind v3 via PostCSS (existing config)
  - Server preset for Vercel: `server: { preset: 'vercel' }`
  - Prerender enabled: `prerender: { enabled: true }`
- Create `app.config.ts` for TanStack Start:
  - Define routes directory
  - Configure prerendering
- Update `tsconfig.json`:
  - Update module resolution for Vite
  - Add Vite types
- Delete `next.config.ts` (no longer needed)

**Must NOT do**:
- Do not add `@tailwindcss/vite` (that's Tailwind v4)
- Do not remove `postcss.config.mjs` (needed for Tailwind v3)

**Parallelizable**: NO (depends on Task 2)

**References**:

**Pattern References**:
- `next.config.ts` - Current config to reference for MDX setup
- `content-collections.ts` - Content Collections config (stays mostly same)
- `tsconfig.json` - Current TypeScript config to update
- `postcss.config.mjs` - Keep for Tailwind v3

**Documentation References**:
- TanStack Start Vite config: `https://tanstack.com/start/latest/docs/framework/react/quick-start`
- Content Collections Vite: `https://www.content-collections.dev/docs/adapters/vite`
- Vercel preset: `https://tanstack.com/start/latest/docs/framework/react/hosting`

**Acceptance Criteria**:

**Manual Execution Verification:**
- [ ] File exists: `vite.config.ts`
- [ ] File contains: `@tanstack/react-start/plugin/vite`
- [ ] File contains: `contentCollections()` as first plugin
- [ ] File contains: `server: { preset: 'vercel' }`
- [ ] File exists: `app.config.ts`
- [ ] `next.config.ts` deleted
- [ ] Command: `pnpm vite --version` → Shows Vite version

**Commit**: YES
- Message: `feat: add vite and tanstack start configuration`
- Files: `vite.config.ts`, `app.config.ts`, `tsconfig.json`
- Pre-commit: N/A (app not runnable yet)

---

### - [ ] 4. Create Root Layout (`__root.tsx`)

**What to do**:
- Create `src/routes/__root.tsx`:
  - Import and configure `createRootRoute`
  - Add `head()` function with metadata (title, description, charset, viewport)
  - Add `<HeadContent />` in head
  - Add `<Scripts />` before closing body
  - Import and render `<Header />` and `<Footer />` components
  - Add `<Outlet />` for child routes
  - Import Geist fonts from Fontsource
  - Import global CSS (`globals.css`)
  - Add Vercel Analytics component
- Create `src/routes/index.tsx` as placeholder (empty component)
- Create entry files:
  - `src/client.tsx` - Client entry
  - `src/server.tsx` - Server entry (for SSR)
  - `src/router.tsx` - Router configuration

**Must NOT do**:
- Do not delete `src/app/layout.tsx` yet (keep for reference)
- Do not change Header or Footer components

**Parallelizable**: NO (depends on Task 3)

**References**:

**Pattern References**:
- `src/app/layout.tsx:1-50` - Current root layout structure (metadata, providers, wrapper)
- `src/components/header.tsx` - Header component to import (no changes needed)
- `src/components/footer.tsx` - Footer component to import (no changes needed)
- `src/app/globals.css` - Global styles to import (move to src/styles/)

**Documentation References**:
- TanStack Start root layout: `https://tanstack.com/start/latest/docs/framework/react/guide/routing#root-layout`
- Head management: `https://tanstack.com/start/latest/docs/framework/react/guide/head`
- Fontsource usage: `https://fontsource.org/docs/getting-started/usage`

**Acceptance Criteria**:

**Manual Execution Verification:**
- [ ] File exists: `src/routes/__root.tsx`
- [ ] File contains: `createRootRoute`, `HeadContent`, `Scripts`, `Outlet`
- [ ] File contains: Font imports from `@fontsource/geist-sans`, `@fontsource/geist-mono`
- [ ] File contains: Header and Footer components
- [ ] File exists: `src/client.tsx`, `src/server.tsx`, `src/router.tsx`
- [ ] Command: `pnpm dev` → Server starts (may have errors for missing routes)

**Commit**: YES
- Message: `feat: create tanstack start root layout and entry files`
- Files: `src/routes/__root.tsx`, `src/routes/index.tsx`, `src/client.tsx`, `src/server.tsx`, `src/router.tsx`

---

### - [ ] 5. Migrate Routes

**What to do**:
- Create `src/routes/index.tsx` (Home page):
  - Port content from `src/app/page.tsx`
  - Use `createFileRoute('/')`
  - Import and use existing components
- Create `src/routes/posts/index.tsx` (Posts listing):
  - Port content from `src/app/posts/page.tsx`
  - Use `createFileRoute('/posts')`
  - Add loader to fetch `allPosts` from Content Collections
  - Use `Route.useLoaderData()` to access posts
- Create `src/routes/posts/$slug.tsx` (Post detail):
  - Port content from `src/app/posts/[slug]/page.tsx`
  - Use `createFileRoute('/posts/$slug')`
  - Add loader to fetch single post by slug
  - Add `notFoundComponent` for invalid slugs
  - Render MDX content using Content Collections pattern

**Must NOT do**:
- Do not add dynamic metadata (out of scope - current site doesn't have it)
- Do not change the MDX rendering pattern
- Do not modify Content Collections schema

**Parallelizable**: NO (depends on Task 4)

**References**:

**Pattern References**:
- `src/app/page.tsx:1-40` - Home page content to port
- `src/app/posts/page.tsx:1-50` - Posts listing logic to port (mapping over allPosts)
- `src/app/posts/[slug]/page.tsx:1-80` - Post detail logic to port (finding post, MDX rendering)
- `content-collections.ts` - Content Collections config (allPosts structure)
- `src/mdx-components.tsx` - MDX components mapping (Quote, Button, etc.)

**Documentation References**:
- File-based routing: `https://tanstack.com/router/latest/docs/framework/react/guide/file-based-routing`
- Route loaders: `https://tanstack.com/start/latest/docs/framework/react/data-fetching`
- Dynamic routes: `https://tanstack.com/router/latest/docs/framework/react/guide/route-params`

**Acceptance Criteria**:

**Manual Execution Verification:**
- [ ] File exists: `src/routes/index.tsx`, `src/routes/posts/index.tsx`, `src/routes/posts/$slug.tsx`
- [ ] Using Playwright browser:
  - Navigate to `http://localhost:3000/`
  - Verify: Home page content renders (About section)
  - Navigate to `http://localhost:3000/posts`
  - Verify: Posts list renders with all blog posts
  - Navigate to `http://localhost:3000/posts/fluency-illusion`
  - Verify: Post content renders, Quote component works
  - Navigate to `http://localhost:3000/posts/invalid-slug`
  - Verify: Not found handling works

**Commit**: YES
- Message: `feat: migrate all routes to tanstack start file-based routing`
- Files: `src/routes/index.tsx`, `src/routes/posts/index.tsx`, `src/routes/posts/$slug.tsx`

---

### - [ ] 6. Update Component Imports

**What to do**:
- Update `src/components/header.tsx`:
  - Replace `Link` from `next-view-transitions` with `Link` from `@tanstack/react-router`
  - Update Link props if needed (href → to)
- Update `src/components/footer.tsx`:
  - Replace `Link` from `next/link` with `Link` from `@tanstack/react-router`
  - External links stay as `<a>` tags
- Update `src/mdx-components.tsx`:
  - Replace any Next.js specific imports
  - Verify MDX component mapping works

**Must NOT do**:
- Do not change component styling
- Do not change component behavior
- Do not refactor component structure

**Parallelizable**: NO (depends on Task 5)

**References**:

**Pattern References**:
- `src/components/header.tsx:1-30` - Current header with navigation links
- `src/components/footer.tsx:1-40` - Current footer with social links
- `src/mdx-components.tsx:1-20` - MDX component mapping

**Documentation References**:
- TanStack Router Link: `https://tanstack.com/router/latest/docs/framework/react/api/router/LinkComponent`

**Acceptance Criteria**:

**Manual Execution Verification:**
- [ ] No imports from `next/link` or `next-view-transitions` remain
- [ ] Using Playwright browser:
  - Navigate to `http://localhost:3000/`
  - Click "Posts" in header
  - Verify: Navigates to `/posts`
  - Click site title/logo
  - Verify: Navigates to `/`
  - Scroll to footer
  - Click GitHub/Twitter links
  - Verify: Opens in new tab (external links)

**Commit**: YES
- Message: `refactor: update link imports to tanstack router`
- Files: `src/components/header.tsx`, `src/components/footer.tsx`, `src/mdx-components.tsx`

---

### - [ ] 7. Configure View Transitions

**What to do**:
- Enable view transitions in router config (`src/router.tsx`):
  - Add `defaultViewTransition: true` to router options
- Add view transition CSS:
  - Add `view-transition-name` to main content area
  - Ensure smooth page transitions

**Must NOT do**:
- Do not add custom transition animations (match current behavior)
- Do not add transition to header/footer (they should be stable)

**Parallelizable**: NO (depends on Task 6)

**References**:

**Pattern References**:
- Current site uses `next-view-transitions` - observe current transition effect

**Documentation References**:
- TanStack Router view transitions: `https://tanstack.com/router/latest/docs/framework/react/guide/view-transitions`

**Acceptance Criteria**:

**Manual Execution Verification:**
- [ ] Using Playwright browser:
  - Navigate from `/` to `/posts`
  - Verify: Smooth crossfade transition (not instant jump)
  - Navigate from `/posts` to `/posts/fluency-illusion`
  - Verify: Smooth transition
  - Use browser back button
  - Verify: Smooth reverse transition
- [ ] Header and footer remain stable during transitions

**Commit**: YES
- Message: `feat: enable view transitions in tanstack router`
- Files: `src/router.tsx`, `src/app/globals.css` (if CSS changes needed)

---

### - [ ] 8. Configure Vercel Deployment

**What to do**:
- Create `vercel.json` (if needed for TanStack Start):
  - Configure build command
  - Configure output directory
- Verify `server: { preset: 'vercel' }` in Vite config
- Update `package.json` scripts for Vercel:
  - Ensure `build` command works for Vercel
- Test production build locally:
  - `pnpm build`
  - `pnpm preview`

**Must NOT do**:
- Do not change Vercel Analytics configuration
- Do not add additional Vercel features

**Parallelizable**: NO (depends on Task 7)

**References**:

**Pattern References**:
- Current site deploys to Vercel (no special config visible)

**Documentation References**:
- TanStack Start Vercel hosting: `https://tanstack.com/start/latest/docs/framework/react/hosting#vercel`

**Acceptance Criteria**:

**Manual Execution Verification:**
- [ ] Command: `pnpm build` → Completes without errors
- [ ] Command: `pnpm preview` → Server starts
- [ ] Using Playwright browser at preview URL:
  - All routes work
  - Styling intact
  - Transitions work
- [ ] Push to branch triggers Vercel preview deployment
- [ ] Vercel preview URL works

**Commit**: YES
- Message: `chore: configure vercel deployment for tanstack start`
- Files: `vercel.json` (if needed), `package.json`

---

### - [ ] 9. Final Verification and Cleanup

**What to do**:
- Delete old Next.js files:
  - `src/app/` directory (entire App Router structure)
  - `next.config.ts` (already deleted in Task 3)
  - `next-env.d.ts`
- Verify all functionality one final time
- Run type checking: `pnpm type-check`
- Check Vercel Analytics dashboard for events
- Compare side-by-side with production Next.js site

**Must NOT do**:
- Do not delete if any functionality is broken
- Do not merge to main until all verification passes

**Parallelizable**: NO (depends on Task 8)

**References**:

**Pattern References**:
- Current production site for comparison

**Acceptance Criteria**:

**Manual Execution Verification:**
- [ ] Command: `pnpm type-check` → No type errors
- [ ] Command: `pnpm dev` → Starts without console errors
- [ ] Using Playwright browser - full site walkthrough:
  - [ ] `/` - Home page renders, LetterSwapPingPong animation works
  - [ ] `/posts` - All posts listed with correct dates and tags
  - [ ] `/posts/fluency-illusion` - Post renders, Quote component styled correctly
  - [ ] Navigation works in all directions
  - [ ] View transitions smooth
  - [ ] Fonts render correctly (Geist Sans, Geist Mono)
  - [ ] Dark theme colors correct
  - [ ] Footer links work
- [ ] No Next.js files remain in `src/app/`
- [ ] Vercel preview shows Analytics events

**Commit**: YES
- Message: `chore: remove legacy next.js files and complete migration`
- Files: Deleted `src/app/`, `next-env.d.ts`

---

### - [ ] 10. Phase 2: Tailwind v4 Upgrade (OPTIONAL - Separate PR)

**What to do**:
- Run Tailwind upgrade tool: `npx @tailwindcss/upgrade`
- Replace PostCSS Tailwind with Vite plugin:
  - Remove `postcss.config.mjs`
  - Add `@tailwindcss/vite` to `vite.config.ts`
- Update `tailwind.config.ts` → CSS-based config
- Verify all styles still work

**Must NOT do**:
- Do not include in main migration PR
- Only proceed after Phase 1 is stable and merged

**Parallelizable**: NO (separate phase)

**References**:

**Documentation References**:
- Tailwind v4 upgrade: `https://tailwindcss.com/docs/upgrade-guide`
- Tailwind Vite plugin: `https://tailwindcss.com/docs/installation/vite`

**Acceptance Criteria**:

**Manual Execution Verification:**
- [ ] Command: `npx @tailwindcss/upgrade` → Completes
- [ ] Command: `pnpm build` → No errors
- [ ] Using Playwright browser:
  - All pages render with correct styling
  - Dark theme works
  - Typography classes work
  - Animations work
- [ ] Side-by-side comparison shows no visual differences

**Commit**: YES (separate PR)
- Message: `chore: upgrade to tailwind css v4`
- Files: `vite.config.ts`, `src/app/globals.css`, deleted `postcss.config.mjs`, deleted `tailwind.config.ts`

---

## Commit Strategy

| After Task | Message | Key Files | Verification |
|------------|---------|-----------|--------------|
| 0 | `chore: create migration branch for tanstack-start` | branch only | `git branch` |
| 1 | `docs: add comprehensive tanstack start migration guide` | `docs/TANSTACK-START-MIGRATION.md` | file exists |
| 2 | `chore: swap next.js dependencies for tanstack start` | `package.json` | `pnpm install` |
| 3 | `feat: add vite and tanstack start configuration` | `vite.config.ts`, `app.config.ts` | `pnpm vite --version` |
| 4 | `feat: create tanstack start root layout and entry files` | `src/routes/__root.tsx`, entry files | `pnpm dev` starts |
| 5 | `feat: migrate all routes to tanstack start file-based routing` | `src/routes/*.tsx` | all routes render |
| 6 | `refactor: update link imports to tanstack router` | `src/components/*.tsx` | navigation works |
| 7 | `feat: enable view transitions in tanstack router` | `src/router.tsx` | transitions smooth |
| 8 | `chore: configure vercel deployment for tanstack start` | `vercel.json` | preview deploys |
| 9 | `chore: remove legacy next.js files and complete migration` | delete `src/app/` | clean build |
| 10 | `chore: upgrade to tailwind css v4` (separate PR) | Tailwind files | styles work |

---

## Success Criteria

### Verification Commands
```bash
# Development
pnpm dev                    # Expected: Server starts at localhost:3000

# Type checking
pnpm type-check            # Expected: No errors

# Production build
pnpm build                 # Expected: Build completes successfully

# Preview production
pnpm preview               # Expected: Preview server starts
```

### Final Checklist
- [ ] All "Must Have" features present and working
- [ ] All "Must NOT Have" guardrails respected
- [ ] No Next.js dependencies remain in package.json
- [ ] No Next.js files remain in src/app/
- [ ] Vercel preview deployment successful
- [ ] Vercel Analytics receiving events
- [ ] Visual comparison with production site shows no regressions
- [ ] Migration documentation complete and accurate

---

## Rollback Procedure

If migration fails and needs rollback:

```bash
# Discard all changes and return to main
git checkout main

# Delete the migration branch locally
git branch -D migrate/tanstack-start

# Delete from remote (if pushed)
git push origin --delete migrate/tanstack-start
```

The main branch remains untouched throughout migration. No risk to production.
