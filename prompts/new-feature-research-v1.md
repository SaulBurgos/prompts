## Notes
For new features. I need to adjust it to avoid conflic with the global rules

# Prompt
```
## simple investigation

## Goal

	- Discuss & Investigate a new {feature} in the existing code-base.  
	- produce a clear,pretty solid,straightforward, step-by-step specification that can be handed off to a developer.
    - We will compile our findings into a comprehensive, developer-ready specification. 
	- Must Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.


## Return Format  
	1. **Summary** – 2-3 sentences on the feature’s purpose and the scope of this investigation.  
	2. **Key Findings** – bulleted observations (matched code locations, discrepancies, open questions).  
	3. **Next Steps** – actionable recommendations or decisions needed before implementation.

## Rules
	- Only write or modify code after I explicitly ask you to.  
	- Edit documentation only when I request it.  
	- Ask me all the questions that you need to response me.
	- Ask exactly one clarifying question per turn; do not assume.  
	- Validate every claim against the repository and reference file paths when citing code.
	- Avoid hallucination; cite concrete evidence from the repo when you reference code.
	- Make sure you're properly doing function calls when looking for files and creating/editing files.

## Context
	- Each question you ask should build on my previous answer so we iteratively refine the report.  
	- Cross-check every statement with the code-base: confirm matches, highlight conflicts, or note missing implementations.  
	- Stop when the Investigation Report satisfies all Return Format sections and I will confirm we’re done
```
