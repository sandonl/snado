---
title: "Hello world"
summary: "This is my first post!"
createdAt: "2024-01-01"
tags: ["hello", "world"]
author: "Sandon L"
---

tl:dr; Going beyond testing and evaluating simple prompts for Gen AI for legal. Test and evaluate on legal use cases. How do we achieve this when developing Mobius.

# Evaluating Due Diligence with AI - An intro to Mobius

### Overview

Mobius is an AI Platform built and designed by TILT Legal to help legal teams improve their legal workflows. One of the main objectives we had when starting Mobius was to go beyond automating legal workflows and narrow in on certain legal use cases and grasp as to whether AI was capable enough of aiding legal teams.

### What are we trying to achieve

Common legal AI benchmarks often involve evaluating the accuracy of a model's response to a simple legal question. However, this approach doesn't truly reflect AI's capabilities in broader legal workflows. Instead of focusing solely on question-answer accuracy, we shifted our focus to evaluating AI's performance in specific legal tasks—such as contract review or data extraction from multiple documents. This shift not only changes how we assess AI output but also highlights additional engineering challenges. How can we scale this approach to handle large contracts, multiple contracts, or analyses based on various instructions? Our challenge was to evaluate our ability to manage this scale, while also determining if we could effectively address the legal use case at hand.

One of the first use cases that we identified was to perform due diligence on a given contract. The task was to see if the model was able to identify key risks provided by the user and able to assess how close this analysis of a contract was to an ‘ideal state’. A simple prompt such as ‘Find the two parties in this contract’ might work fine consistently but something like ‘Identify the consequential loss clause and compare them to an ideal state’ adds a whole deal of complexity and variance to what the model outputs.

So this comes to our first iteration of an evaluation loop which was to answer the question; Can Mobius, given a contract and set of instructions, complete a contract review that aligns with some reference output **consistently?**

### Introducing Graphs and LLM orchestration

The issue with this type of task is that suddenly a zero-shot, question-answer prompt doesn’t really address or achieve what we’re trying to solve. One of the key challenges of this type of task is the limitation of a model’s context window as well as being able to get an accurate enough answer. Contracts are unique in that often they may require context of the document in it’s entirety to answer questions, often referencing or requiring definition of other clauses throughout to answer a given question. For something with this level of complexity, we decided to shift our LLM architecture to focus on using LLM https://langchain-ai.github.io/langgraph/tutorials/introduction/ Graphs which gave us better control and decision flow of an application and the ability to break down these types of complex tasks in an agentic way.

There are many ‘levers’ or factors we can pull here to aid in not only performance, but to help break down the task of getting closer to a reference output. These are not limited to:

- Model choice
- Prompting (System and review prompts)
- Examples provided
- Parsing
- Pre-processing of a document
- Optimising context-windows
- Utilising multi-step agent flows,
- RAG

Unfortunately there’s not always a good indication of what lever pulled is really having an impact and pushing the needle forward. Which then comes to our testing and evaluation suite, https://www.langchain.com/langsmith’s Datasets and Evaluation functionality have helped us test and evaluate which ‘levers’ are causing what effect on Mobius. Allowing us to iterate quickly. LangSmith is a great platform to help test and trace end-to-end LLM applications, by using LangSmith we were able to not only investigate and debug each step in our graphs but also get a testing + eval feedback loop to identify what factors were causing degradation or improvement. This was done by simply creating a dataset with examples, in which we provided good ‘reference outputs’.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/25ee4446-b807-48f1-9844-3d0adbe3428b/f9191cf8-7ad3-46fb-a684-575ec640aaf0/image.png)

A small selection of examples from our dataset with a predetermined ideal reference output.

By being able to quickly swap out, test and evaluate different factors (often combining a variety of them) of our graphs, we were able to see what effect this was having on Mobius in being able to get closer to our reference output. Scaling this to run on multiple datasets gave us a better idea of what overall direction to put our effort towards.

### A word on evaluators

So now you might be wondering how we actually evaluated our graphs and the outputs they gave, and the answer is more AI! Using ‘LLM-as-a-judge’ to help compare answers that our graphs gave against the reference output. One of the first challenges we encountered was having the LLM-as-a-judge be too harsh when comparing responses between a reference and given output. Often would be the case when analysing the underlying risks, actionable advice and legal accuracy would the LLM do an overtly critical job at trying to find discrepancies between the two outputs. This often lead to the case of determining a false negative since the underlying substance of both outputs were similar and in a way useful enough but one simply lacked more comprehension and nuance.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/25ee4446-b807-48f1-9844-3d0adbe3428b/9d8514e5-bf5d-4ad5-b25b-6a3b0f9723ee/image.png)

An example of the type of analysis our evaluator was generating on certain clauses (keys). We assigned them a score based on how close they were to our reference output.

The difficulty here was coming up with an evaluator that was useful to us that was able to balance both being critical of the response but similar enough in substance to the reference output. This is where the can be a lot more improvement on our side. https://www.braintrust.dev/docs/start has been doing great work in the eval space and have a tool to help quickly evaluate AI model outputs with standardised evaluators.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/25ee4446-b807-48f1-9844-3d0adbe3428b/57541b7b-2f4c-417e-943e-78e4ae2460b1/image.png)

An overview of multiple experiments and how we were able to get closer to our reference outputs.

### Takeaways

Theres still a lot of work to do. One of the first suspicions you may of had is how good is this ‘reference output’ that I’ve mentioned numerous times, and the answer is, it’s of course subjective. Different lawyers may find different outputs useful and what one lawyer finds useful in one response might not be useful to another.

What we’ve tested and evaluated is a case of a small feedback loop narrowed into a specific use-case on a very small dataset, But you can imagine once the dataset grows and use cases diversify, we can apply a similar methodology to help drive some of our engineering attention.

Furthermore, 100% Accuracy is not the goal - rather than focusing on number evaluations, at the end of the day, our objective was to answer the case of AI in focused legal workflows. There’s a still a lot of doubt and lack of confidence in AI output, and these type of evaluations can go a long way in instilling confidence to the lawyer and dispelling the black box. Even if the tool can cut a use case time down by 30% in a reliable way, does this still empower the lawyer? There is a constant balance of lawyers in the loop of these types of workflows.

If this type of content interests you, let’s connect!

### Questions for reviewers:

- Does this give away too much ‘sauce’ ?
- Can you follow the storyline of the post?
- Is there actually anything to take away from this?
- Language use and writing style - I want to give off the informal casual conversation vibe rather than a ‘PR’.

Random thought:

Iteration and reviewing outputs with ChatGPT → Taking the exact same process and concepts but scaling this. If im stuck in a silo where in order to progress i had to iterate and refine my outputs. Now if I scale this - the process is exactly the same, I iterate and refine my outputs but applying my IP and expertise
