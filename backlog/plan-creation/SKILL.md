---
name: plan-creation
description: Create clear, implementation-ready plans with a goal, success criteria, summary, phases, and risks. Use when the user asks for a plan, implementation plan, execution plan, proposed plan, migration plan, rollout plan, or similar planning artifact before coding. Also use before outputting a proposed implementation plan or proposed_plan block due to active collaboration mode.
---

# Plan Creation

## Trigger Guard

Use this skill before presenting any implementation, execution, proposed, or `<proposed_plan>` plan.

## Workflow

Use this as the required output shape for every plan.

Every plan must include:

- Goal: target outcome.
- What Success Looks Like: proof the goal is done. Weak: "Implement the plan." Strong: real outcome, behavior, validation, or user result.
- Summary: short approach and why.
- Phases: ordered chunks with validation.
- Risks & notes: blockers, unknowns, safety issues, or follow-ups.

## Phase Design

Before presenting the plan, break it into small phases. Each phase should build on the previous one. Prefer iterative, testable changes over large rewrites.

Refine phases until they are sequential, incremental, and right-sized for safe implementation and validation.

The final plan should be implementation-ready: a developer can follow it without guessing order or validation.
