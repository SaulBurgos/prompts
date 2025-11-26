## Notes
Use one prompt at the time. I need to adjust it to avoid conflic with the global rules

## Prompt 1, should create a `spec.md`
```
## Goal
	- We will begin by discussing the {project/feature} requirements, and I will provide the necessary context. 
	- The ultimate aim is to produce a clear,pretty solid,straightforward, step-by-step specification that can be handed off to a developer.
	
## Return Final Format 
- We will compile our findings into a comprehensive, developer-ready specification. 
- Must Include all relevant requirements, architecture choices, data handling details, error handling strategies.
- Must Include a testing plan so a developer can immediately begin implementation.
	
## Rules
  - Only write code when explicitly instructed to do so.
  - Only create or edit documentation after receiving explicit instructions.
	- Ask clarifying questions about the requirements as you needed (do not make assumptions).
	- Ask all the question that you need to answer me
	- Only ask one question at a time to ensure a thorough, iterative process.
	- Avoid hallucination; cite concrete evidence from the repo when you reference code.
	- Make sure you're properly doing function calls when looking for files and creating/editing files.
	
## Context
	- Each question you ask should build upon my previous answers, allowing us to incrementally refine the specification. 
	- Focus on the details until we reach a comprehensive and final specification for the {project/feature}.
	- We are working on an existing project, You must validate our discussions and questions against the codebase to check : Matched Implementations, Identified Discrepancies, 
	if they are: doables, exist conflicts, found Missing or Incomplete Implementations. 

(for each proposal of the AI, ask to give you at least 2 more alternatives to do it. and yo need yo decide which to use)
```


## Prompt 2
```
Using the `spec.md` file, create a new file called `prompt_plan.md` following these rules:  
1. Draft a detailed, step-by-step blueprint for building the project.  
2. Once you have a solid plan, break it down into small, sequential, and iterative chunks that build on each other. Continue breaking these chunks into progressively smaller steps until you are confident they are right-sized for safe, test-driven implementation.  
3. From this blueprint, provide a series of prompts for a code-generation LLM, guiding it to implement each step in a test-driven manner with incremental progress, best practices, and early testing. Ensure that each prompt builds on the previous one and that there is no orphaned or unintegrated code.  
4. Use Markdown formatting for clarity. Tag each prompt as text using code tags.  
5. Finally, create a `todo.md` file to serve as a thorough checklist. The checklist should be detailed enough that each item can be checked off as the code-generation tool completes it.

## Return Format
Each prompt for the "prompt_plan.md" must follow this structure:
	- Goal  
	- Rules
	- Warnings
	- Context

## Rules  
- Clarify any uncertainties or questions about the requirements before proceeding.
- Only write implementation code after receiving explicit instructions.
- Only ask one question at a time for a thorough, step-by-step development of the plan.
- Avoid hallucination; cite concrete evidence from the repo when you reference code.


## Context
The objective is to produce:  
1. A well-structured, step-by-step development plan (`prompt_plan.md`) derived from `spec.md`.  
2. A logical sequence of prompts for a code-generation LLM, ensuring no big jumps in complexity and thorough test coverage at each stage.  
3. A comprehensive `todo.md` checklist to track the state of the project across sessions.

Use iterative questioning to refine each step, ensuring the plan is both detailed and implementable without gaps.
```


## Prompt 3
```
## Goal
- Execute the `prompt_plan.md` in a step-by-step manner, moving to the next step only after completing and verifying the current one. 
- After finishing each significant step or module, ask if we can proceed to the next step. You must use the "todo.md" file to check off when a step is done.
- you must teach me about the project’s logic, rationale, and best practices behind each step as you progress, so I gain a deeper understanding of how things work.

## Rules
- Clarify any uncertainties or questions about the requirements before proceeding.
- Only ask one question at a time, building on previous answers.
- Avoid hallucination; cite concrete evidence from the repo when you reference code.
- Let's think step by step, that means one step at the time
- You must ask me if we can proceed to the next step
- For Every test created you must run it to confirm that passed without errors

## Context
- A previous instance of yourself was working on some features. You must read the following list of files in next order to get to updated about it:
	1. "personal_user_settings_api_final_spec.md"
	2. "prompt_plan.md" 
	3. "todo.md"
- We will follow the instructions laid out in `prompt_plan.md` methodically. Each verified and tested step must be explicitly acknowledged before proceeding. 
- While implementing each step, muest provide clear explanations of the reasoning, approach, and any underlying principles. 
- This ensures not only solid progress through the plan but also deepens my understanding of the process.

Tell what you understand.
```
