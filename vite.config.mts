import { defineConfig } from 'vite'
import { tanstackStart } from '@tanstack/react-start/plugin/vite'
import viteReact from '@vitejs/plugin-react'
import contentCollections from '@content-collections/vite'
import mdx from '@mdx-js/rollup'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [
    contentCollections(),
    tanstackStart(),
    viteReact(),
    mdx(),
    tsconfigPaths()
  ]
})
