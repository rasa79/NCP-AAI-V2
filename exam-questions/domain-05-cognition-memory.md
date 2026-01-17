# Domain 5: Cognition, Planning, and Memory

**Exam Weight**: 10%  
**Number of Questions**: 10

---

### Question 1: Chain-of-Thought for Complex Reasoning

**Scenario:**
A financial planning agent must calculate retirement savings needs considering multiple factors: current age, retirement age, life expectancy, current savings, monthly contributions, expected returns, inflation, and desired retirement income. Direct calculation often produces errors.

**Requirements:**
- Perform multi-step calculations accurately
- Show reasoning process
- Handle complex financial formulas
- Enable verification of calculations

**Question:** What reasoning approach ensures accurate financial calculations?

**Options:**

A) Chain-of-thought prompting: instruct agent to show step-by-step reasoning, break down calculation into stages (calculate years to retirement, future value of current savings, future value of contributions, required nest egg, gap analysis), verify each step.

B) Ask agent to provide final answer directly.

C) Use calculator tool for all calculations.

D) Fine-tune model on financial calculations.

**Correct Answer:** A

**Explanation:**
**Chain-of-thought** improves accuracy through explicit reasoning: (1) **Step 1**: "Years to retirement = 65 - 35 = 30 years", (2) **Step 2**: "Future value of $50K at 7% for 30 years = $50K × (1.07)^30 = $380K", (3) **Step 3**: "Future value of $500/month contributions...", (4) **Step 4**: "Required nest egg for $5K/month income...", (5) **Step 5**: "Gap = Required - Available". Each step verifiable. Direct answer (B) error-prone. Calculator tool (C) helps but doesn't structure reasoning. Fine-tuning (D) expensive, less flexible.

**NVIDIA Tools:** TensorRT-LLM for fast chain-of-thought inference

**Exam Mapping:** Domain 5, Objective 5.2 (Apply reasoning frameworks including chain-of-thought)

**Key Concepts:** Chain-of-thought, step-by-step reasoning, complex calculations, verification

---

### Question 2: Task Decomposition for Complex Goals

**Scenario:**
A project management agent must help plan a product launch involving market research, product development, marketing campaign, sales training, and launch event. The agent must break down the high-level goal into actionable subtasks with dependencies.

**Requirements:**
- Decompose complex goal into subtasks
- Identify task dependencies
- Create actionable plan
- Handle task ordering constraints

**Question:** What planning approach handles complex task decomposition?

**Options:**

A) Hierarchical task decomposition: break goal into major phases, decompose each phase into subtasks, identify dependencies, create dependency graph, generate execution plan respecting dependencies.

B) List all tasks in random order.

C) Ask user to decompose the goal.

D) Use predefined template for all product launches.

**Correct Answer:** A

**Explanation:**
**Hierarchical decomposition**: (1) **Level 1**: Major phases (Research, Development, Marketing, Training, Launch), (2) **Level 2**: Subtasks (Research → Market analysis, Competitor analysis, Customer surveys), (3) **Dependencies**: Development depends on Research, Marketing depends on Development, (4) **Graph**: Visualize dependencies, (5) **Plan**: Topological sort for execution order. Random order (B) ignores dependencies. User decomposition (C) defeats purpose. Template (D) inflexible.

**NVIDIA Tools:** NeMo Agent Toolkit for task planning

**Exam Mapping:** Domain 5, Objective 5.3 (Engineer planning strategies for sequential decision-making)

**Key Concepts:** Task decomposition, hierarchical planning, dependency graphs, execution planning

---

### Question 3: Short-Term vs Long-Term Memory

**Scenario:**
A personal assistant agent helps with daily tasks (calendar, reminders, emails) and must remember both immediate conversation context and long-term user preferences (meeting preferences, email style, frequent contacts).

**Requirements:**
- Maintain immediate conversation context
- Remember long-term preferences
- Distinguish between temporary and persistent information
- Efficient memory access

**Question:** What memory architecture balances short-term and long-term needs?

**Options:**

A) Dual memory system: short-term memory (conversation buffer, last 10 turns) for immediate context, long-term memory (vector database) for preferences and historical information, with intelligent retrieval combining both.

B) Store everything in conversation context.

C) Store everything in vector database.

D) Use only the most recent message as context.

**Correct Answer:** A

**Explanation:**
**Dual memory**: (1) **Short-term**: Conversation buffer (fast access, recent context), holds last 10 turns, (2) **Long-term**: Vector DB (persistent storage), user preferences ("prefers 30-min meetings"), frequent contacts, past decisions, (3) **Retrieval**: Query long-term memory for relevant preferences, combine with short-term context. Everything in context (B) hits limits, expensive. Everything in vector DB (C) slow for recent context. Recent-only (D) forgets preferences.

**NVIDIA Tools:** NIM for embedding and retrieval, TensorRT-LLM for generation

**Exam Mapping:** Domain 5, Objective 5.1 (Implement memory mechanisms for short- and long-term context)

**Key Concepts:** Short-term memory, long-term memory, dual memory systems, conversation buffers

---

### Question 4: Stateful Orchestration for Multi-Step Workflows

**Scenario:**
An insurance claims agent handles multi-day workflows: claim submission, document collection, adjuster assignment, damage assessment, approval, payment. The agent must maintain state across sessions and resume from interruptions.

**Requirements:**
- Track workflow state across sessions
- Resume from interruptions
- Handle state transitions
- Support parallel workflows for multiple claims

**Question:** What orchestration approach manages stateful workflows?

**Options:**

A) State machine with persistent storage: define workflow states and transitions, store current state in database, load state on session resume, support multiple concurrent workflows with separate state instances.

B) Store state in conversation context.

C) Restart workflow from beginning on each session.

D) Use stateless agent, ask user for status each time.

**Correct Answer:** A

**Explanation:**
**State machine**: (1) **States**: Submitted, DocumentsPending, UnderReview, Approved, Paid, (2) **Transitions**: Submitted → DocumentsPending (when docs requested), DocumentsPending → UnderReview (when docs received), (3) **Persistence**: Store state in DB with claim ID, (4) **Resume**: Load state on session start, continue from current state, (5) **Concurrency**: Each claim has separate state instance. Context storage (B) lost between sessions. Restart (C) poor UX. Stateless (D) burdens user.

**NVIDIA Tools:** NeMo Agent Toolkit for workflow orchestration

**Exam Mapping:** Domain 5, Objective 5.4 (Manage stateful orchestration for complex tasks)

**Key Concepts:** State machines, stateful orchestration, workflow management, persistence

---

### Question 5: Adaptive Reasoning Based on Experience

**Scenario:**
A customer service agent learns that certain types of issues (billing errors) are best resolved by immediate refund, while others (technical issues) need troubleshooting. The agent should adapt its approach based on past successful resolutions.

**Requirements:**
- Learn from successful resolutions
- Adapt strategy based on issue type
- Improve over time
- Maintain knowledge of effective approaches

**Question:** What approach enables learning from experience?

**Options:**

A) Case-based reasoning: store successful resolutions in memory, retrieve similar past cases when handling new issues, adapt successful strategies to current situation, update case library with new successes.

B) Use fixed rules for all issue types.

C) Randomly try different approaches.

D) Always ask supervisor for guidance.

**Correct Answer:** A

**Explanation:**
**Case-based reasoning**: (1) **Storage**: Store successful cases (issue type, approach, outcome), (2) **Retrieval**: New billing error → retrieve similar past billing errors, (3) **Adaptation**: Past case used immediate refund successfully → try immediate refund, (4) **Learning**: If successful, add to case library. Builds knowledge over time. Fixed rules (B) don't adapt. Random (C) inefficient. Supervisor (D) doesn't scale.

**NVIDIA Tools:** NIM for case retrieval and adaptation

**Exam Mapping:** Domain 5, Objective 5.5 (Adapt reasoning strategies based on prior experiences)

**Key Concepts:** Case-based reasoning, learning from experience, adaptive strategies, knowledge accumulation

---

### Question 6: Planning with Uncertainty

**Scenario:**
A travel planning agent must create itineraries considering uncertain factors: weather (might rain), availability (hotels might be booked), preferences (user might change mind). The agent needs flexible plans that adapt to changes.

**Requirements:**
- Create plans considering uncertainty
- Include contingency options
- Adapt plans when conditions change
- Balance flexibility and specificity

**Question:** What planning approach handles uncertainty?

**Options:**

A) Contingency planning: create primary plan with backup options for uncertain elements, monitor conditions, switch to contingencies when needed, maintain plan flexibility while ensuring key requirements met.

B) Create single fixed plan.

C) Wait until all uncertainty resolved before planning.

D) Create multiple complete plans, let user choose.

**Correct Answer:** A

**Explanation:**
**Contingency planning**: (1) **Primary**: Outdoor activity on Day 2, (2) **Contingency**: If rain → indoor museum, (3) **Monitoring**: Check weather forecast, (4) **Adaptation**: Switch to contingency if rain likely, (5) **Flexibility**: Multiple options for uncertain elements. Fixed plan (B) brittle. Waiting (C) delays planning. Multiple complete plans (D) overwhelming.

**NVIDIA Tools:** NeMo Agent Toolkit for adaptive planning

**Exam Mapping:** Domain 5, Objective 5.3 (Engineer planning strategies)

**Key Concepts:** Contingency planning, uncertainty handling, adaptive plans, flexibility

---

### Question 7: Memory Consolidation and Summarization

**Scenario:**
A therapy chatbot has 50+ sessions with a patient. Full conversation history exceeds context limits. The agent needs to remember key themes, progress, and important details without storing every word.

**Requirements:**
- Compress long conversation history
- Retain important information
- Enable recall of key themes
- Manage context window limits

**Question:** What memory management approach works best?

**Options:**

A) Hierarchical summarization: summarize each session, create meta-summary of multiple sessions, store important details separately, retrieve relevant summaries and details for current session.

B) Store full transcripts of all sessions.

C) Keep only most recent session.

D) Ask patient to summarize previous sessions.

**Correct Answer:** A

**Explanation:**
**Hierarchical summarization**: (1) **Session summaries**: Each session → 200-word summary (key topics, progress, homework), (2) **Meta-summaries**: Every 5 sessions → overall progress summary, (3) **Important details**: Store separately (trauma history, medications, goals), (4) **Retrieval**: Current session retrieves relevant summaries + important details. Full transcripts (B) exceed context limits. Recent-only (C) loses history. Patient summary (D) burdens patient.

**NVIDIA Tools:** TensorRT-LLM for fast summarization

**Exam Mapping:** Domain 5, Objective 5.1 (Implement memory mechanisms)

**Key Concepts:** Memory consolidation, hierarchical summarization, context management, information compression

---

### Question 8: Goal-Oriented Planning

**Scenario:**
A fitness coaching agent must help user achieve goal: "Lose 20 pounds in 6 months." The agent must create actionable plan with milestones, track progress, and adjust plan based on results.

**Requirements:**
- Break goal into milestones
- Create actionable steps
- Track progress toward goal
- Adjust plan based on progress

**Question:** What planning framework supports goal achievement?

**Options:**

A) Goal decomposition with monitoring: break goal into monthly milestones (3-4 lbs/month), create weekly action plans (diet, exercise), track progress metrics, adjust plan if behind/ahead of schedule.

B) Provide general advice about weight loss.

C) Create detailed 6-month plan upfront, don't adjust.

D) Set goal, let user figure out how to achieve it.

**Correct Answer:** A

**Explanation:**
**Goal-oriented planning**: (1) **Decomposition**: 20 lbs in 6 months → 3.3 lbs/month → 0.8 lbs/week, (2) **Action plans**: Weekly diet (calorie target) and exercise (workout schedule), (3) **Tracking**: Weekly weigh-ins, progress toward milestones, (4) **Adaptation**: If behind schedule → increase calorie deficit or exercise, if ahead → maintain current plan. General advice (B) not actionable. Fixed plan (C) doesn't adapt. No guidance (D) unhelpful.

**NVIDIA Tools:** NeMo Agent Toolkit for goal tracking

**Exam Mapping:** Domain 5, Objective 5.3 (Engineer planning strategies)

**Key Concepts:** Goal decomposition, milestone planning, progress tracking, adaptive planning

---

### Question 9: Working Memory Management

**Scenario:**
A coding assistant agent helps debug complex code. During debugging, the agent must track: current hypothesis, variables checked, tests run, and findings. This working memory must be maintained during the debugging session but can be discarded after.

**Requirements:**
- Maintain working memory during session
- Track multiple pieces of information
- Update memory as investigation progresses
- Clear memory after session

**Question:** What working memory approach is appropriate?

**Options:**

A) Structured working memory: maintain explicit data structure (hypothesis, checked_variables, tests_run, findings), update structure as debugging progresses, include in context for each turn, clear after session ends.

B) Rely on conversation history for working memory.

C) Store working memory in long-term database.

D) Ask user to track debugging progress.

**Correct Answer:** A

**Explanation:**
**Structured working memory**: (1) **Structure**: `{hypothesis: "null pointer", checked: ["var1", "var2"], tests: ["test_input_null"], findings: ["var1 is null"]}`, (2) **Updates**: Add to checked/tests/findings as debugging progresses, (3) **Context**: Include structure in each prompt, (4) **Lifecycle**: Clear after bug fixed. Conversation history (B) unstructured, hard to track. Long-term storage (C) unnecessary for temporary info. User tracking (D) burdens user.

**NVIDIA Tools:** NeMo Agent Toolkit for structured memory

**Exam Mapping:** Domain 5, Objective 5.1 (Implement memory mechanisms)

**Key Concepts:** Working memory, structured memory, session-based memory, memory lifecycle

---

### Question 10: Multi-Agent Coordination with Shared Memory

**Scenario:**
A research team of AI agents (literature reviewer, data analyst, writer) collaborates on research paper. Agents must share findings and coordinate work. Literature reviewer finds relevant papers, data analyst analyzes data, writer synthesizes into paper.

**Requirements:**
- Share information between agents
- Coordinate agent activities
- Avoid duplicate work
- Maintain shared understanding

**Question:** What memory architecture enables agent coordination?

**Options:**

A) Shared memory workspace: central memory store accessible to all agents, agents write findings to shared memory, agents read from shared memory to understand others' work, coordination through shared state.

B) Each agent has private memory, no sharing.

C) Agents communicate only through final outputs.

D) Single agent does all work.

**Correct Answer:** A

**Explanation:**
**Shared memory**: (1) **Workspace**: Central store with sections (literature_findings, data_analysis, draft_sections), (2) **Writing**: Literature reviewer writes paper summaries to literature_findings, (3) **Reading**: Data analyst reads literature_findings to understand context, (4) **Coordination**: Writer reads both sections to synthesize. Enables collaboration. Private memory (B) no coordination. Final outputs only (C) no intermediate sharing. Single agent (D) loses specialization benefits.

**NVIDIA Tools:** NeMo Agent Toolkit for multi-agent coordination

**Exam Mapping:** Domain 5, Objective 5.4 (Manage stateful orchestration), Domain 1 (Multi-agent systems)

**Key Concepts:** Shared memory, multi-agent coordination, collaborative work, memory sharing

---

**End of Domain 5 Questions**

**Summary:**
- Total Questions: 10
- Domain Weight: 10%
- Topics Covered: Chain-of-thought reasoning, task decomposition, short-term vs long-term memory, stateful orchestration, adaptive reasoning, planning with uncertainty, memory consolidation, goal-oriented planning, working memory, multi-agent coordination


---

## Study Resources

To prepare for these questions, review:

**Course Notes:** [Module 05 Cognition Planning Memory](../../course-notes/module-05-cognition-planning-memory.md)

**Practice Notebooks:**
- [01 Memory Mechanisms](../../notebooks/module-05/01-memory-mechanisms.ipynb)
