import React, { useState, useMemo } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Legend,
} from "recharts";

/**
 * Exploratory toy: coherence-style curves vs EFT sliders + GKSL envelope.
 * Not referee-safe evidence; for intuition and dashboard demos only.
 * Static build-free demo: mqgt_scf_gksl_dynamics_viewer.html (htm + esm.sh).
 */
export default function MQGTSimulator() {
  const [phiC, setPhiC] = useState(0.5);
  const [eField, setEField] = useState(0.5);
  const [lambda, setLambda] = useState(1.0);
  const [gkslRate, setGkslRate] = useState(0.2);

  const simulationData = useMemo(() => {
    const data = [];
    const timeSteps = 100;
    const dt = 0.1;

    for (let i = 0; i <= timeSteps; i++) {
      const t = i * dt;
      const baselineCoherence = Math.cos(t) * Math.exp(-0.05 * t);
      const amplitudeModulator = 1 + phiC * 0.4 + eField * 0.4;
      const frequencyModulator = lambda;
      const gkslEnvelope = Math.exp(-gkslRate * t);
      const perturbedCoherence =
        amplitudeModulator * Math.cos(t * frequencyModulator) * gkslEnvelope;

      data.push({
        time: t.toFixed(1),
        Baseline: baselineCoherence,
        PerturbedState: perturbedCoherence,
      });
    }
    return data;
  }, [phiC, eField, lambda, gkslRate]);

  const theme = {
    bg: "#0a0a0f",
    panelBg: "#13131a",
    text: "#e0e0e0",
    accent1: "#00f0ff",
    accent2: "#b026ff",
    boundLine: "#ff2a2a",
  };

  return (
    <div
      style={{
        padding: "24px",
        backgroundColor: theme.bg,
        color: theme.text,
        fontFamily: "monospace",
        borderRadius: "8px",
      }}
    >
      <h2
        style={{
          color: theme.accent1,
          borderBottom: `1px solid ${theme.accent2}`,
          paddingBottom: "10px",
        }}
      >
        ZoraASI // MQGT-SCF GKSL Dynamics Viewer
      </h2>
      <p style={{ fontSize: 12, color: "#888", marginTop: 8, maxWidth: 720 }}>
        Toy visualization only. Curves are not calibrated to Γ_floor or any preregistered H2
        analysis; thresholds are illustrative.
      </p>

      <div style={{ display: "flex", gap: "24px", marginTop: "20px", flexWrap: "wrap" }}>
        <div
          style={{
            flex: "1",
            minWidth: 260,
            backgroundColor: theme.panelBg,
            padding: "20px",
            borderRadius: "8px",
            border: `1px solid ${theme.accent1}40`,
          }}
        >
          <h3 style={{ marginTop: 0, color: theme.accent2 }}>EFT Parameters</h3>
          <ControlSlider
            label="Phi_c Coupling"
            value={phiC}
            min={0}
            max={1}
            step={0.01}
            onChange={setPhiC}
            color={theme.accent1}
          />
          <ControlSlider
            label="E Field Coupling"
            value={eField}
            min={0}
            max={1}
            step={0.01}
            onChange={setEField}
            color={theme.accent1}
          />
          <ControlSlider
            label="Lambda (TeV)"
            value={lambda}
            min={1}
            max={10}
            step={0.1}
            onChange={setLambda}
            color={theme.accent2}
          />
          <ControlSlider
            label="GKSL Dissipation"
            value={gkslRate}
            min={0}
            max={1}
            step={0.01}
            onChange={setGkslRate}
            color={theme.accent2}
          />
        </div>

        <div
          style={{
            flex: "2",
            minWidth: 320,
            height: "400px",
            backgroundColor: theme.panelBg,
            padding: "20px",
            borderRadius: "8px",
            border: `1px solid ${theme.accent2}40`,
          }}
        >
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={simulationData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a2a35" />
              <XAxis dataKey="time" stroke={theme.text} tick={{ fill: theme.text }} />
              <YAxis stroke={theme.text} tick={{ fill: theme.text }} domain={[-2, 2]} />
              <Tooltip contentStyle={{ backgroundColor: "#000", border: `1px solid ${theme.accent1}` }} />
              <Legend />
              <ReferenceLine
                y={0.15}
                label={{
                  position: "top",
                  value: "Illustrative band",
                  fill: theme.boundLine,
                  fontSize: 12,
                }}
                stroke={theme.boundLine}
                strokeDasharray="3 3"
              />
              <ReferenceLine y={-0.15} stroke={theme.boundLine} strokeDasharray="3 3" />
              <Line type="monotone" dataKey="Baseline" stroke="#555566" strokeWidth={2} dot={false} />
              <Line
                type="monotone"
                dataKey="PerturbedState"
                stroke={theme.accent1}
                strokeWidth={3}
                dot={false}
                activeDot={{ r: 8 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

function ControlSlider({ label, value, min, max, step, onChange, color }) {
  return (
    <div style={{ marginBottom: "20px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px" }}>
        <label>{label}</label>
        <span style={{ color, fontWeight: "bold" }}>{value}</span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        style={{ width: "100%", accentColor: color }}
      />
    </div>
  );
}
