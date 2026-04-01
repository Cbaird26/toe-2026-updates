import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Relative base keeps the bundle portable for local preview or private hosting.
export default defineConfig({
  plugins: [react()],
  base: "./",
  test: {
    environment: "node",
    include: ["src/**/*.test.js"],
  },
});
