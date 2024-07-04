import { defineConfig } from "histoire";
import { HstVue } from "@histoire/plugin-vue";

export default defineConfig({
  plugins: [HstVue()],
  setupFile: "./histoire.setup.ts",
  sourceDirs: [
    {
      path: "./src",
    },
  ],
  vite: {
    server: {
      port: 6180,
    },
    base: "/paybuddy/histoire/",
  },
});
