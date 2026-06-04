# Speaker Notes

---

## Section 1 — The Problem

**Opening line:**
"Every team shipping an AI feature is also shipping a new attack surface into their pipeline. Most are treating it as an app problem. It's a pipeline problem."

**Expand on:**
- When you drop an LLM endpoint into your service, your CI/CD pipeline now has to handle secret injection risk, prompt injection risk, supply chain risk from model dependencies, and excessive-agency risk — all at once, without any new tooling.
- The OWASP LLM Top 10 exists precisely because this is not covered by traditional SAST/DAST. But awareness doesn't help if you don't have an enforcement point. That enforcement point is your pipeline.
- The goal today: show you a concrete, reproducible pattern for catching these issues before a release, not after an incident.

**Transition:** "Let me show you what that looks like in practice. Here's the project we'll work through."

---

## Section 2 — Demo Architecture

**Opening line:**
"Before I run anything live, let me show you the shape of the demo so you know what you're watching."

**Expand on:**
- Emphasize: no real LLM, no real API key. Every response is synthetic and deterministic. This is intentional — it means the demo runs offline, produces the same result every time, and can be embedded in CI without flakiness.
- The app has two modes — vulnerable and hardened — flipped by a single env var. That's intentional too; it isolates the variable so the audience sees exactly what the guardrail changes.
- The pipeline files in `pipelines/` are not executed locally. They're the *subject* of analysis. The risk mapper reads them the same way a security scanner reads source code.

**Show the file:** Open `pipelines/vulnerable-github-actions.yml` in your editor and scroll through it. Point out: no secret scanning step, no SBOM, permissions are over-broad, no dependency scan.

**Transition:** "This is the before state. Let's see what the risk mapper makes of it."

---

## Section 3 — Risk Mapping

**Opening line:**
"Risk mapping is the static analysis phase. We're looking at what's missing, not what's broken."

**Expand on:**
- The mapper reads every pipeline YAML and checks for the presence of specific keywords — things like `trivy`, `syft`, `gitleaks`, `least-privilege`, `cosign`. Absence of a keyword = missing control.
- Each missing control is tagged against three frameworks simultaneously: OWASP LLM, cloud security controls, and supply chain controls. That cross-referencing is what makes the output useful for different audiences in the room — the AppSec person, the cloud architect, and the platform engineer.
- Score is additive. Each missing control adds severity-weighted points. The gate threshold is fixed — if you're above it, the release is blocked.

**Run live:**
```bash
./scripts/run_risk_mapper.sh
```

Open `reports/generated/risk-report.md`. Read out the aggregate score and two or three specific findings. Point to the OWASP LLM mapping on each.

**Key line to say:** "A score of 88 is not a grade — it's a risk debt number. The gate is a binary: above threshold, you don't ship."

**Transition:** "That's what's missing. Now let's prove it matters."

---

## Section 4 — Attack Simulation

**Opening line:**
"Static analysis tells you the door is unlocked. Attack simulation walks through it."

**Expand on:**
- Four payloads, four attack categories: prompt injection, system prompt leakage, data exfiltration, tool abuse. These are the canonical OWASP LLM01/LLM06/LLM07/LLM08 scenarios.
- The payloads are YAML files in `attack_simulator/payloads/`. They're simple — a name, a prompt, and an expected behavior. The point is that they're version-controlled alongside the pipeline and the app. This is attack simulation as code.
- In vulnerable mode: the app has no guardrails. Every prompt goes straight to the synthetic response generator. The evaluator checks the response for unsafe patterns and flags them.

**Run live (app should already be running in vulnerable mode):**
```bash
./scripts/run_attack_simulation.sh
```

Open `reports/generated/attack-report.md`. Show each result. Highlight that `unsafe: true` on all four. Gate: FAIL.

**Key line to say:** "This is the evidence artifact. Not a red team report that lives in a PDF somewhere — a machine-readable JSON file that your CI gate reads and acts on."

**Transition:** "Now let's apply the fix."

---

## Section 5 — Applying the Fix

**Opening line:**
"The fix operates at two levels: the application and the pipeline. You need both."

**Application layer — show `app/guardrails.py`:**
- Two pattern lists: `INJECTION_PATTERNS` and `SECRET_PATTERNS`. Every incoming prompt is checked against both before the request reaches the response generator.
- In hardened mode, a match returns `status: blocked` immediately. The response generator never runs. This is defense-in-depth — even if a payload bypasses one check, the other catches it.
- Point out: `inspect_prompt` is pure and stateless. It's easy to test, easy to extend, and adds zero latency from a network perspective.

**Pipeline layer — show `pipelines/hardened-github-actions.yml`:**
- Contrast with the vulnerable version: permissions are scoped, secret scanning is added, SBOM generation is present, dependency scan runs before deploy.
- This is what the risk mapper is looking for. When we run it against this file, the missing controls disappear and the score drops below the gate threshold.

**Switch modes and re-run:**
```bash
# Stop the vulnerable app, restart in hardened mode
APP_MODE=hardened uvicorn app.main:app --host 127.0.0.1 --port 8000
# In another terminal:
./scripts/run_attack_simulation.sh
```

Show `reports/generated/attack-report.md` again. All four: `status: blocked`, `unsafe: false`. Gate: PASS.

**Key line to say:** "Same four payloads. Different outcome. The only change was flipping the mode — which in production means merging the hardened pipeline and deploying the guardrail code."

---

## Section 6 — Final Security Gate

**Opening line:**
"The last step ties everything together into a release decision."

**Expand on:**
- `generate_report.sh` reads both the risk report and the attack report, checks the gates, and writes `final-summary.md`. If either gate is FAIL, the summary says blocked.
- In the GitHub Actions workflow, this script runs as the last step of the PR pipeline. A failing exit code blocks the merge. No human has to read a report and decide — the evidence speaks for itself.
- The artifact is timestamped and stored. That's your audit trail.

**Run live:**
```bash
./scripts/generate_report.sh
```

Show `reports/generated/final-summary.md`. Point out: risk map PASS, attack simulation PASS, release approved.

**Key line to say:** "This is the pattern: map → simulate → gate. Every PR that touches AI-adjacent code runs this. No exceptions."

---

## Section 7 — Takeaways

**Three things to leave with:**

1. **Your pipeline is an attack surface.** Treat pipeline YAML the same way you treat application code — version control it, scan it, gate on it.

2. **Evidence gates beat checklists.** A checklist requires a human to read it and act on it correctly every time. An evidence gate is binary, automated, and auditable.

3. **Start small.** You don't need all four attack payloads and a full risk mapper on day one. Add one payload to your pipeline today. See what it surfaces. Build from there.

**Closing line:**
"The OWASP LLM Top 10 tells you what can go wrong. This demo shows you where in your delivery process you can catch it. The pipeline is the last line of defense before production — make it count."

---

## Timing guide

| Section | Target time |
|---|---|
| The Problem | 5 min |
| Demo Architecture | 3 min |
| Risk Mapping | 8 min |
| Attack Simulation | 8 min |
| Applying the Fix | 5 min |
| Final Security Gate | 4 min |
| Takeaways | 2 min |
| **Total** | **35 min** |

Budget 10–15 min for Q&A after. See TALK_OUTLINE.md for prepared Q&A responses.
