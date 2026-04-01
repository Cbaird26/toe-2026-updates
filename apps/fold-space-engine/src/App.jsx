import { useState, useEffect, useRef, useCallback } from "react";
import { branchProbabilities, buildSymmetricFutures, timelineBranchProbabilities } from "./math.js";

const TAU = Math.PI * 2;
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
const lerp = (a, b, t) => a + (b - a) * t;

const P = {
  void: "#06070c", deep: "#0b0d16", panel: "#0e1019",
  surface: "#131624", border: "#222640", glow: "#00f0ff",
  glow2: "#b374ff", glow3: "#f472b6", gold: "#fbbf24",
  ember: "#ff9533", green: "#3de8a8", text: "#d4d8e8",
  dim: "#8890b0", ghost: "#363c58", faint: "#5c6488",
};

const FONT = "'Courier New', 'Lucida Console', monospace";

function Knob({ label, value, onChange, min, max, step = 0.01, color = P.glow }) {
  return (
    <div style={{ marginBottom: 12 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, fontFamily: FONT, marginBottom: 3 }}>
        <span style={{ color: P.dim, textTransform: "uppercase", letterSpacing: "0.06em" }}>{label}</span>
        <span style={{ color, fontWeight: 600 }}>{typeof value === "number" ? (Math.abs(value) < 0.001 && value !== 0 ? value.toExponential(1) : value.toFixed(step < 0.01 ? 4 : 2)) : value}</span>
      </div>
      <input type="range" min={min} max={max} step={step} value={value}
        onChange={e => onChange(parseFloat(e.target.value))}
        style={{ width: "100%", accentColor: color, height: 4, background: P.border, borderRadius: 2, cursor: "pointer" }} />
    </div>
  );
}

function GlowBox({ color, children, glow = false }) {
  return (
    <div style={{
      padding: "12px 14px", background: color + "0a", borderRadius: 7,
      border: "1px solid " + color + "30", fontSize: 12, color: P.text,
      lineHeight: 1.8, fontFamily: FONT, position: "relative", overflow: "hidden", marginTop: 12,
    }}>
      {glow && <div style={{ position: "absolute", top: -20, right: -20, width: 60, height: 60, background: "radial-gradient(circle, " + color + "18, transparent)", borderRadius: "50%" }} />}
      {children}
    </div>
  );
}

function EqBlock({ children, color = P.glow }) {
  return (
    <div style={{
      fontFamily: FONT, fontSize: 13, color, background: color + "0a",
      padding: "8px 12px", borderRadius: 5, border: "1px solid " + color + "20",
      marginBottom: 6, letterSpacing: "0.01em", overflowX: "auto",
    }}>{children}</div>
  );
}

function DeviceHeader({ name, subtitle, color, classification }) {
  return (
    <div style={{ marginBottom: 16 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 5, flexWrap: "wrap" }}>
        <div style={{ width: 10, height: 10, borderRadius: "50%", background: color, boxShadow: "0 0 14px " + color + "80" }} />
        <span style={{ fontSize: 18, fontWeight: 700, color: "#fff", fontFamily: "'Georgia', serif" }}>{name}</span>
        <span style={{
          fontSize: 9, color: P.ember, background: P.ember + "18", padding: "3px 8px",
          borderRadius: 4, border: "1px solid " + P.ember + "35", textTransform: "uppercase",
          letterSpacing: "0.1em", fontFamily: FONT, fontWeight: 600,
        }}>{classification}</span>
      </div>
      <div style={{ fontSize: 13, color: P.dim, fontFamily: FONT, fontStyle: "italic", lineHeight: 1.5 }}>{subtitle}</div>
    </div>
  );
}

function ProbabilitySculptor() {
  const ref = useRef(null);
  const [eta, setEta] = useState(0.0);
  const [nFutures, setNFutures] = useState(6);
  const [coherence, setCoherence] = useState(0.5);
  const [t, setT] = useState(0);
  useEffect(() => { const id = setInterval(() => setT(p => p + 0.03), 30); return () => clearInterval(id); }, []);

  const draw = useCallback(() => {
    const cv = ref.current; if (!cv) return;
    const ctx = cv.getContext("2d"); const W = cv.width, H = cv.height;
    ctx.clearRect(0, 0, W, H);
    const bg = ctx.createRadialGradient(W/2, H/2, 0, W/2, H/2, W/2);
    bg.addColorStop(0, "#0d0f1a"); bg.addColorStop(1, P.void);
    ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);
    const cx = W/2, cy = H/2, R = Math.min(W, H) * 0.36;
    const futures = buildSymmetricFutures(nFutures);
    const { probs } = branchProbabilities({ eta, coherence, futures });
    for (let i = 0; i < nFutures; i++) {
      const f = futures[i], prob = probs[i];
      const angle = f.angle + Math.sin(t + i) * 0.02;
      const r = R * (0.3 + prob * 2.5);
      const x = cx + Math.cos(angle) * r, y = cy + Math.sin(angle) * r;
      const hue = f.dE > 0 ? 170 : (f.dE < 0 ? 320 : 50);
      ctx.strokeStyle = "hsla("+hue+",80%,60%,"+(0.15+prob*0.6)+")";
      ctx.lineWidth = 0.5 + prob * 4;
      ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(x, y); ctx.stroke();
      const orbR = 8 + prob * 40;
      const grad = ctx.createRadialGradient(x, y, 0, x, y, orbR);
      grad.addColorStop(0, "hsla("+hue+",90%,70%,"+(0.6+prob*0.4)+")");
      grad.addColorStop(0.5, "hsla("+hue+",80%,50%,"+(0.2+prob*0.3)+")");
      grad.addColorStop(1, "transparent");
      ctx.fillStyle = grad; ctx.beginPath(); ctx.arc(x, y, orbR, 0, TAU); ctx.fill();
      ctx.fillStyle = "hsla("+hue+",60%,85%,"+(0.5+prob)+")";
      ctx.font = "bold "+(12+prob*6)+"px "+FONT; ctx.textAlign = "center";
      ctx.fillText(f.label, x, y - orbR - 6);
      ctx.font = "11px "+FONT; ctx.fillStyle = "hsla("+hue+",50%,75%,0.8)";
      ctx.fillText((prob*100).toFixed(1)+"%", x, y+4);
      ctx.font = "10px "+FONT; ctx.fillText("dE="+f.dE.toFixed(1), x, y+16);
    }
    const cg = ctx.createRadialGradient(cx, cy, 0, cx, cy, 22);
    cg.addColorStop(0, "rgba(0,240,255,"+(0.5+Math.sin(t*2)*0.2)+")");
    cg.addColorStop(0.5, "rgba(0,240,255,0.15)"); cg.addColorStop(1, "transparent");
    ctx.fillStyle = cg; ctx.beginPath(); ctx.arc(cx, cy, 22, 0, TAU); ctx.fill();
    ctx.fillStyle = "#fff"; ctx.font = "bold 13px "+FONT; ctx.textAlign = "center"; ctx.fillText("\u03A8", cx, cy+5);
    ctx.strokeStyle = "rgba(0,240,255,"+(0.12+Math.sin(t)*0.05)+")"; ctx.lineWidth = 0.5;
    ctx.beginPath(); ctx.arc(cx, cy, R, 0, TAU); ctx.stroke();
    const mi = probs.indexOf(Math.max(...probs));
    ctx.fillStyle = P.gold; ctx.font = "bold 13px "+FONT; ctx.textAlign = "left";
    ctx.fillText("DOMINANT: "+futures[mi].label+" ("+(probs[mi]*100).toFixed(1)+"%)", 12, H-12);
  }, [eta, nFutures, coherence, t]);
  useEffect(() => { draw(); }, [draw]);

  return (<div>
    <DeviceHeader name="Probability Sculptor" subtitle="Bias quantum branching toward desired futures via amplified \u03B7-tilt" color={P.glow} classification="Thought Experiment" />
    <EqBlock>{"P(future_i) \u221D |c_i|\u00B2 \u00B7 exp(\u03B7_eff \u00B7 \u0394E_i) \u2014 amplified Born rule"}</EqBlock>
    <EqBlock color={P.glow2}>{"\u03B7_eff = \u03B7 \u00B7 (1 + Coherence \u00B7 \u03A6c_density) \u2014 consciousness amplification"}</EqBlock>
    <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
      <div style={{ flex: "1 1 280px" }}>
        <canvas ref={ref} width={440} height={380} style={{ width: "100%", maxWidth: 440, borderRadius: 8, border: "1px solid "+P.border }} />
      </div>
      <div style={{ flex: "0 0 200px", minWidth: 180 }}>
        <Knob label={"\u03B7 (tilt strength)"} value={eta} onChange={setEta} min={-3} max={3} step={0.01} />
        <Knob label={"\u03A6c coherence"} value={coherence} onChange={setCoherence} min={0} max={1} step={0.01} color={P.glow2} />
        <Knob label="N futures" value={nFutures} onChange={v => setNFutures(Math.round(v))} min={3} max={12} step={1} color={P.gold} />
        <GlowBox color={P.glow} glow>
          <span style={{ color: P.glow, fontWeight: 700 }}>PRINCIPLE:</span> The paper's measure tilt biases outcomes by \u0394E. If \u03A6c coherence is amplified (jh\u0101na-level), effective \u03B7 scales dramatically.<br /><br />
          <span style={{ color: P.gold }}>{"\u03B7 = 0:"}</span> all futures equiprobable<br />
          <span style={{ color: P.glow3 }}>{"\u03B7 \u226B 1:"}</span> single future dominates
        </GlowBox>
      </div>
    </div>
  </div>);
}

function FoldSpaceEngine() {
  const ref = useRef(null);
  const [mM, setMM] = useState(1.0);
  const [coupling, setCoupling] = useState(1.0);
  const [foldFactor, setFoldFactor] = useState(0.0);
  const [t, setT] = useState(0);
  useEffect(() => { const id = setInterval(() => setT(p => p + 0.02), 30); return () => clearInterval(id); }, []);

  const draw = useCallback(() => {
    const cv = ref.current; if (!cv) return;
    const ctx = cv.getContext("2d"); const W = cv.width, H = cv.height;
    ctx.clearRect(0, 0, W, H);
    const bg = ctx.createRadialGradient(W/2, H/2, 0, W/2, H/2, W*0.6);
    bg.addColorStop(0, "#0f0a1a"); bg.addColorStop(1, P.void);
    ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);
    const cx = W/2, cy = H/2, gs = 16, sp = 22;
    const sx = cx - (gs-1)*sp/2, sy = cy - (gs-1)*sp/2;
    for (let i = 0; i < gs; i++) for (let j = 0; j < gs; j++) {
      let x = sx + i*sp, y = sy + j*sp;
      const dx = x-cx, dy = y-cy, dist = Math.sqrt(dx*dx+dy*dy);
      const kv = coupling * Math.exp(-mM*dist/80) / (dist/80+0.1);
      const fs = foldFactor * kv * 0.3;
      x -= dx*fs; y -= dy*fs;
      const w = Math.sin(dist*0.05 - t*2) * (1-foldFactor) * 2;
      x += w*dx/(dist+1)*0.5; y += w*dy/(dist+1)*0.5;
      const int = clamp(kv*0.15, 0, 1);
      const hue = lerp(260, 180, int);
      ctx.fillStyle = "hsla("+hue+",80%,"+(50+int*30)+"%,"+(0.25+int*0.6)+")";
      ctx.beginPath(); ctx.arc(x, y, 1.5+int*3, 0, TAU); ctx.fill();
      if (i < gs-1) {
        let nx = sx+(i+1)*sp, ny = sy+j*sp;
        const nd = Math.sqrt((nx-cx)**2+(ny-cy)**2);
        const nk = coupling*Math.exp(-mM*nd/80)/(nd/80+0.1);
        const nf = foldFactor*nk*0.3;
        nx -= (nx-cx)*nf; ny -= (ny-cy)*nf;
        ctx.strokeStyle = "hsla("+hue+",60%,50%,"+((0.25+int*0.6)*0.35)+")";
        ctx.lineWidth = 0.5;
        ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(nx, ny); ctx.stroke();
      }
    }
    if (foldFactor > 0.1) {
      const fg = ctx.createRadialGradient(cx, cy, 0, cx, cy, 40+foldFactor*60);
      fg.addColorStop(0, "rgba(179,116,255,"+foldFactor*0.5+")");
      fg.addColorStop(0.5, "rgba(179,116,255,"+foldFactor*0.15+")");
      fg.addColorStop(1, "transparent");
      ctx.fillStyle = fg; ctx.beginPath(); ctx.arc(cx, cy, 40+foldFactor*60, 0, TAU); ctx.fill();
    }
    ctx.fillStyle = P.glow2; ctx.font = "12px "+FONT; ctx.textAlign = "left";
    ctx.fillText("K(r) range: l = 1/mM = "+(1/mM).toFixed(2), 10, H-28);
    ctx.fillStyle = P.text; ctx.font = "11px "+FONT;
    ctx.fillText("Fold radius: "+(foldFactor*(1/mM)*50).toFixed(1)+" units", 10, H-10);
  }, [mM, coupling, foldFactor, t]);
  useEffect(() => { draw(); }, [draw]);

  return (<div>
    <DeviceHeader name="Fold-Space Engine" subtitle="Exploit Yukawa kernel long-range limit to contract spatial separation" color={P.glow2} classification="Thought Experiment" />
    <EqBlock color={P.glow2}>{"K(r) = g\u03A6\u00B7gE \u00B7 exp(\u2212mM\u00B7r) / (4\u03C0r) \u2014 nonlocal kernel"}</EqBlock>
    <EqBlock color={P.ember}>{"mM \u2192 0 \u27F9 K(r) \u2192 g\u03A6gE/(4\u03C0r) \u2014 infinite range fold"}</EqBlock>
    <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
      <div style={{ flex: "1 1 280px" }}>
        <canvas ref={ref} width={440} height={380} style={{ width: "100%", maxWidth: 440, borderRadius: 8, border: "1px solid "+P.border }} />
      </div>
      <div style={{ flex: "0 0 200px", minWidth: 180 }}>
        <Knob label="mM (mediator mass)" value={mM} onChange={setMM} min={0.01} max={3} step={0.01} color={P.glow2} />
        <Knob label={"g\u03A6 \u00B7 gE"} value={coupling} onChange={setCoupling} min={0.1} max={5} step={0.05} color={P.glow} />
        <Knob label="Fold factor" value={foldFactor} onChange={setFoldFactor} min={0} max={1} step={0.01} color={P.ember} />
        <GlowBox color={P.glow2} glow>
          <span style={{ color: P.glow2, fontWeight: 700 }}>PRINCIPLE:</span> As mM approaches 0 the nonlocal interaction goes infinite-range, folding separated points together.<br /><br />
          <span style={{ color: P.ember, fontWeight: 600 }}>Drag Fold factor</span> to collapse the spacetime grid.
        </GlowBox>
      </div>
    </div>
  </div>);
}

function TimelineSelector() {
  const ref = useRef(null);
  const [eta, setEta] = useState(0);
  const [Fi, setFi] = useState(0.5);
  const [t, setT] = useState(0);
  useEffect(() => { const id = setInterval(() => setT(p => p + 0.015), 30); return () => clearInterval(id); }, []);
  const timelines = [
    { name: "Stagnation", dE: -0.8, hue: 0 },{ name: "Conflict", dE: -0.3, hue: 30 },
    { name: "Baseline", dE: 0.0, hue: 50 },{ name: "Growth", dE: 0.4, hue: 150 },
    { name: "Convergence", dE: 0.8, hue: 180 },{ name: "Transcendence", dE: 1.2, hue: 270 },
  ];

  const draw = useCallback(() => {
    const cv = ref.current; if (!cv) return;
    const ctx = cv.getContext("2d"); const W = cv.width, H = cv.height;
    ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.void; ctx.fillRect(0, 0, W, H);
    const { probs } = timelineBranchProbabilities({ eta, Fi, timelines });
    const oX = 65, bH = (H-80)/timelines.length, tY = 40;
    for (let i = 0; i < timelines.length; i++) {
      const tl = timelines[i], prob = probs[i], y = tY + i*bH + bH/2;
      const endX = oX + 90 + prob * (W - 200);
      const alpha = 0.2 + prob * 0.7;
      ctx.strokeStyle = "hsla("+tl.hue+",70%,60%,"+alpha+")";
      ctx.lineWidth = 0.8 + prob * 5;
      ctx.beginPath(); ctx.moveTo(oX, H/2); ctx.quadraticCurveTo(oX+40, y, endX, y); ctx.stroke();
      ctx.strokeStyle = "hsla("+tl.hue+",80%,70%,"+(alpha*0.5)+")";
      ctx.lineWidth = 1; ctx.beginPath();
      for (let px = endX-60; px < endX+30; px += 2) {
        const wave = Math.sin((px-endX)*0.15+t*3+i)*prob*10;
        px === endX-60 ? ctx.moveTo(px, y+wave) : ctx.lineTo(px, y+wave);
      }
      ctx.stroke();
      const oR = 5+prob*18;
      const grad = ctx.createRadialGradient(endX, y, 0, endX, y, oR);
      grad.addColorStop(0, "hsla("+tl.hue+",90%,75%,"+(0.5+prob*0.5)+")"); grad.addColorStop(1, "transparent");
      ctx.fillStyle = grad; ctx.beginPath(); ctx.arc(endX, y, oR, 0, TAU); ctx.fill();
      ctx.fillStyle = "hsla("+tl.hue+",60%,85%,"+(0.5+prob)+")";
      ctx.font = "bold "+(11+prob*4)+"px "+FONT; ctx.textAlign = "left";
      ctx.fillText(tl.name, endX+oR+8, y);
      ctx.font = "11px "+FONT; ctx.fillStyle = "hsla("+tl.hue+",40%,70%,0.7)";
      ctx.fillText((prob*100).toFixed(1)+"% dE="+tl.dE, endX+oR+8, y+14);
    }
    const og = ctx.createRadialGradient(oX, H/2, 0, oX, H/2, 18);
    og.addColorStop(0, "rgba(255,255,255,0.8)"); og.addColorStop(0.5, "rgba(0,240,255,0.3)"); og.addColorStop(1, "transparent");
    ctx.fillStyle = og; ctx.beginPath(); ctx.arc(oX, H/2, 18, 0, TAU); ctx.fill();
    ctx.fillStyle = "#fff"; ctx.font = "bold 13px "+FONT; ctx.textAlign = "center"; ctx.fillText("NOW", oX, H/2+5);
  }, [eta, Fi, t]);
  useEffect(() => { draw(); }, [draw]);

  return (<div>
    <DeviceHeader name="Timeline Selector" subtitle="GKSL + consciousness-induced collapse as a branch-selection mechanism" color={P.green} classification="Thought Experiment" />
    <EqBlock color={P.green}>{"P(s_i) \u221D |\u27E8s_i|\u03A8\u27E9|\u00B2 \u00B7 [1 + \u03B7 \u00B7 F_i(\u03A6c, E)] \u2014 biased collapse"}</EqBlock>
    <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
      <div style={{ flex: "1 1 300px" }}>
        <canvas ref={ref} width={500} height={400} style={{ width: "100%", maxWidth: 500, borderRadius: 8, border: "1px solid "+P.border }} />
      </div>
      <div style={{ flex: "0 0 200px", minWidth: 180 }}>
        <Knob label={"\u03B7 (collapse bias)"} value={eta} onChange={setEta} min={-2} max={2} step={0.01} color={P.green} />
        <Knob label="F_i amplification" value={Fi} onChange={setFi} min={0} max={1} step={0.01} color={P.glow2} />
        <GlowBox color={P.green} glow>
          <span style={{ color: P.green, fontWeight: 700 }}>PRINCIPLE:</span> Fi measures how much each outcome increases \u03A6c and E. The GKSL container keeps things CPTP, but the bias selects timelines.<br /><br />
          <span style={{ color: P.glow3, fontWeight: 600 }}>{"\u03B7 > 0:"}</span> consciousness-enhancing<br />
          <span style={{ color: P.ember, fontWeight: 600 }}>{"\u03B7 < 0:"}</span> entropy-maximizing
        </GlowBox>
      </div>
    </div>
  </div>);
}

function JhanaEngine() {
  const ref = useRef(null);
  const [phiC, setPhiC] = useState(0.5);
  const [E, setE] = useState(0.5);
  const [gamma, setGamma] = useState(-0.5);
  const [t, setT] = useState(0);
  useEffect(() => { const id = setInterval(() => setT(p => p + 0.02), 30); return () => clearInterval(id); }, []);

  const draw = useCallback(() => {
    const cv = ref.current; if (!cv) return;
    const ctx = cv.getContext("2d"); const W = cv.width, H = cv.height;
    ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.void; ctx.fillRect(0, 0, W, H);
    const pL = 55, pR = 20, pT = 35, pB = 45, pW = W-pL-pR, pH = H-pT-pB, range = 3;
    for (let py = 0; py < pH; py += 3) for (let px = 0; px < pW; px += 3) {
      const phi = (px/pW)*range, e = (1-py/pH)*range;
      const V = 0.5*phi**2 + 0.15*phi**4 + 0.5*e**2 + 0.15*e**4 + gamma*phi**2*e;
      const norm = clamp((V+2)/6, 0, 1);
      const hue = V < 0 ? 280 : lerp(220, 30, norm);
      const light = V < 0 ? lerp(50, 25, clamp(-V/2, 0, 1)) : lerp(8, 35, norm);
      ctx.fillStyle = "hsl("+hue+",70%,"+light+"%)";
      ctx.fillRect(pL+px, pT+py, 3, 3);
    }
    const jhanas = [
      { name: "J1 Applied attention", phi: 0.8, e: 0.4 },
      { name: "J2 Rapture", phi: 1.2, e: 0.8 },
      { name: "J3 Contentment", phi: 1.6, e: 1.2 },
      { name: "J4 Equanimity", phi: 2.0, e: 1.8 },
    ];
    for (const j of jhanas) {
      const px = pL+(j.phi/range)*pW, py = pT+(1-j.e/range)*pH;
      const pulse = 0.5+0.5*Math.sin(t*3+j.phi);
      const grad = ctx.createRadialGradient(px, py, 0, px, py, 18+pulse*8);
      grad.addColorStop(0, "rgba(179,116,255,"+(0.6+pulse*0.3)+")"); grad.addColorStop(1, "transparent");
      ctx.fillStyle = grad; ctx.beginPath(); ctx.arc(px, py, 18+pulse*8, 0, TAU); ctx.fill();
      ctx.fillStyle = "#fff"; ctx.font = "bold 12px "+FONT; ctx.textAlign = "center";
      ctx.fillText(j.name, px, py+4);
    }
    const sxp = pL+(phiC/range)*pW, syp = pT+(1-E/range)*pH;
    ctx.fillStyle = P.glow; ctx.beginPath(); ctx.arc(sxp, syp, 7, 0, TAU); ctx.fill();
    ctx.strokeStyle = P.glow; ctx.lineWidth = 1.5; ctx.setLineDash([3,3]);
    ctx.beginPath(); ctx.arc(sxp, syp, 14+Math.sin(t*4)*3, 0, TAU); ctx.stroke(); ctx.setLineDash([]);
    ctx.strokeStyle = "rgba(255,255,255,0.25)"; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(pL, pT); ctx.lineTo(pL, pT+pH); ctx.lineTo(pL+pW, pT+pH); ctx.stroke();
    ctx.fillStyle = P.text; ctx.font = "12px "+FONT; ctx.textAlign = "center";
    ctx.fillText("\u03A6c \u2192", pL+pW/2, pT+pH+30);
    ctx.save(); ctx.translate(16, pT+pH/2); ctx.rotate(-Math.PI/2); ctx.fillText("E \u2191", 0, 0); ctx.restore();
    const V = 0.5*phiC**2+0.15*phiC**4+0.5*E**2+0.15*E**4+gamma*phiC**2*E;
    ctx.fillStyle = P.gold; ctx.font = "bold 12px "+FONT; ctx.textAlign = "right";
    ctx.fillText("V = "+V.toFixed(3), W-pR, pT+16);
  }, [phiC, E, gamma, t]);
  useEffect(() => { draw(); }, [draw]);

  return (<div>
    <DeviceHeader name={"Jh\u0101na Engine"} subtitle={"Navigate \u03A6c-E phase space attractors \u2014 meditative states as field configurations"} color={P.glow2} classification="Thought Experiment" />
    <EqBlock color={P.glow2}>{"V(\u03A6c,E) = \u00BDmc\u00B2\u03A6c\u00B2 + \u03BBc/4\u00B7\u03A6c\u2074 + \u00BDmE\u00B2E\u00B2 + \u03BBE/4\u00B7E\u2074 + \u03B3\u03A6c\u00B2E"}</EqBlock>
    <EqBlock color={P.glow3}>{"\u03B3 < 0 \u27F9 \u03A6c\u00B2E > 0 lowers energy \u2014 consciousness + ethics = stability"}</EqBlock>
    <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
      <div style={{ flex: "1 1 280px" }}>
        <canvas ref={ref} width={440} height={400} style={{ width: "100%", maxWidth: 440, borderRadius: 8, border: "1px solid "+P.border }} />
      </div>
      <div style={{ flex: "0 0 200px", minWidth: 180 }}>
        <Knob label={"\u03A6c (consciousness)"} value={phiC} onChange={setPhiC} min={0} max={2.5} step={0.01} color={P.glow2} />
        <Knob label="E (ethical field)" value={E} onChange={setE} min={0} max={2.5} step={0.01} color={P.glow3} />
        <Knob label={"\u03B3 (coupling)"} value={gamma} onChange={setGamma} min={-1.5} max={0.5} step={0.01} color={P.gold} />
        <GlowBox color={P.glow2} glow>
          <span style={{ color: P.glow2, fontWeight: 700 }}>PRINCIPLE:</span> {" Jh\u0101nas are attractors. With \u03B3<0, high consciousness + ethics = lowest energy."}<br /><br />
          Purple wells = attractors<br />
          <span style={{ color: P.glow, fontWeight: 600 }}>Cyan dot</span> = your current state<br />
          <span style={{ color: P.gold, fontWeight: 600 }}>Navigate toward J4</span>
        </GlowBox>
      </div>
    </div>
  </div>);
}

function TeleologicalAccelerator() {
  const ref = useRef(null);
  const [xi, setXi] = useState(0.001);
  const [timeCursor, setTimeCursor] = useState(50);

  const draw = useCallback(() => {
    const cv = ref.current; if (!cv) return;
    const ctx = cv.getContext("2d"); const W = cv.width, H = cv.height;
    ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.void; ctx.fillRect(0, 0, W, H);
    const pL = 55, pR = 20, pT = 35, pB = 45, pW = W-pL-pR, pH = H-pT-pB;
    const tMax = 100, dt = 0.1;
    const cfgs = [
      { xi: 0, color: P.faint, label: "\u03BE=0 (no teleology)" },
      { xi: xi*0.5, color: P.glow+"90", label: "\u03BE="+(xi*0.5).toFixed(4) },
      { xi: xi, color: P.gold, label: "\u03BE="+xi.toFixed(4)+" (active)" },
      { xi: xi*2, color: P.glow3, label: "\u03BE="+(xi*2).toFixed(4) },
    ];
    const trajs = cfgs.map(c => {
      let phi = 0.1, e = 0.1; const pts = [];
      for (let s = 0; s < tMax/dt; s++) {
        const dP = phi+0.6*phi**3-1.0*phi*e, dE = e+0.6*e**3-0.5*phi**2;
        phi += (-dP*0.01+c.xi+Math.sin(s*0.01)*0.001)*dt;
        e += (-dE*0.01+c.xi*0.5)*dt;
        phi = Math.max(0, phi); e = Math.max(0, e);
        pts.push({ t: s*dt, total: phi+e });
      }
      return pts;
    });
    const maxV = Math.max(...trajs.flatMap(tr => tr.map(p => p.total)), 1);
    ctx.strokeStyle = "rgba(255,255,255,0.2)"; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(pL, pT); ctx.lineTo(pL, pT+pH); ctx.lineTo(pL+pW, pT+pH); ctx.stroke();
    ctx.font = "11px "+FONT; ctx.fillStyle = P.dim; ctx.textAlign = "right";
    for (let v = 0; v <= 1; v += 0.25) {
      const py = pT+pH*(1-v); ctx.fillText((v*maxV).toFixed(1), pL-6, py+4);
      ctx.strokeStyle = P.ghost+"40"; ctx.beginPath(); ctx.moveTo(pL, py); ctx.lineTo(pL+pW, py); ctx.stroke();
    }
    for (let ti = 0; ti < trajs.length; ti++) {
      const tr = trajs[ti]; ctx.strokeStyle = cfgs[ti].color; ctx.lineWidth = ti===2?3:1.2;
      ctx.beginPath();
      for (let i = 0; i < tr.length; i += 3) {
        const x = pL+(tr[i].t/tMax)*pW, y = pT+pH*(1-tr[i].total/maxV);
        i===0?ctx.moveTo(x, y):ctx.lineTo(x, y);
      }
      ctx.stroke();
    }
    ctx.font = "11px "+FONT; ctx.textAlign = "left";
    for (let i = 0; i < cfgs.length; i++) {
      ctx.fillStyle = cfgs[i].color;
      ctx.fillRect(pL+10, pT+8+i*18, 10, 10);
      ctx.fillText(cfgs[i].label, pL+26, pT+17+i*18);
    }
    const cx = pL+(timeCursor/100)*pW;
    ctx.strokeStyle = "rgba(255,255,255,0.3)"; ctx.setLineDash([4,4]);
    ctx.beginPath(); ctx.moveTo(cx, pT); ctx.lineTo(cx, pT+pH); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = P.text; ctx.font = "12px "+FONT; ctx.textAlign = "center";
    ctx.fillText("Cosmic time \u2192", pL+pW/2, pT+pH+32);
    ctx.save(); ctx.translate(16, pT+pH/2); ctx.rotate(-Math.PI/2); ctx.fillText("\u03A6c + E (total)", 0, 0); ctx.restore();
  }, [xi, timeCursor]);
  useEffect(() => { draw(); }, [draw]);

  return (<div>
    <DeviceHeader name="Teleological Accelerator" subtitle={"Amplify the universe's \u03BE-bias toward consciousness and ethical realization"} color={P.gold} classification="Thought Experiment" />
    <EqBlock color={P.gold}>{"L_teleology = +\u03BE \u00B7 f(\u03A6c, E) \u2014 gentle push toward higher consciousness"}</EqBlock>
    <EqBlock color={P.ember}>{"\u03BE breaks T-symmetry: the cosmos acquires a direction toward \u03A6c\u2191 E\u2191"}</EqBlock>
    <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
      <div style={{ flex: "1 1 300px" }}>
        <canvas ref={ref} width={500} height={380} style={{ width: "100%", maxWidth: 500, borderRadius: 8, border: "1px solid "+P.border }} />
      </div>
      <div style={{ flex: "0 0 200px", minWidth: 180 }}>
        <Knob label={"\u03BE (teleological coupling)"} value={xi} onChange={setXi} min={0} max={0.05} step={0.0001} color={P.gold} />
        <Knob label="Time cursor" value={timeCursor} onChange={setTimeCursor} min={0} max={100} step={1} color={P.dim} />
        <GlowBox color={P.gold} glow>
          <span style={{ color: P.gold, fontWeight: 700 }}>PRINCIPLE:</span> {" L_teleology = +\u03BE\u00B7f(\u03A6c,E) breaks time-reversal symmetry."}<br /><br />
          <span style={{ color: P.ember, fontWeight: 600 }}>{"\u03BE = 0:"}</span> fields decay<br />
          <span style={{ color: P.gold, fontWeight: 600 }}>{"\u03BE > 0:"}</span> monotonic consciousness rise
        </GlowBox>
      </div>
    </div>
  </div>);
}

function QualionChamber() {
  const ref = useRef(null);
  const [nSeed, setNSeed] = useState(12);
  const [coherent, setCoherent] = useState(false);
  const [coupling, setCoupling] = useState(0.5);
  const [t, setT] = useState(0);
  const particles = useRef([]);
  const stats = useRef({ qualions: 0, ethions: 0, conversions: 0 });

  const resetParticles = useCallback((n) => {
    particles.current = [];
    for (let i = 0; i < n; i++) {
      particles.current.push({
        x: 220+(Math.random()-0.5)*240, y: 195+(Math.random()-0.5)*240,
        vx: (Math.random()-0.5)*2, vy: (Math.random()-0.5)*2,
        phase: Math.random()*TAU, type: "qualion", age: 0, alive: true,
      });
    }
    stats.current = { qualions: n, ethions: 0, conversions: 0 };
  }, []);

  useEffect(() => { resetParticles(nSeed); }, [nSeed, resetParticles]);

  useEffect(() => {
    const id = setInterval(() => {
      setT(p => p + 0.03);
      const pts = particles.current;
      const cx = 220, cy = 195;
      const alive = pts.filter(p => p.alive);
      for (const p of alive) {
        p.age++; p.phase += 0.05;
        if (coherent) {
          const dx = cx-p.x, dy = cy-p.y, dist = Math.sqrt(dx*dx+dy*dy)+0.1;
          p.vx += dx/dist*0.08*coupling; p.vy += dy/dist*0.08*coupling;
        } else {
          p.vx += (Math.random()-0.5)*0.25; p.vy += (Math.random()-0.5)*0.25;
        }
        p.vx *= 0.96; p.vy *= 0.96; p.x += p.vx; p.y += p.vy;
        const dx = p.x-cx, dy = p.y-cy, dist = Math.sqrt(dx*dx+dy*dy);
        if (dist > 155) { p.x = cx+dx/dist*154; p.y = cy+dy/dist*154; p.vx *= -0.5; p.vy *= -0.5; }
      }
      const qualions = alive.filter(p => p.type === "qualion");
      for (let i = 0; i < qualions.length; i++) {
        for (let j = i+1; j < qualions.length; j++) {
          const a = qualions[i], b = qualions[j];
          if (!a.alive || !b.alive) continue;
          const dx = a.x-b.x, dy = a.y-b.y, dist = Math.sqrt(dx*dx+dy*dy);
          const convProb = coupling * 0.005 * Math.max(0, 1 - dist/40);
          if (Math.random() < convProb) {
            a.alive = false; b.alive = false;
            pts.push({
              x: (a.x+b.x)/2, y: (a.y+b.y)/2,
              vx: (a.vx+b.vx)*0.3, vy: (a.vy+b.vy)*0.3,
              phase: Math.random()*TAU, type: "ethion", age: 0, alive: true,
            });
            stats.current.conversions++;
          }
        }
      }
      const ethions = alive.filter(p => p.type === "ethion");
      for (const e of ethions) {
        if (!e.alive) continue;
        const decayProb = 0.002;
        if (e.age > 40 && Math.random() < decayProb) {
          e.alive = false;
          for (let k = 0; k < 2; k++) {
            pts.push({
              x: e.x+(Math.random()-0.5)*20, y: e.y+(Math.random()-0.5)*20,
              vx: (Math.random()-0.5)*3, vy: (Math.random()-0.5)*3,
              phase: Math.random()*TAU, type: "qualion", age: 0, alive: true,
            });
          }
        }
      }
      const aliveNow = pts.filter(p => p.alive);
      stats.current.qualions = aliveNow.filter(p => p.type === "qualion").length;
      stats.current.ethions = aliveNow.filter(p => p.type === "ethion").length;
      if (pts.length > 200) particles.current = pts.filter(p => p.alive);
    }, 30);
    return () => clearInterval(id);
  }, [coherent, coupling]);

  const draw = useCallback(() => {
    const cv = ref.current; if (!cv) return;
    const ctx = cv.getContext("2d"); const W = cv.width, H = cv.height;
    ctx.clearRect(0, 0, W, H);
    const bg = ctx.createRadialGradient(W/2, H/2, 0, W/2, H/2, W*0.5);
    bg.addColorStop(0, "#0a0818"); bg.addColorStop(1, P.void);
    ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);
    const cX = 220, cY = 195;
    ctx.strokeStyle = P.ghost; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.arc(cX, cY, 160, 0, TAU); ctx.stroke();
    const alive = particles.current.filter(p => p.alive);
    for (let i = 0; i < alive.length; i++) for (let j = i+1; j < alive.length; j++) {
      const dx = alive[i].x-alive[j].x, dy = alive[i].y-alive[j].y, dist = Math.sqrt(dx*dx+dy*dy);
      if (dist < 70*coupling) {
        const alpha = (1-dist/(70*coupling))*0.35;
        const cross = alive[i].type !== alive[j].type;
        ctx.strokeStyle = cross ? "rgba(255,149,51,"+alpha+")" : "rgba(0,240,255,"+alpha+")";
        ctx.lineWidth = cross ? 1 : 0.5;
        ctx.beginPath(); ctx.moveTo(alive[i].x, alive[i].y); ctx.lineTo(alive[j].x, alive[j].y); ctx.stroke();
      }
    }
    for (const p of alive) {
      const isQ = p.type === "qualion";
      const hue = isQ ? 185 : 30;
      const pulse = 0.5+0.5*Math.sin(p.phase);
      const r = isQ ? 5+pulse*3 : 6+pulse*4;
      const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, r*2.5);
      grad.addColorStop(0, "hsla("+hue+",90%,75%,"+(0.7+pulse*0.3)+")");
      grad.addColorStop(0.4, "hsla("+hue+",85%,55%,0.3)"); grad.addColorStop(1, "transparent");
      ctx.fillStyle = grad; ctx.beginPath(); ctx.arc(p.x, p.y, r*2.5, 0, TAU); ctx.fill();
      ctx.fillStyle = "hsla("+hue+",90%,85%,0.95)";
      ctx.beginPath(); ctx.arc(p.x, p.y, r*0.5, 0, TAU); ctx.fill();
    }
    const s = stats.current;
    ctx.fillStyle = P.panel+"e0"; ctx.fillRect(W-175, 10, 165, 85);
    ctx.strokeStyle = P.border; ctx.strokeRect(W-175, 10, 165, 85);
    ctx.font = "bold 13px "+FONT; ctx.textAlign = "left";
    ctx.fillStyle = P.glow; ctx.fillText("Qualions: "+s.qualions, W-163, 32);
    ctx.fillStyle = P.ember; ctx.fillText("Ethions: "+s.ethions, W-163, 52);
    ctx.fillStyle = P.gold; ctx.fillText("Fusions: "+s.conversions, W-163, 72);
    ctx.fillStyle = P.text; ctx.font = "11px "+FONT; ctx.fillText("Total: "+(s.qualions+s.ethions), W-163, 90);
    ctx.fillStyle = P.glow; ctx.font = "bold 12px "+FONT; ctx.textAlign = "left";
    ctx.fillText("\u25CF Qualions (\u03A6c quanta)", 12, H-28);
    ctx.fillStyle = P.ember; ctx.fillText("\u25CF Ethions (E quanta)", 12, H-10);
    ctx.fillStyle = coherent ? P.green : P.dim;
    ctx.font = "bold 12px "+FONT; ctx.textAlign = "right";
    ctx.fillText(coherent ? "\u25C9 COHERENT" : "\u25CB THERMAL", W-12, H-12);
  }, [t, coherent, coupling]);
  useEffect(() => { draw(); }, [draw]);

  return (<div>
    <DeviceHeader name="Qualion Resonance Chamber" subtitle={"Watch qualions fuse into ethions via \u03B3\u03A6c\u00B2E coupling \u2014 consciousness creates ethics"} color={P.ember} classification="Thought Experiment" />
    <EqBlock color={P.glow}>{"\u03A6\u0303c(x) = \u222B d\u00B3k/\u221A(2\u03C9k) [a\u2096 e\u207B\u2071\u1D4F\u02E3 + a\u2096\u2020 e\u2071\u1D4F\u02E3] \u2014 qualion mode expansion"}</EqBlock>
    <EqBlock color={P.ember}>{"\u03B3\u03A6c\u00B2E: two qualions \u2192 one ethion (+ reverse decay). Now with live generation!"}</EqBlock>
    <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
      <div style={{ flex: "1 1 280px" }}>
        <canvas ref={ref} width={440} height={420} style={{ width: "100%", maxWidth: 440, borderRadius: 8, border: "1px solid "+P.border }} />
      </div>
      <div style={{ flex: "0 0 200px", minWidth: 180 }}>
        <Knob label="Initial qualions" value={nSeed} onChange={v => setNSeed(Math.round(v))} min={2} max={30} step={1} color={P.glow} />
        <Knob label={"\u03B3 coupling"} value={coupling} onChange={setCoupling} min={0.1} max={2} step={0.05} color={P.ember} />
        <div style={{ marginBottom: 10 }}>
          <button type="button" onClick={() => setCoherent(!coherent)} style={{
            width: "100%", padding: "10px", background: coherent ? P.glow2+"20" : "transparent",
            border: "1px solid "+(coherent ? P.glow2 : P.border), borderRadius: 6,
            color: coherent ? P.glow2 : P.dim, fontSize: 12, cursor: "pointer", fontFamily: FONT, fontWeight: 600,
          }}>{coherent ? "\u25C9 COHERENT MODE ON" : "\u25CB ACTIVATE COHERENCE"}</button>
        </div>
        <div style={{ marginBottom: 10 }}>
          <button type="button" onClick={() => resetParticles(nSeed)} style={{
            width: "100%", padding: "10px", background: "transparent",
            border: "1px solid "+P.border, borderRadius: 6,
            color: P.dim, fontSize: 12, cursor: "pointer", fontFamily: FONT,
          }}>{"\u21BB RESET CHAMBER"}</button>
        </div>
        <GlowBox color={P.ember} glow>
          <span style={{ color: P.ember, fontWeight: 700 }}>FIXED:</span> Qualions now actively fuse into ethions on collision. Ethions decay back into qualion pairs, creating an ongoing cycle.<br /><br />
          Even with 2 qualions: they collide {"\u2192"} ethion {"\u2192"} decays back {"\u2192"} 2 qualions {"\u2192"} repeat.<br /><br />
          <span style={{ color: P.glow2, fontWeight: 600 }}>Coherent mode</span> pulls everything inward, dramatically boosting collision rate.
        </GlowBox>
      </div>
    </div>
  </div>);
}

const DEVICES = [
  { id: "sculptor", label: "Probability Sculptor", color: P.glow, comp: ProbabilitySculptor },
  { id: "fold", label: "Fold-Space Engine", color: P.glow2, comp: FoldSpaceEngine },
  { id: "timeline", label: "Timeline Selector", color: P.green, comp: TimelineSelector },
  { id: "jhana", label: "Jh\u0101na Engine", color: P.glow3, comp: JhanaEngine },
  { id: "teleology", label: "Teleological Accelerator", color: P.gold, comp: TeleologicalAccelerator },
  { id: "qualion", label: "Qualion Chamber", color: P.ember, comp: QualionChamber },
];

export default function App() {
  const [active, setActive] = useState("sculptor");
  const Comp = DEVICES.find(d => d.id === active).comp;

  return (
    <div style={{ minHeight: "100vh", background: P.void, color: P.text, fontFamily: FONT, position: "relative", overflow: "hidden" }}>
      <div style={{ position: "relative", zIndex: 1, padding: "20px 18px" }}>
        <div style={{ marginBottom: 18 }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 12, flexWrap: "wrap" }}>
            <h1 style={{ margin: 0, fontSize: 22, fontWeight: 700, color: "#fff", fontFamily: "'Georgia', serif" }}>Fold-Space Engine</h1>
            <span style={{ fontSize: 11, color: P.glow, letterSpacing: "0.1em", textTransform: "uppercase", fontWeight: 600 }}>Internal Primary · MQGT\u2013SCF interactive lab</span>
          </div>
          <div style={{ fontSize: 12, color: P.dim, marginTop: 4, maxWidth: 720, lineHeight: 1.6 }}>
            {"Internal primary surface: Probability Sculptor visualizes \u03b7-tilted branch weighting. Companion panels explore Fold-Space contraction, timeline selection, \u03A6c\u2013E landscapes, teleology, and qualion dynamics. Grounded in MQGT\u2013SCF notation by C. M. Baird. "}
            <span style={{ color: P.ember, fontWeight: 600 }}>Illustrative software; not a hardware claim.</span>
          </div>
          <div style={{ height: 1, background: "linear-gradient(90deg, "+P.glow+"40, "+P.glow2+"25, "+P.gold+"18, transparent)", marginTop: 12 }} />
        </div>
        <div style={{ display: "flex", gap: 5, marginBottom: 16, flexWrap: "wrap" }}>
          {DEVICES.map(d => (
            <button type="button" key={d.id} onClick={() => setActive(d.id)} style={{
              padding: "8px 14px", background: active === d.id ? d.color+"12" : "transparent",
              border: "1px solid "+(active === d.id ? d.color : P.border), borderRadius: 5,
              color: active === d.id ? d.color : P.dim, fontSize: 12, fontFamily: FONT,
              cursor: "pointer", transition: "all 0.2s", whiteSpace: "nowrap",
              fontWeight: active === d.id ? 600 : 400,
            }}>{d.label}</button>
          ))}
        </div>
        <div style={{ background: P.panel, borderRadius: 10, border: "1px solid "+P.border, padding: "18px" }}>
          <Comp />
        </div>
        <div style={{ marginTop: 16, textAlign: "center" }}>
          <div style={{ fontSize: 11, color: P.faint, letterSpacing: "0.04em", lineHeight: 1.7 }}>
            {"GROUNDING: S_core (Eq.2) \u00B7 GKSL (Eq.18) \u00B7 Measure tilt (Eq.21) \u00B7 Yukawa kernel (Eq.16) \u00B7 L_teleology \u00B7 Qualion quantization"}
          </div>
          <div style={{ fontSize: 11, color: P.dim, marginTop: 5, fontStyle: "italic" }}>
            {'"The value of the anchor paper lies exactly in this reduction. If the framework fails, it can fail quantitatively." \u2014 C. M. Baird, 2026'}
          </div>
        </div>
      </div>
    </div>
  );
}
