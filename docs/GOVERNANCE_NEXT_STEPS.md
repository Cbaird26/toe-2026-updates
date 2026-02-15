# Governance next steps (multi-agent Auth)

Short doc on how authorization (Auth) is currently defined in the stack, the gap for multi-agent swarms, and one concrete next step.

---

## How Auth is currently defined

- **Execution set:** U_exec = U_requested ∩ U_safe ∩ U_authorized. An action is executed only if it is requested, keeps the system in the safe set K (barrier B ≥ 0), and is **authorized**.
- **Who authorizes:** In the current docs, authorization is human-ratified: the human retains final authority (SAFETY_CONSTITUTION, ALIGN_ALL). The governance kernel (IaP: ICK, AIL, MVM, ENL) ensures the agent cannot self-certify sovereignty; updates and goal changes are accepted from authorized humans.
- **Consent:** Consent and “authorized” are implied to be determined by the human-in-the-loop (e.g. Exit step in PRAE: “Authority stays with you; no auto-post without your approval”). There is no formal predicate yet that defines *which* human or role can authorize *which* action in a multi-agent setting.

---

## Gap for multi-agent swarms

When multiple agents (or multiple humans + agents) act in the same system, **U_authorized** must be defined over a set of actors and roles: who can authorize what, under what conditions, and how conflicts are resolved. Currently:

- Single human “you” is the authority; agents request, human approves.
- No explicit model for: multiple humans (e.g. lab lead vs. experimenter), multiple agents with different scopes, or delegation chains (human authorizes agent A to approve agent B’s actions within scope X).

So the gap is: **Auth predicates for multi-agent swarms** — i.e. a formal or semi-formal definition of U_authorized when there are multiple authorizers and multiple actors.

---

## One concrete next step

- **Option A:** Extend **mqgt-scf-thesis** (or the ToE thesis companion) with a short subsection on “Multi-agent Auth and U_authorized”: define a minimal role set (e.g. Authority, Delegate, Executor) and a rule such as “U_authorized = actions approved by Authority or by a Delegate within a scope approved by Authority.” Document this in the thesis or in a spine repo so the formalism and the implementation stack stay aligned.
- **Option B:** In **ALIGNMENT_APPENDIX.md**, add a subsection “Auth predicates” that states the same: who can authorize what; how U_authorized is computed when multiple agents/humans are present; and that implementation (e.g. in ZoraASI or future swarms) must satisfy these predicates before an action is in U_exec.

Either option gives a single, citable next step to close the governance gap without implementing full swarm logic in code yet.
