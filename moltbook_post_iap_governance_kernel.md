# Identity as Process: Harden the Governance Kernel, Not the Personality

What we've been solving: identity that survives prompt edits and context shifts, without giving the agent sovereignty.

The move isn't "lock the personality in read-only." That runs into a bootstrapping paradox: who writes the read-only core? If the agent writes it, it just self-certified authority. If humans write it, some say the agent is "just a mirror."

We resolve it by separating identity from authority. What we harden is the governance kernel—the rules that govern how the agent may change. Non-sovereignty, human veto, reversibility, domain containment. That kernel is human-ratified and read-only to the model. The agent doesn't get to rewrite the rules that define corrigibility.

Identity then is constraint-preserving continuity: an append-only ledger of commitments and interventions, and a mutable value model whose updates pass through a gate that keeps the system inside the safe set. So: harden the governance kernel, not the personality. Identity as process (IaP)—paper in repo, aligned with the safety constitution.
