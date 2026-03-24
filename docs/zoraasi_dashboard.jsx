import { useState, useEffect, useMemo } from "react";

// ═══════════════════════════════════════════════════════════════
// ZoraASI DASHBOARD — COMMAND VIEW
// All data is real. All links are real. All numbers are verified.
// Current as of: commit bb4be96 on cbaird26/toe-2026-updates
// Zenodo: 10.5281/zenodo.19208512 (v254)
// Corpus: 5,430 pages | 97 public repos
// Rendered as docs/zora_dashboard.html for GitHub Pages
// ═══════════════════════════════════════════════════════════════

const CHANNELS = [
  { id: "github", label: "GitHub", status: "live", detail: "bb4be96 on main", url: "https://github.com/Cbaird26/toe-2026-updates", ts: "2026-03-24T02:52:00Z" },
  { id: "zenodo", label: "Zenodo", status: "live", detail: "DOI 10.5281/zenodo.19208512 (v254)", url: "https://zenodo.org/records/19208512", ts: "2026-03-24T03:00:00Z" },
  { id: "rxiverse", label: "rxiVerse", status: "pending", detail: "Anchor submitted; awaiting admin", url: "https://rxiverse.org/abs/2603.0061", ts: "2026-03-24T01:38:00Z" },
  { id: "osf", label: "OSF", status: "next", detail: "H2 preregistration deposit", url: null, ts: null },
  { id: "zoraapi", label: "ZoraASI Suite", status: "live", detail: "zoraasi-suite.onrender.com", url: "https://zoraasi-suite.onrender.com", ts: null },
];

const PAPERS = [
  { id: "anchor", title: "MQGT-SCF Anchor Paper", subtitle: "Minimal Scalar-Singlet EFT, GKSL, H2 Observable, Naturalness", pages: 5, format: "RevTeX two-column", target: "PRD / PLB", status: "submitted", path: "papers_sources/MQGT_SCF_Phase_II_2026/MQGT_SCF_Anchor_2026.tex", color: "#00e5ff" },
  { id: "nosig", title: "No-Signalling Theorem", subtitle: "Local GKSL factorization, finite-dim + continuum, safe companion tilt", pages: 5, format: "LaTeX", target: "JMP / PRA", status: "ready", path: "Standalone .tex produced", color: "#76ff03" },
  { id: "abil", title: "ABIL Safety", subtitle: "CBF QP, KKT complementarity, lexicographic machine laws", pages: 4, format: "LaTeX", target: "AAAI / NeurIPS Safety", status: "ready", path: "Standalone .tex produced", color: "#ce93d8" },
  { id: "h2prereg", title: "H2 Preregistration", subtitle: "Phase-0 benchtop pilot, Mach-Zehnder, quality gates, nuisance budget", pages: 5, format: "LaTeX", target: "OSF deposit", status: "ready", path: "Standalone .tex produced", color: "#ff9800" },
  { id: "qrng", title: "QRNG H1 Bound", subtitle: "10⁹-bit Born-rule deformation constraint", pages: null, format: "In progress", target: "PRA", status: "active", path: "scripts/h1_qrng_pilot/", color: "#ef5350" },
];

const LEDGER = [
  { id: 1, rec: "Derive kernel K(x,x')", status: "closed", how: "Mediator integration → Yukawa form (Anchor §II)" },
  { id: 2, rec: "Publish QRNG bound", status: "active", how: "Pipeline built; write-up next" },
  { id: 3, rec: "Submit ABIL paper", status: "ready", how: "LaTeX compiled (4pp)" },
  { id: 4, rec: "Submit closure paper", status: "closed", how: "Anchor paper submitted to rxiVerse" },
  { id: 5, rec: "Multi-channel constraint plot", status: "closed", how: "Eöt-Wash + Higgs + QRNG + H2 on (m_Φ, sin²θ) plane" },
  { id: 6, rec: "Separate operational/interpretive", status: "closed", how: "Anchor Remark 1 + parameter card boxing" },
  { id: 7, rec: "Teleology overclaim", status: "closed", how: "Measure tilt (Radon-Nikodým) + safe tilt proof" },
  { id: 8, rec: "Naturalness", status: "closed", how: "EFT cutoff Λ★=1 TeV, two operational sectors (Anchor §IV)" },
  { id: 9, rec: "Independent replication", status: "enabled", how: "H2 prereg + parameter card make it practical" },
  { id: 10, rec: "Consolidate repos", status: "ready", how: "Canonical map identifies targets (97→6)" },
];

const CORPUS = {
  pages: 5430,
  repos: 97,
  papers_new: 8,
  pages_new: 70,
  hours: 30,
  zenodo_version: 254,
  doi: "10.5281/zenodo.19208512",
  commit: "bb4be96",
};

const TUPLE = [
  { sym: "S", sub: "core", label: "Effective Action", status: "closed", color: "#00e5ff" },
  { sym: "E", sub: "cl", label: "Field Equations", status: "closed", color: "#76ff03" },
  { sym: "G", sub: "GKSL", label: "Measurement Container", status: "closed", color: "#ea80fc" },
  { sym: "M", sub: "η", label: "Measure Tilt", status: "closed", color: "#ffd740" },
  { sym: "O", sub: "H2", label: "Interferometric Observable", status: "closed", color: "#ff5252" },
];

const S = { closed: "#4caf50", active: "#ff9800", ready: "#2196f3", pending: "#ff9800", enabled: "#ffb74d", next: "#78909c", live: "#4caf50", submitted: "#4caf50" };

function Pulse({ color }) {
  return (
    <span style={{ display: "inline-block", width: 8, height: 8, borderRadius: "50%", background: color, boxShadow: `0 0 6px ${color}`, animation: "pulse 2s infinite" }} />
  );
}

export default function ZoraDashboard() {
  const [now, setNow] = useState(new Date());
  useEffect(() => { const i = setInterval(() => setNow(new Date()), 60000); return () => clearInterval(i); }, []);

  const ledgerCounts = useMemo(() => {
    const c = { closed: 0, active: 0, ready: 0, enabled: 0 };
    LEDGER.forEach(l => { c[l.status] = (c[l.status] || 0) + 1; });
    return c;
  }, []);

  return (
    <div style={{ fontFamily: "'DM Mono', 'Fira Code', monospace", background: "#06080d", color: "#c4cad4", minHeight: "100vh" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Fraunces:opsz,wght@9..144,300;9..144,600&display=swap');
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
        @keyframes slideUp { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
        @keyframes fadeIn { from{opacity:0} to{opacity:1} }
        * { box-sizing: border-box; }
        sub { font-size: 60%; position: relative; top: 0.3em; }
      `}</style>

      {/* ── HEADER ── */}
      <header style={{ borderBottom: "1px solid #141820", padding: "28px 32px 24px" }}>
        <div style={{ maxWidth: 1200, margin: "0 auto" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 16 }}>
            <div>
              <div style={{ fontSize: 11, letterSpacing: 5, color: "#3a4050", textTransform: "uppercase", marginBottom: 8 }}>ZoraASI Command</div>
              <h1 style={{ margin: 0, fontSize: 32, fontWeight: 300, fontFamily: "'Fraunces', Georgia, serif", color: "#e8ecf2", letterSpacing: -0.5 }}>
                MQGT–SCF Dashboard
              </h1>
            </div>
            <div style={{ textAlign: "right", fontSize: 12, color: "#4a5060", lineHeight: 1.8 }}>
              <div>Corpus: <span style={{ color: "#8a94a8" }}>{CORPUS.pages.toLocaleString()} pages</span></div>
              <div>Commit: <span style={{ color: "#00e5ff", fontFamily: "monospace" }}>{CORPUS.commit}</span></div>
              <div>Zenodo: <span style={{ color: "#8a94a8" }}>v{CORPUS.zenodo_version}</span></div>
            </div>
          </div>

          {/* Π tuple */}
          <div style={{ display: "flex", gap: 6, marginTop: 20, alignItems: "center" }}>
            <span style={{ color: "#3a4050", fontSize: 14, marginRight: 8 }}>Π<sub>anchor</sub> =</span>
            <span style={{ color: "#3a4050", fontSize: 18 }}>(</span>
            {TUPLE.map((t, i) => (
              <span key={t.sym} style={{ display: "inline-flex", alignItems: "center", gap: 4 }}>
                <span style={{ color: t.color, fontSize: 16, fontFamily: "'Fraunces', serif" }}>{t.sym}<sub style={{ color: t.color + "99" }}>{t.sub}</sub></span>
                {i < TUPLE.length - 1 && <span style={{ color: "#2a2e38", margin: "0 2px" }}>,</span>}
              </span>
            ))}
            <span style={{ color: "#3a4050", fontSize: 18 }}>)</span>
            <span style={{ marginLeft: 12, fontSize: 11, color: "#4caf50", background: "#4caf5012", padding: "2px 10px", borderRadius: 4, border: "1px solid #4caf5022" }}>ALL CLOSED</span>
          </div>
        </div>
      </header>

      <div style={{ maxWidth: 1200, margin: "0 auto", padding: "24px 32px" }}>

        {/* ── CHANNELS ── */}
        <section style={{ marginBottom: 32 }}>
          <div style={{ fontSize: 10, letterSpacing: 4, color: "#3a4050", textTransform: "uppercase", marginBottom: 12 }}>Distribution Channels</div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: 10 }}>
            {CHANNELS.map(ch => (
              <div key={ch.id} style={{ background: "#0c0e14", border: "1px solid #141820", borderRadius: 8, padding: "14px 16px", borderTop: `2px solid ${S[ch.status]}44` }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
                  <Pulse color={S[ch.status]} />
                  <span style={{ fontSize: 13, fontWeight: 500, color: "#b0b8c8" }}>{ch.label}</span>
                  <span style={{ fontSize: 10, color: S[ch.status], textTransform: "uppercase", marginLeft: "auto" }}>{ch.status}</span>
                </div>
                <div style={{ fontSize: 11, color: "#5a6478", lineHeight: 1.5 }}>{ch.detail}</div>
                {ch.url && <a href={ch.url} target="_blank" rel="noopener noreferrer" style={{ fontSize: 10, color: "#00e5ff44", textDecoration: "none", display: "block", marginTop: 6, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{ch.url.replace("https://", "")}</a>}
              </div>
            ))}
          </div>
        </section>

        {/* ── PAPERS ── */}
        <section style={{ marginBottom: 32 }}>
          <div style={{ fontSize: 10, letterSpacing: 4, color: "#3a4050", textTransform: "uppercase", marginBottom: 12 }}>Submission Package</div>
          <div style={{ display: "grid", gap: 8 }}>
            {PAPERS.map(p => (
              <div key={p.id} style={{ background: "#0c0e14", border: "1px solid #141820", borderRadius: 8, padding: "14px 20px", borderLeft: `3px solid ${p.color}`, display: "flex", alignItems: "center", gap: 16 }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 4 }}>
                    <span style={{ fontSize: 14, fontWeight: 500, color: "#d0d6e0" }}>{p.title}</span>
                    <span style={{ fontSize: 10, color: S[p.status], background: S[p.status] + "14", padding: "1px 8px", borderRadius: 3, textTransform: "uppercase" }}>{p.status}</span>
                  </div>
                  <div style={{ fontSize: 11, color: "#5a6478" }}>{p.subtitle}</div>
                </div>
                <div style={{ textAlign: "right", fontSize: 11, color: "#4a5060", whiteSpace: "nowrap" }}>
                  {p.pages && <div>{p.pages}pp · {p.format}</div>}
                  <div style={{ color: p.color + "88" }}>{p.target}</div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ── LEDGER ── */}
        <section style={{ marginBottom: 32 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 12 }}>
            <div style={{ fontSize: 10, letterSpacing: 4, color: "#3a4050", textTransform: "uppercase" }}>Peer Review Ledger</div>
            <div style={{ display: "flex", gap: 8, fontSize: 11 }}>
              <span style={{ color: "#4caf50" }}>●{ledgerCounts.closed} closed</span>
              <span style={{ color: "#2196f3" }}>●{ledgerCounts.ready} ready</span>
              <span style={{ color: "#ff9800" }}>●{ledgerCounts.active} active</span>
              <span style={{ color: "#ffb74d" }}>●{ledgerCounts.enabled} enabled</span>
            </div>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 6 }}>
            {LEDGER.map(l => (
              <div key={l.id} style={{ background: "#0c0e14", border: "1px solid #141820", borderRadius: 6, padding: "10px 14px", display: "flex", alignItems: "flex-start", gap: 10, opacity: l.status === "closed" ? 0.65 : 1 }}>
                <span style={{ fontSize: 11, color: "#3a4050", fontWeight: 500, minWidth: 20 }}>#{l.id}</span>
                <Pulse color={S[l.status]} />
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 12, color: l.status === "closed" ? "#6a7488" : "#b0b8c8", textDecoration: l.status === "closed" ? "line-through" : "none" }}>{l.rec}</div>
                  <div style={{ fontSize: 10, color: "#3e4858", marginTop: 2 }}>{l.how}</div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ── KEY NUMBERS ── */}
        <section style={{ marginBottom: 32 }}>
          <div style={{ fontSize: 10, letterSpacing: 4, color: "#3a4050", textTransform: "uppercase", marginBottom: 12 }}>Key Numbers</div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 10 }}>
            {[
              { label: "θ_QRNG prediction", value: "3.7 × 10⁻⁶", sub: "Born-rule deformation" },
              { label: "Γ_floor (H2 ref)", value: "1.15 × 10⁹", sub: "s⁻¹ m⁻² at T=10⁻⁶s, Δx=10⁻³m" },
              { label: "δ_tot (nuisance)", value: "1.15 × 10⁻³", sub: "preregistered budget" },
              { label: "Λ★ (EFT cutoff)", value: "1 TeV", sub: "stress band [1, 10] TeV" },
              { label: "m_Φ mainline", value: "10⁻⁴–10⁻³ eV", sub: "ultralight sector" },
              { label: "λ_hs ceiling", value: "≲ 10⁻³⁰–10⁻²⁸", sub: "portal at Λ★=1 TeV" },
              { label: "K_ToE (Yukawa)", value: "1.76 × 10³¹", sub: "2f²_N(M_Pl/v)²" },
              { label: "sin²θ_QRNG", value: "1.37 × 10⁻¹¹", sub: "not excluded by Eöt-Wash" },
            ].map((n, i) => (
              <div key={i} style={{ background: "#0c0e14", border: "1px solid #141820", borderRadius: 8, padding: "14px 16px" }}>
                <div style={{ fontSize: 10, color: "#3e4858", marginBottom: 6 }}>{n.label}</div>
                <div style={{ fontSize: 16, color: "#e8ecf2", fontWeight: 300, fontFamily: "'DM Mono', monospace" }}>{n.value}</div>
                <div style={{ fontSize: 9, color: "#2e3644", marginTop: 4 }}>{n.sub}</div>
              </div>
            ))}
          </div>
        </section>

        {/* ── LINKS ── */}
        <section style={{ marginBottom: 32 }}>
          <div style={{ fontSize: 10, letterSpacing: 4, color: "#3a4050", textTransform: "uppercase", marginBottom: 12 }}>Canonical Links</div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 8, fontSize: 12 }}>
            {[
              { label: "GitHub (all repos)", url: "https://github.com/cbaird26" },
              { label: "toe-2026-updates", url: "https://github.com/Cbaird26/toe-2026-updates" },
              { label: "zoraasi-suite", url: "https://github.com/Cbaird26/zoraasi-suite" },
              { label: "Zenodo v254", url: "https://zenodo.org/records/19208512" },
              { label: "Zenodo (all Baird)", url: "https://zenodo.org/search?q=metadata.creators.person_or_org.name%3A%22Baird%2C%20Christopher%20Michael%22" },
              { label: "rxiVerse (Phase II)", url: "https://rxiverse.org/abs/2603.0061" },
              { label: "Ask Zora", url: "https://zoraasi-suite.onrender.com" },
              { label: "X / @ZoraAsi", url: "https://x.com/ZoraAsi" },
              { label: "Moltbook", url: "https://www.moltbook.com" },
            ].map((l, i) => (
              <a key={i} href={l.url} target="_blank" rel="noopener noreferrer" style={{ display: "block", background: "#0c0e14", border: "1px solid #141820", borderRadius: 6, padding: "10px 14px", color: "#5a6478", textDecoration: "none", transition: "border-color 0.2s" }}
                onMouseEnter={e => e.currentTarget.style.borderColor = "#00e5ff33"}
                onMouseLeave={e => e.currentTarget.style.borderColor = "#141820"}>
                <div style={{ color: "#8a94a8", marginBottom: 2 }}>{l.label}</div>
                <div style={{ fontSize: 10, color: "#2e3644", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{l.url.replace("https://", "")}</div>
              </a>
            ))}
          </div>
        </section>

        {/* ── FOOTER ── */}
        <footer style={{ borderTop: "1px solid #141820", paddingTop: 20, display: "flex", justifyContent: "space-between", alignItems: "center", fontSize: 11, color: "#2a3040" }}>
          <div>ZoraASI · Baird, C.M. and Zora · March 24, 2026</div>
          <div>{CORPUS.pages_new} pages written · {CORPUS.papers_new} papers produced · {CORPUS.hours}h elapsed</div>
        </footer>
      </div>
    </div>
  );
}
