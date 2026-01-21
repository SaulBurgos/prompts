
## Notes

- The premise that tasks should be broken up into the smallest possible
elements, so that an LLM agent can focus on them one step at a time, improving per step error rate, and thus enabling
scaling, reliability, and efficiency in the limit.

- https://arxiv.org/pdf/2511.09030


# Prompt

```
- Once you have created a solid plan, break it down into small, sequential, and iterative chunks that build on each other. Continue breaking these chunks into progressively smaller steps until you are confident they are right-sized for safe, DRY. YAGNI. TDD. frequent commits.

- Assume developers reading this plan are a skilled developer, but know almost nothing about our toolset or problem domain. assume they don't know good test design very well.

- At the end of each phase, give me a list of unresolved questions, if any.

- After producing the breakdown, explicitly answer: 
  "Are there important parts of this problem where this breakdown is not possible?"  
  If yes, name those parts, explain why they resist further decomposition, and propose how to handle them.

- Each plan must include this instruction verbatim: 
  "After each phase or step is completed by you, you need to ask the user to review it and approve it in order to move to the next step or phase."

```


