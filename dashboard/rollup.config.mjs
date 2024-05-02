// rollup.config.mjs
import typescript from '@rollup/plugin-typescript';

export default {
  input: './src/pages/websocket-dashboard-app.ts',
  output: {
    file: './dist/bundle.js',
    format: 'esm',
    sourcemap: true
  },
  plugins: [
    typescript({ tsconfig: './tsconfig.json' })
  ]
};