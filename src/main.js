import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { Toaster } from 'vue-sonner'
import renderMathInElement from "katex/contrib/auto-render/auto-render"
import "katex/dist/katex.min.css"

const app = createApp(App)
app.component('Toaster', Toaster)
app.mount("#app")

// Auto-Render alle 50ms nach Mount
setTimeout(() => {
  renderMathInElement(document.body, {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "\\[", right: "\\]", display: true },
      { left: "\\(", right: "\\)", display: false },
      { left: "$", right: "$", display: false },
    ],
    throwOnError: false,
  })
}, 50)
