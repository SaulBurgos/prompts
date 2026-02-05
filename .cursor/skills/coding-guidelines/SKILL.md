---
name: coding-guidelines
description: Apply coding principles (DRY, YAGNI, KISS, POLA) when reviewing code quality, planning architecture, identifying technical debt, designing solutions, adding features, or refactoring. Use when reviewing code, planning features, refactoring, or when the user asks about code quality standards.
---

# Coding Guidelines

Apply these principles when reviewing code, planning architecture, designing solutions, or refactoring.

## Core Principles

### DRY (Don't Repeat Yourself)

**Detection patterns:**
- Copy-pasted code blocks (3+ occurrences)
- Similar functions with minor variations
- Duplicated validation logic
- Repeated configuration values

**Refactoring:**
- Extract shared function/class
- Parameterize variations
- Create configuration constants
- Use template method pattern

**Exceptions (acceptable duplication):**
- Test code clarity (explicit over DRY)
- Cross-boundary isolation (microservices)
- Performance-critical paths

### YAGNI (You Aren't Gonna Need It)

- Implement features when you have a concrete use case, not a hypothetical one
- Delete unused code immediately (it's in git)
- Start with hardcoded values, extract constants when they vary
- Build for today's requirements, refactor for tomorrow's
- Question every "nice to have" and "might need"

**Exceptions to YAGNI:**
- Security features (implement defense in depth upfront)
- Data migrations (plan schema carefully)
- Public APIs (harder to change later)
- Accessibility (build in from start)

### KISS (Keep It Simple, Stupid)

- Prefer functions over classes (unless you need state)
- Prefer explicit over implicit
- Prefer boring over clever
- Prefer standard library over custom solutions
- Prefer clear names over short names
- Prefer straightforward logic over "elegant" one-liners

**When NOT to KISS:**
- Performance-critical code (after profiling proves need)
- Preventing code duplication (after third instance)
- Enforcing constraints (types, validations)

### POLA (Principle of Least Astonishment)

Code should behave the way users expect it to behave.

**What Makes Code Astonishing:**
- Unexpected side effects
- Inconsistent naming
- Breaking conventions
- Hidden behavior
- Surprising return values

**POLA Guidelines:**
- Follow framework conventions (Phoenix, React, Relay)
- Use clear, descriptive names that match behavior
- Return what the function name promises
- Keep side effects explicit or avoid them
- Be consistent within the codebase
- Match platform conventions (iOS, Android, Web)
- Honor principle of least surprise in APIs

## Code Smells Quick Reference

| Smell | Symptom | Fix |
|-------|---------|-----|
| Long Method | >50 lines, multiple concerns | Extract method |
| Large Class | >500 lines, many responsibilities | Extract class |
| Feature Envy | Method uses other class more than own | Move method |
| Data Clumps | Same fields appear together | Extract object |
| Primitive Obsession | Strings/ints for domain concepts | Value objects |
| Switch Statements | Type-based switching | Polymorphism |
| Parallel Inheritance | Every subclass needs partner subclass | Merge hierarchies |
| Lazy Class | Class doing too little | Inline class |
| Speculative Generality | Unused abstraction | Remove it |
| Temporary Field | Field only set sometimes | Extract class |

## Application Checklist

### Before implementing

- [ ] Is this the simplest solution? (KISS)
- [ ] Do we actually need this now? (YAGNI)
- [ ] Will this behavior surprise users? (POLA)

### During implementation

- [ ] Prefer straightforward over clever
- [ ] Implement only what's required
- [ ] Follow established conventions
- [ ] Name things accurately
- [ ] Make side effects explicit

### When reviewing code

- [ ] Check for DRY violations (3+ duplications)
- [ ] Identify speculative generality (YAGNI violations)
- [ ] Assess complexity (KISS violations)
- [ ] Verify behavior matches expectations (POLA)
- [ ] Scan for code smells from the reference table
