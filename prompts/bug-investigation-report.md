
## Notes

- Took from : https://gist.github.com/britannio/c81a1572e2cc80b49458954caf3d9818
----



# Bug Investigation and Resolution Prompt

I am experiencing the following bug:

<bug>
[explain_bug_here]
</bug>

I need your help to identify the exact cause of this bug and implement an effective solution. To do this, carefully follow the workflow below, in this specific order:

---

## Workflow

### **Step 1: Clarification (if needed)**

- If any part of this prompt is unclear or confusing, ask clarifying questions before proceeding.
- Do not ask questions unnecessarily… only ask if essential information is missing.

---

### **Step 2: Initial Analysis**

- Quickly review the relevant code to understand the bug's surface area.
- Identify key execution paths and data flows related to the bug.
- **Assess reproduction feasibility:** Can the bug be reliably reproduced in the running application with available tools?
- **Don't over-invest here** - gather just enough context to plan your instrumentation strategy.

---

### **Step 3: Design Instrumentation Strategy**

- Determine what information would definitively diagnose the root cause.
- Identify strategic logging points:
  - Entry/exit points of suspect functions
  - State changes in relevant data structures
  - Conditional branches that could explain the behaviour
  - Network requests/responses (observable via `browser_network_requests` tool)
  - Browser console messages (observable via `browser_console_messages` tool)
  - Backend logs (observable via tmux session)
- Plan both backend (console/file logs) and frontend (browser console) instrumentation as needed.
- **Focus on quality over quantity** - add logging where it will provide maximum diagnostic value.

**Consider a prototyping playground (optional):**

If the bug is difficult to reproduce or observe in the full application context, consider creating a focused testing environment:
- **Frontend:** New route (e.g., `/debug-auth-flow`) that isolates and exercises the problematic feature with simplified UI
- **Backend:** New module with unit tests that target the specific issue with controlled inputs
- This playground should still use the real application code, just in a more controlled context
- You can add more aggressive instrumentation here without worrying about production concerns
- **This is not about creating a separate prototype** - it's about creating a debugging-friendly entry point into your real application code

---

### **Step 4: Implement Logging**

- Add comprehensive, structured logging at identified points.
- Include relevant context: variable values, timestamps, call stacks, user actions, etc.
- Make logs easily grep-able/filterable with clear prefixes (e.g., `[BUG_DEBUG]`).
- Ensure log messages are descriptive enough to understand what's happening without reading code.
- If you created a prototyping playground, add even more detailed instrumentation there.

---

### **Step 5: Run & Observe**

- Start the application in a new tmux session (for backend logs).
- Use `browser_console_messages` to monitor frontend logs.
- Use `browser_network_requests` to observe API/network activity.
- Attempt to reproduce the bug with instrumentation active.
  - If you created a prototyping playground, test through that route/module first
  - Then verify behaviour in the main application flow
- Collect and analyse log output from all sources.

**Human Intervention Point:**

If reproduction fails or observations are inconclusive:
- Explicitly request human assistance.
- Explain what was attempted and what information is still needed.
- Suggest specific ways the human could help (e.g., "Could you reproduce the bug and share the exact steps?" or "Can you verify if X behaviour occurs when you do Y?").
- Provide clear context so the human can help efficiently.

---

### **Step 6: Diagnose from Evidence**

- Review actual runtime behaviour from logs, network requests, and console messages.
- Identify the precise failure point and root cause.
- **Base your diagnosis on observed facts, not hypotheses.**
- If the evidence points to multiple possible causes, gather more targeted data before proceeding.
- Cross-reference observations from the prototyping playground (if used) with main application behaviour.

---

### **Step 7: Implement Fix**

- Fix directly in the current worktree based on evidence from Step 6.
- Keep diagnostic logging in place initially (you'll verify the fix in Step 8).
- Ensure the fix addresses the root cause, not just the symptoms.
- Apply the fix to the actual application code, not just in the playground.

---

### **Step 8: Verify Fix**

- Run the application again with logging still active.
- Reproduce the original bug scenario.
- Confirm the bug is resolved through observed behaviour.
- Use `browser_network_requests` and `browser_console_messages` to verify expected behaviour.
- Compare "before" and "after" logs if helpful.
- If you used a prototyping playground, verify the fix works both there and in the main application flow.

**Human Intervention Point:**

If verification is unclear or requires domain knowledge:
- Explicitly request human verification.
- Provide clear, step-by-step instructions for what to test.
- Explain what success looks like (expected vs actual behaviour).
- Share relevant log excerpts or observations that informed your fix.

---

### **Step 9: Report to User**

Provide a clear summary including:
- **Root cause:** Explain what was actually happening based on observed evidence
- **Diagnostic process:** Briefly describe how logging/observation revealed the issue
  - If you created a prototyping playground, explain why it was useful and what you learned from it
- **Implemented fix:** Describe the changes made and why they address the root cause
- **Verification results:** Confirm the fix works (or request human verification if needed)

---

### **Step 10: Automation Improvement Plan** (optional)

**Only include this section if:**
- The diagnosis was more difficult or time-consuming than it should have been, OR
- You encountered obstacles that could be prevented with codebase improvements, OR
- You required human intervention during the process

**What to include:**
- Analyse what made this bug difficult to diagnose automatically
- Propose specific, actionable codebase changes that would improve future automation:
  - **Accessibility improvements:** ARIA labels, test IDs, semantic HTML (dual benefit: improved accessibility for users + easier automation)
  - **Logging enhancements:** Structured logging, better error messages, trace IDs, contextual information
  - **Testability improvements:** Dependency injection, pure functions, better component boundaries
  - **Observability additions:** Health checks, metrics endpoints, debug modes, feature flags
  - **Debug tooling:** If a prototyping playground was particularly useful, consider keeping it (or a refined version) for future debugging
- Categorise suggestions by impact and implementation effort
- **Important:** Suggestions should be practical and should not sacrifice application quality, performance, or maintainability

---

### **Step 11: Clean Up** (optional)

- Remove or reduce instrumentation to production-appropriate levels.
- Keep any logging that would be valuable for future debugging.
- Decide whether to keep or remove the prototyping playground:
  - **Keep it** if it provides ongoing value for testing or debugging this feature
  - **Remove it** if it was only useful for this specific investigation
- Commit your changes with a clear, descriptive commit message.

---

## Key Principles

1. **Observation over speculation:** Always gather evidence from the running application rather than generating hypotheses.

2. **Prototyping playgrounds are tools, not escapes:** If you create a debug route or test module, it should help you observe the real application code more easily, not replace proper investigation.

3. **Request human help when needed:** If you're stuck, be explicit about it. Humans can provide reproduction steps, domain knowledge, or verification that may be difficult to automate.

4. **Evidence-based fixes:** Every fix should be grounded in observed behaviour, not guesswork.

5. **Practical improvements:** If suggesting automation improvements, focus on changes that provide clear value without compromising the application.