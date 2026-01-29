import { defineConfig } from 'vite'
import { tanstackStart } from '@tanstack/react-start/plugin/vite'
import viteReact from '@vitejs/plugin-react'
import contentCollections from '@content-collections/vite'
import tsconfigPaths from 'vite-tsconfig-paths'
import { nitro } from 'nitro/vite'

export default defineConfig({
  plugins: [
    contentCollections(),
    tsconfigPaths(),
    tanstackStart(),
    nitro(),
    viteReact()
  ]
})
