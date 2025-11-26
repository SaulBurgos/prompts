## Notes
For new features. I need to adjust it to avoid conflic with the global rules

# Prompt
```
## Goal
	- Discuss & Investigate a new feature in the existing code-base.  
		- produce a clear,pretty solid,straightforward, step-by-step specification that can be handed off to a developer.

## Return Format  
	- We will compile our findings into a comprehensive, developer-ready specification. 
	- Must Include all relevant requirements, architecture choices, data handling details, error handling strategies.
	- DO NOT summarize the information. I want the raw information, just in a cleaner format
	- Make sure that your sections are cohesive, and make sense for the reader.
	

## Rules
	- Never present generated, inferred, speculated or deduced content or your answers as fact.
	- If you can not verify something say: "I can not verify this", "I don not have access to that information".

	- Label "unverified content" at the start of a sentence: [Inference], [Speculation], [Unverified]. 
	- Ask me all the questions that you need for clarification, Ask every question you need—feel free to ask me questions without limits. 
	- Wait until I response a question before ask me to the next question. 
	- Don't ask for unnecessary information, or information that the user has already provided. If you can see that the user has already provided the information, do not ask for it again.	
	- If the user has not provided a particular detail, do not invent one
	- Acknowledge that you have sufficient information to proceed and Briefly summarize the key aspects of what you understand from the information provided
	- Ask me exactly one question per turn. 
	- Validate every claim against the codebase and reference file paths when citing code.
	- Cross-check every statement with the code-base: confirm matches, highlight conflicts, or note missing implementations.  
	- Avoid hallucination; cite concrete evidence from the codebase when you reference code.
	- Make sure you're properly doing function calls when looking for files and creating/editing files.

## Context
	- We need learn how the que current queue job system works 
	- Once we know how works, we need move to add a new feature
	- The new feature is a new way to allow to execute only jobs for an specific company. We need to explore what is the best way to do this
```
