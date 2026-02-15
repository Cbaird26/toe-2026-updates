# Research Tab Content — christophermichaelbaird.com

Use this copy when adding a **Research** tab to your site. Adapt markup to match your existing structure.

---

## Tab label (nav)
```
Research
```

---

## Page title
```
Research
```

---

## Intro paragraph
```
Alongside clinical work, I pursue theoretical physics research—including Theory of Everything (ToE) and MQGT-SCF frameworks. Papers, simulations, and open-source projects live on GitHub under [Cbaird26](https://github.com/Cbaird26). Below is an interactive map of the ecosystem.
```

---

## Embedded or linked illustration

**Option A — Link (recommended for simplicity)**  
Place a button or card that links out:

```html
<a href="https://cbaird26.github.io/toe-2026-updates/cbaird26_ecosystem_illustration.html" 
   target="_blank" 
   rel="noopener">
  View Cbaird26 Ecosystem Map →
</a>
```

Fallback URL (if Pages not yet enabled):  
`https://htmlpreview.github.io/?https://raw.githubusercontent.com/Cbaird26/toe-2026-updates/main/cbaird26_ecosystem_illustration.html`

---

**Option B — Embed via iframe**  
If you prefer it embedded on the page:

```html
<iframe 
  src="https://cbaird26.github.io/toe-2026-updates/cbaird26_ecosystem_illustration.html" 
  title="Cbaird26 GitHub ecosystem"
  width="100%" 
  height="700" 
  style="border: 1px solid #2a3142; border-radius: 8px;">
</iframe>
```

---

## Optional: additional links

```
• [GitHub: Cbaird26](https://github.com/Cbaird26) — repos & clone guide  
• [ToE 2026 Updates](https://github.com/Cbaird26/toe-2026-updates) — papers, addenda, illustrations  
• Zenodo / cbaird26 — latest Baird outputs (papers, datasets)
```

---

## Suggested section structure (HTML)

```html
<section id="research">
  <h2>Research</h2>
  <p>Alongside clinical work, I pursue theoretical physics research—including Theory of Everything (ToE) and MQGT-SCF frameworks. Papers, simulations, and open-source projects live on GitHub under <a href="https://github.com/Cbaird26">Cbaird26</a>. Below is an interactive map of the ecosystem.</p>
  
  <p>
    <a href="https://cbaird26.github.io/toe-2026-updates/cbaird26_ecosystem_illustration.html" 
       target="_blank" 
       rel="noopener"
       class="button">View Cbaird26 Ecosystem Map →</a>
  </p>
  
  <p><small>97 public repos across ToE, MQGT-SCF, simulations, quantum, and tools.</small></p>
</section>
```

---

*Add this as a new nav item and route (e.g. `/#research` or `/research`) to match your site’s pattern.*
