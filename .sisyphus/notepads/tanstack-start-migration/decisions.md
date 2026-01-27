# Architectural Decisions - TanStack Start Migration

## Key Decisions Made
- **Two-phase approach**: Framework migration (Phase 1) separate from Tailwind v4 (Phase 2)
- **Fontsource for fonts**: Replace `next/font/google` with `@fontsource/geist-sans` and `@fontsource/geist-mono`
- **SSG mode**: Using `prerender: { enabled: true }` for static site generation
- **Content Collections Vite adapter**: `@content-collections/vite` instead of `@content-collections/next`

(Subagents will append additional decisions here)

## Vite Configuration Files Created

### vite.config.ts
- **Plugin order (CRITICAL)**: contentCollections() → tanstackStart() → viteReact() → mdx() → tsconfigPaths()
- **contentCollections() MUST be first** - required for proper MDX/content integration
- **tanstackStart()** - simplified config, no srcDirectory/router/server/prerender options in plugin
- **viteReact()** - standard React plugin
- **mdx()** - @mdx-js/rollup for MDX support
- **tsconfigPaths()** - resolves TypeScript path aliases

### app.config.ts
- **server.preset: 'vercel'** - Vercel deployment configuration
- **prerender.enabled: true** - Static site generation enabled
- **prerender.routes** - Explicitly defined routes: '/', '/posts'
- Uses `@tanstack/react-start/config` for type-safe configuration

### tsconfig.json Updates
- **Removed**: `plugins: [{ "name": "next" }]` - Next.js plugin no longer needed
- **Added**: `"types": ["vite/client"]` - Vite client types for proper IDE support
- **Updated include**: Removed `next-env.d.ts` and `.next/types/**/*.ts` references
- **Kept**: Path aliases (@/*, content-collections) unchanged for compatibility

### Files Deleted
- **next.config.ts** - Removed, replaced by vite.config.ts and app.config.ts

### Verification
- ✅ Vite installed: vite/7.3.1 darwin-arm64 node-v25.2.1
- ✅ All configuration files created successfully
- ✅ No breaking changes to existing source code
