import { PluginOption } from "vite";

type Input = {
    entry: string,
    ssr?: string,
    manifest?: string
}
type NestipyPlugin = (options: Input) => PluginOption
const nestipyVite: NestipyPlugin = ({entry, ssr, manifest = "manifest.json"}) => {
    return {
        name: "nestipy-vite-plugin",
        config: (config, env) => {
            return {
                ...config,
                build: {
                    manifest: env.isSsrBuild ? false: manifest,
                    outDir: env.isSsrBuild ? "dist/ssr" : "dist",
                    rollupOptions: {
                        input: env.isSsrBuild && ssr ? ssr : entry,
                    },
                },
                ssr: {
                    noExternal: ['@inertiajs/server']
                }
            }
        }
    }
}

export default nestipyVite
