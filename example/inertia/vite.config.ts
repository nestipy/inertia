import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import nestipyVite from "./nestipy.inertia";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        react(),
        nestipyVite({
            entry: './src/main.tsx',
            ssr: './src/ssr.tsx'
        }),
    ],
})
