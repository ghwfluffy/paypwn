import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  base: "/paybuddy/",
  plugins: [vue()],
  /*dev*/server: {
    port: 8180,
    watch: {
      usePolling: true,
    },
  },
});
