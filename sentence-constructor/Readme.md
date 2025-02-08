
## Technical Uncertainty

**1.  How well can an AI-Powered Assistant perform a very broad task?** 
- It is okay, but our research has found that it is best served in executing specific, or very specific, tasks that is narrowly formatted by the designer to ensure it's response/action is consistent and repeatable. 

**2. Would a very broad task be better performed by dividing it into subtasks with specialized agents?** 
- Absolutely, in our research we found it is best to think through (perhaps even with the help of the AI) each of the steps in a particular task or flow or process and dedicate each step as a separate propmpt or action with the specialized agent
*  
**4. How could we take the agent we built in an AI-Powered Assistant and reimplement it into a stack that allows for direct integration into our platform?** 
One of the first steps will be to break everything into constituent, modular service parts in order to easily deploy and scale, as needed. We would also then design each service as APIs. With these services in tow, we would then containerize each microservice, again for easier deployment and management. We might also consider serverless functions that are triggered by the API requests in order to once again scale effectively

We would service the APIs with a standard autorization mechanism, most likely simple API keys. 

**5. How much do we have to rework our prompt documents from one AI-Powered Assistant to another?**  
There was minimal need to rework the prompt documents, save for an additional step to simply execute the prompt. Some models were simply reviewing the long prompt instead of executing it. By adding this step at the beginning, it worked out the issue. 

**6. What prompting techniques can we naturally discover working in the confines of an AI-Powered Assistant?**  


**7. Are there any interesting innovations unique to specific AI-Powered Assistants for our business goal?**  
The AI-Powered Assistant is quite effective at giving context clues without giving away the answer. Further, by leveraging a DB of the student's inputs over multiple uses, it can provide clearer, more focused feedback specific to that student's particular challenges in learning the language. The more the student uses it, the more precise and focused the feedback is









