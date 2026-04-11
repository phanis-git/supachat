// import { defineConfig } from 'vite'
// import react from '@vitejs/plugin-react'

// // https://vite.dev/config/
// export default defineConfig({
//   plugins: [react()],
//   server: {
//     host: '0.0.0.0',
//     port: 5173,
//     allowedHosts: ['all']  // ✅ allows any host including "frontend"
//   }
// })

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,        // ← alternative to '0.0.0.0'
    port: 5173,
    allowedHosts: [
      'all',
      'frontend',
      'localhost',
      '23.20.195.93'
    ]
  }
})