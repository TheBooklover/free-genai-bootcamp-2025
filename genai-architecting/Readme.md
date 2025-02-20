# **Conceptual Design Review**  

## **1. Architectural & Design Considerations**  
This section outlines the fundamental principles guiding system design, including requirements, risks, constraints, and assumptions.  

### **Requirements**  
#### **Business Requirements (Goals & Objectives)**  
- Provide an **AI-powered, interactive language learning experience** that adapts to students' progress  
- Deliver **real-time feedback** on pronunciation, vocabulary, and sentence structure   
- Ensure **teacher oversight** with analytics on student progress  

#### **Functional Requirements (Capabilities)**  
- **Speech Recognition Service:** Transcribes spoken language into text  
- **AI Feedback Engine:** Evaluates fluency, pronunciation, and grammar 
- **RAG System:** Retrieves contextual references to enhance AI responses and provide more relevant feedback 
- **Knowledge Base Integration:** Stores past interactions to refine recommendations.  

#### **Non-Functional Requirements (Performance, Security, Usability)**  
- **Scalability:** Should support hundreds of concurrent users  
- **Latency:** Real-time speech analysis should occur within seconds
- **Security:** Adheres to **Law 25** for student data protection.  

### **Risks & Mitigation Strategies**  
| Risk | Impact | Mitigation |
|------|--------|------------|
| High compute costs for AI processing | Speech recognition inaccuracies | Poor user experience | 
| Data privacy concerns | Compliance risk | Potential model bias in AI feedback | Unfair grading | Regularly audit & fine-tune models for fairness |
| Cost unpredictability | The use of **open-source LLMs** (IBM Granite / Huggy Face) |

### **Assumptions & Constraints**  
- **Assumptions:**  
  - Students will have **consistent internet access** for cloud-based processing  
  - Speech-to-text models will achieve **85%+ accuracy** for varied accents.  
- **Constraints:**  
  - AI models must run **within defined latency thresholds (<500ms per query).**  
  - The system must comply with **Québec education sector and data privacy regulations (Law 25).**  

---

## **2. Data Strategy**  

### **Data Collection & Preparation**  
- **User Speech Data:** Collected via Speech Recognition Service  
- **Text Responses:** Stored in a **structured knowledge vector database** for retrieval  
- **User Progress Metrics:** Captured for adaptive and progressive learning insights  

### **Privacy & Security**  
- Use **federated learning** where possible to minimize raw data storage  

---

## **3. Model Selection & Development**  

### **LLM Choices**  
| Consideration | SaaS (GPT-4, Claude) | Self-Hosted (GPT-NeoX, Falcon, GPT-J, Mistral, Llama) |
|--------------|---------------------|---------------------------|
| Cost         | Pay per token        | One-time infra cost |
| Latency      | Lower | Higher       |
| Control      | Vendor-managed       | Full control |
| Customization | Limited             | Full fine-tuning possible |

### **Speech Recognition Model**  
- **Whisper (OpenAI)** – Best for **multilingual** support  
- **Google ASR** – Good for **education-based vocab** tuning
- **DeepSpeech** – Open-source & customizable
- **Wav2Vec** – Open-source & customizable

### **Evaluation Criteria**  
- **Context Window:** At least **8K tokens** to retain conversation flow  
- **Fine-Tuning Needs:** Custom datasets improve fluency evaluation  
- **Performance Metrics:** **Word Error Rate (WER) <10%** for best UX 

---

## **4. Infrastructure Design**  
A scalable and flexible infrastructure that For suresupports GenAI workloads.  

### **Cloud vs. On-Prem Considerations**  
| Infrastructure | Benefits | Challenges |
|---------------|---------|------------|
| **Cloud (AWS, GCP, Azure)**   | Scalable, pay-as-you-go         | High costs when scaling (though cureently not an issue) |
| **Hybrid (Cloud + Edge AI)**  | Low latency, cost control       | Complex setup |
| **On-Prem (Self-hosted LLMs)**| Full control, no vendor lock-in | High upfront infrastructure cost |

**Recommended Approach:**  
- **Hybrid architecture:** Run inference **on-prem for cost savings**, scale to cloud as needed  
- **Containerized workloads:** Deploy AI models in **Docker/Kubernetes**.  
- **GPU acceleration:** Use **A100 GPUs** or **TPUs** for speech model inference.  

---

## **5. Integration & Deployment**  
- **APIs:** Develop REST or GraphQL APIs for LMS integration 
- **CI/CD Pipelines:** Automate model deployment & updates 

---

## **6. Monitoring & Optimization**  
- **Real-time telemetry:** Track AI performance & latency.  
- **Feedback Loops:** Capture user corrections to improve model
- **Usage Cost Alerts:** Prevent overuse with **billing notifications.**  

---
# **Business Considerations for GenAI Implementation**
To effectively integrate **Gen AI** within the classroom and teach foreign students how to properly speak Québecois French **specific use cases**. Identify the **business problems** we aim to solve

### **Business Problem: Quebecois French Language Learning**
#### **Challenge:**
Schools across Quebec lack **accessible, AI-enhanced resources** for teaching **Quebecois French**, making it difficult for students to achieve fluency in a way that reflects local linguistic and cultural nuances

#### **Impact:**
Existing language learning tools often focus on **standard French**, failing to address regional expressions, pronunciation, and contextual usage. This gap leads to **lower engagement, reduced comprehension, and a lack of practical language skills** among students

#### **Need:**
There is a demand for a **customized, AI-powered learning platform** that supports **teachers and students** by providing **interactive, adaptive, and culturally relevant exercises** in Quebecois French.

### **Defining the Desired Outcomes**
- **Personalized Learning Experience:** Deliver AI-driven exercises that adapt to student proficiency levels
- **Real-time Feedback & Corrections:** Provide instant evaluation on pronunciation, grammar, and vocabulary usage
- **Cultural & Linguistic Relevance:** Ensure the AI-generated content aligns with Quebecois French, incorporating regional expressions and nuances
- **Teacher Support & Insights:** Generate performance analytics to help educators tailor lesson plans

### **Aligning with Strategic Goals & Workflows**
- **Curriculum Integration:** Align AI-generated lessons with the Quebec education system's learning objectives
- **Sustainable AI Training:** Continuously refine AI models based on feedback from students and educators
- **Regulatory Compliance:** Maintain adherence to data privacy regulations (Law 25) to protect student information
- **Efficient Resource Utilization:** Optimize AI infrastructure to balance performance, cost, and sustainability


## **Complexity**

### **Key Questions to Consider:**
- **How many moving parts will it add to our workload?**
  - Does the integration require **multiple AI models**, **new infrastructure**, or **retraining staff**?
- **Is this set-and-forget, or does it need regular monitoring?**
  - GenAI models drift over time and require **ongoing monitoring**, evaluation, and fine-tuning

## **Key Levers of Cost**


### **Primary Cost Factors:**
- **Compute Costs:**
  - Size of servers (GPUs, TPUs, Cloud instances)
  - Model inference vs. training costs
- **Model Size & API Usage:**
  - Small models (e.g., Mistral, Llama 2) vs. large proprietary models (GPT-4, Claude)
  - Pay-per-token API calls vs. self-hosted models
- **Storage Costs:**
  - Storing training data, embeddings, and logs
  - Maintaining high-availability databases for fast retrieval

## **Avoiding Vendor Lock-In**
To **future-proof** our GenAI stack, we must plan for flexibility and avoid reliance on a single provider

### **Strategies to Reduce Lock-In Risk:**
- **Use Open-Source Models:**
  - Llama 2, Falcon, Mistral for self-hosted solutions
- **Design an Interoperable Stack:**
  - Use standard APIs and modular components
- **Hybrid Model Approach:**
  - Start with SaaS for fast deployment, transition to self-hosted for cost control
- **Plan for Migration Paths:**
  - Ensure easy swapping of models without major infrastructure changes

## **Essential Components for a Production-Ready GenAI Deployment**
For a **robust and scalable** GenAI system, include:

### **1. Guardrails**
- **Input Filtering:** Prevent prompt injection and malicious inputs
- **Output Control:** Restrict sensitive or non-compliant outputs
- **Ethical Considerations:** Ensure fairness, privacy, and safety

### **2. Evaluations**
- **Regular Performance Benchmarking:** Measure accuracy, latency, and cost-efficiency.
- **A/B Testing:** Compare different models to optimize results.
- **Bias & Fairness Audits:** Identify and mitigate unintended biases in AI-generated content.

### **3. Sandboxing via Containers**
- **Isolate AI Workloads:** Deploy LLMs in **Docker/Kubernetes** environments.
- **Ensure Scalability:** Dynamically allocate compute resources as demand fluctuates.
- **Security & Compliance:** Protect sensitive data with containerized environments.


