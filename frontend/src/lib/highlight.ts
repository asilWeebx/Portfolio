import hljs from 'highlight.js/lib/core'
import bash from 'highlight.js/lib/languages/bash'
import css from 'highlight.js/lib/languages/css'
import dart from 'highlight.js/lib/languages/dart'
import dockerfile from 'highlight.js/lib/languages/dockerfile'
import ini from 'highlight.js/lib/languages/ini'
import javascript from 'highlight.js/lib/languages/javascript'
import json from 'highlight.js/lib/languages/json'
import nginx from 'highlight.js/lib/languages/nginx'
import plaintext from 'highlight.js/lib/languages/plaintext'
import python from 'highlight.js/lib/languages/python'
import sql from 'highlight.js/lib/languages/sql'
import typescript from 'highlight.js/lib/languages/typescript'
import xml from 'highlight.js/lib/languages/xml'
import yaml from 'highlight.js/lib/languages/yaml'

const langs = { bash, css, dart, dockerfile, ini, javascript, json, nginx, plaintext, python, sql, typescript, xml, yaml }
Object.entries(langs).forEach(([name, lang]) => hljs.registerLanguage(name, lang))
hljs.configure({ ignoreUnescapedHTML: true })

export function highlightAll(root: HTMLElement) {
  root.querySelectorAll<HTMLElement>('pre code').forEach((el) => {
    if (el.dataset.highlighted) return
    const m = el.className.match(/language-([\w-]+)/)
    if (m && !hljs.getLanguage(m[1])) el.className = 'language-plaintext'
    hljs.highlightElement(el)
  })
}
