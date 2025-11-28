## Notes
- Used before the "plan mode" on IDE
- Use one prompt at the time. I need to adjust it to avoid conflic with the global rules

## Prompt 

```
{Project/Feature} Planning Instructions:

1. Initial Discussion & investigation:
    - We'll begin by discussing the {project/feaure} requirements, and I'll provide the necessary context.
    - Please "do not write any code" until I explicitly give you the go-ahead.
    - Ask clarifying questions about the requirements as needed "do not make assumptions"
    - Ask me one question at a time so we can develop a through, step-by-step spec for this plan. Each question should build on my previous answers, 
    and our end goal is to have a detailed specification I can hand off to a developer. Let’s do this iteratively and dig into every relevant detail. 
    Remember, only one question at a time.
    
1.1 After initial discussion (This will output a pretty solid and straightforward spec that can be handed off to the planning step. I like to save it as "spec.md")
		- Now that we’ve wrapped up the brainstorming process, can you compile our findings into a comprehensive, developer-ready specification? Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.
    
2. Planning (using spec.md, the output is: prompt_plan.md)
    - Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, sequential and iterative chunks that build on each other. 
    Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, 
    but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.
    
    - From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices,
     incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. 
     There should be no hanging or orphaned code that isn't integrated into a previous step. Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as 
     text using code tags. The goal is to output prompts, but context, etc is important as well.
     
     - Can you make a `todo.md` that I can use as a checklist? Be thorough. (Your codegen tool should be able to check off the todo.md while processing. This is good for keeping state across sessions.)
    
3. Step-by-Step Execution:
    - We will move on to the next step only after completing and verifying the current one.
    - After finishing each significant step or module, ask me if we can proceed to the next one.
    
4. Summary Checkpoints:
    - After completing  steps, I will ask you to provide a summary of the current plan, context, and key decisions.
    - Create a "Project Status" file to track your progress. Review the conversation and update this file with what has been implemented and what’s next.

```
