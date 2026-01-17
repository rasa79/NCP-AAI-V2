# Module 2: Agent Development

**Exam Weight:** 15%  
**Estimated Study Time:** 8-10 hours  
**Prerequisites:** Module 1 (Agent Architecture and Design), Python programming, REST API concepts

## Learning Objectives

By the end of this module, you will be able to:

1. **Engineer effective prompts and dynamic prompt chains** for complex agent behaviors
2. **Integrate generative and multimodal models** (text, vision, audio) into agent workflows
3. **Build and connect custom tools, APIs, and functions** for agent capabilities
4. **Implement robust error handling** including retry logic, circuit breakers, and graceful degradation
5. **Develop dynamic conversation flows** with real-time streaming responses
6. **Evaluate and refine agent decision-making strategies** through iterative testing

## Exam Objective Mapping

This module directly addresses the following NCP-AAI exam objectives:

- **2.1** - Engineer prompts and dynamic prompt chains
- **2.2** - Integrate generative and multimodal models
- **2.3** - Build and connect custom tools, APIs, and functions
- **2.4** - Implement error handling (retry logic, graceful failure recovery)
- **2.5** - Develop dynamic conversation flows with real-time streaming
- **2.6** - Evaluate and refine agent decision-making strategies

---

## 1. Prompt Engineering for Agents

### 1.1 Fundamentals of Prompt Engineering

**Prompt engineering** is the art and science of crafting inputs that elicit desired behaviors from language models.

**Key Principles:**

1. **Clarity** - Be explicit about what you want
2. **Context** - Provide relevant background information
3. **Structure** - Use consistent formatting
4. **Examples** - Show desired output format (few-shot learning)
5. **Constraints** - Specify limitations and requirements

### 1.2 Prompt Templates for Agents

**Basic Agent Prompt Structure:**

```python
AGENT_PROMPT_TEMPLATE = """
You are {agent_role}, an AI assistant designed to {agent_purpose}.

Your capabilities include:
{capabilities_list}

Guidelines:
- {guideline_1}
- {guideline_2}
- {guideline_3}

Current Context:
{context}

User Request: {user_input}

Think step-by-step and use available tools when needed.
"""
```

**Example: Customer Support Agent**

```python
from langchain.prompts import PromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# Define prompt template
support_prompt = PromptTemplate(
    input_variables=["user_name", "issue", "history"],
    template="""
You are a helpful customer support agent for TechCorp.

Customer: {user_name}
Previous Interactions: {history}

Current Issue: {issue}

Instructions:
1. Acknowledge the customer's concern empathetically
2. Ask clarifying questions if needed
3. Provide step-by-step solutions
4. Escalate to human if issue is complex or customer is frustrated
5. Always maintain a professional and friendly tone

Response:
"""
)

# Use with NVIDIA NIM
llm = ChatNVIDIA(
    model="meta/llama-3.1-70b-instruct",
    nvidia_api_key="your-api-key",
    temperature=0.7
)

# Generate response
response = llm.invoke(
    support_prompt.format(
        user_name="Alice",
        issue="My order hasn't arrived",
        history="Previous order was delivered successfully"
    )
)
```


### 1.3 Dynamic Prompt Chains

**Dynamic prompt chains** adapt based on intermediate results, enabling complex multi-step reasoning.

**Pattern 1: Sequential Chain**

```python
from langchain.chains import LLMChain, SequentialChain
from langchain_nvidia_ai_endpoints import ChatNVIDIA

llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct")

# Chain 1: Extract key information
extract_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        input_variables=["user_query"],
        template="Extract the key entities and intent from: {user_query}\nEntities:"
    ),
    output_key="entities"
)

# Chain 2: Generate search queries
search_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        input_variables=["entities"],
        template="Based on these entities: {entities}\nGenerate 3 search queries:"
    ),
    output_key="search_queries"
)

# Chain 3: Synthesize response
synthesis_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        input_variables=["search_queries", "user_query"],
        template="Original query: {user_query}\nSearch queries: {search_queries}\nProvide a comprehensive answer:"
    ),
    output_key="final_answer"
)

# Combine into sequential chain
overall_chain = SequentialChain(
    chains=[extract_chain, search_chain, synthesis_chain],
    input_variables=["user_query"],
    output_variables=["final_answer"],
    verbose=True
)

# Execute
result = overall_chain({"user_query": "What are the latest developments in quantum computing?"})
```

**Pattern 2: Conditional Chain**

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class ConditionalPromptChain:
    def __init__(self, llm):
        self.llm = llm
        
        # Define different prompt strategies
        self.simple_prompt = PromptTemplate(
            input_variables=["query"],
            template="Answer briefly: {query}"
        )
        
        self.detailed_prompt = PromptTemplate(
            input_variables=["query"],
            template="Provide a comprehensive answer with examples: {query}"
        )
        
        self.technical_prompt = PromptTemplate(
            input_variables=["query"],
            template="Provide a technical explanation with code examples: {query}"
        )
    
    def execute(self, query, complexity="simple"):
        """Execute chain based on complexity level"""
        if complexity == "simple":
            prompt = self.simple_prompt
        elif complexity == "detailed":
            prompt = self.detailed_prompt
        else:
            prompt = self.technical_prompt
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(query=query)

# Usage
chain = ConditionalPromptChain(llm)

# Adapt based on user preference or query complexity
simple_answer = chain.execute("What is RAG?", complexity="simple")
detailed_answer = chain.execute("What is RAG?", complexity="detailed")
technical_answer = chain.execute("What is RAG?", complexity="technical")
```

### 1.4 Few-Shot Prompting for Agents

**Few-shot learning** provides examples to guide agent behavior.

```python
FEW_SHOT_PROMPT = """
You are a code review agent. Analyze code and provide constructive feedback.

Example 1:
Code: def add(a, b): return a + b
Review: Good: Simple and clear. Improvement: Add type hints and docstring.

Example 2:
Code: def process(data): result = []; [result.append(x*2) for x in data]; return result
Review: Issue: Using list comprehension for side effects. Better: return [x*2 for x in data]

Example 3:
Code: try: file = open('data.txt'); content = file.read(); file.close()
Review: Issue: File not closed if error occurs. Better: Use 'with open()' context manager.

Now review this code:
{code_to_review}

Review:
"""

# Use with agent
from langchain_nvidia_ai_endpoints import ChatNVIDIA

llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct")

code = """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total / len(numbers)
"""

review = llm.invoke(FEW_SHOT_PROMPT.format(code_to_review=code))
print(review.content)
```

### 1.5 Chain-of-Thought Prompting

**Chain-of-thought (CoT)** prompting encourages step-by-step reasoning.

```python
COT_PROMPT = """
You are a problem-solving agent. Think through problems step-by-step.

Problem: {problem}

Let's solve this step by step:

Step 1: Understand the problem
[Analyze what is being asked]

Step 2: Identify relevant information
[List key facts and constraints]

Step 3: Develop a solution approach
[Outline the strategy]

Step 4: Execute the solution
[Show the work]

Step 5: Verify the answer
[Check if solution makes sense]

Final Answer:
"""

# Example usage
from langchain_nvidia_ai_endpoints import ChatNVIDIA

llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct", temperature=0.3)

problem = """
A company has 3 data centers. Center A processes 1000 requests/sec, 
Center B processes 1500 requests/sec, and Center C processes 2000 requests/sec.
If we need to handle 6000 requests/sec total and want to distribute load 
proportionally to capacity, how many requests should each center handle?
"""

response = llm.invoke(COT_PROMPT.format(problem=problem))
print(response.content)
```

> 📝 **EXAM TIP**
> 
> Chain-of-thought prompting is essential for complex reasoning tasks. Understand when to use CoT vs. direct prompting. CoT adds latency but improves accuracy for multi-step problems.


---

## 2. Tool Integration and Function Calling

### 2.1 Understanding Tool Integration

**Tools** extend agent capabilities by connecting to external systems, APIs, and functions.

**Common Tool Categories:**

| Category | Examples | Use Cases |
|----------|----------|-----------|
| **Search** | Web search, document search | Information retrieval |
| **Computation** | Calculator, code execution | Mathematical operations |
| **Data Access** | Database queries, API calls | Retrieve structured data |
| **Actions** | Send email, create ticket | Perform operations |
| **Multimodal** | Image generation, speech-to-text | Handle non-text data |

### 2.2 Defining Custom Tools

**LangChain Tool Definition:**

```python
from langchain.tools import Tool
from langchain.pydantic_v1 import BaseModel, Field
import requests

# Method 1: Simple function wrapper
def get_weather(location: str) -> str:
    """Get current weather for a location"""
    try:
        # Call weather API
        response = requests.get(
            f"https://api.weather.com/v1/current",
            params={"location": location, "api_key": "your-key"},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        return f"Weather in {location}: {data['temperature']}°F, {data['conditions']}"
    except requests.RequestException as e:
        return f"Error fetching weather: {str(e)}"

weather_tool = Tool(
    name="get_weather",
    func=get_weather,
    description="Get current weather for a location. Input should be a city name."
)

# Method 2: Structured tool with Pydantic
class WeatherInput(BaseModel):
    location: str = Field(description="City name or zip code")
    units: str = Field(default="fahrenheit", description="Temperature units: fahrenheit or celsius")

class WeatherTool(BaseTool):
    name = "weather_lookup"
    description = "Get current weather conditions for a location"
    args_schema = WeatherInput
    
    def _run(self, location: str, units: str = "fahrenheit") -> str:
        """Execute the tool"""
        try:
            response = requests.get(
                "https://api.weather.com/v1/current",
                params={"location": location, "units": units, "api_key": "your-key"},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            return f"Temperature: {data['temp']}°{units[0].upper()}, Conditions: {data['conditions']}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def _arun(self, location: str, units: str = "fahrenheit") -> str:
        """Async version"""
        # Implement async version for better performance
        raise NotImplementedError("Async not implemented")
```

### 2.3 Tool Integration with Agents

**Creating an Agent with Tools:**

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.tools import Tool

# Define multiple tools
def search_documents(query: str) -> str:
    """Search internal documentation"""
    # Implementation
    return f"Found documents about: {query}"

def create_ticket(description: str) -> str:
    """Create a support ticket"""
    # Implementation
    ticket_id = "TICK-12345"
    return f"Created ticket {ticket_id}: {description}"

def check_system_status(system: str) -> str:
    """Check if a system is operational"""
    # Implementation
    return f"System {system} is operational"

# Create tool list
tools = [
    Tool(
        name="search_docs",
        func=search_documents,
        description="Search internal documentation. Input: search query"
    ),
    Tool(
        name="create_ticket",
        func=create_ticket,
        description="Create a support ticket. Input: issue description"
    ),
    Tool(
        name="check_status",
        func=check_system_status,
        description="Check system status. Input: system name"
    )
]

# Initialize NVIDIA LLM
llm = ChatNVIDIA(
    model="meta/llama-3.1-70b-instruct",
    nvidia_api_key="your-api-key",
    temperature=0.7
)

# Create agent
from langchain import hub
react_prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, react_prompt)

# Create executor with error handling
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    max_execution_time=30,  # Timeout after 30 seconds
    handle_parsing_errors=True,
    return_intermediate_steps=True
)

# Execute
result = agent_executor.invoke({
    "input": "Check if the payment system is working, and if not, create a ticket"
})

print(result["output"])
print(f"Steps taken: {len(result['intermediate_steps'])}")
```

### 2.4 API Integration Best Practices

**Robust API Tool Implementation:**

```python
import requests
from typing import Optional, Dict, Any
import logging
from functools import wraps
import time

logger = logging.getLogger(__name__)

class APITool:
    """Base class for API-based tools with error handling"""
    
    def __init__(self, base_url: str, api_key: str, timeout: int = 10):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        retries: int = 3
    ) -> Dict[Any, Any]:
        """Make HTTP request with retry logic"""
        url = f"{self.base_url}/{endpoint}"
        
        for attempt in range(retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.Timeout:
                logger.warning(f"Request timeout (attempt {attempt + 1}/{retries})")
                if attempt == retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code >= 500:
                    # Server error - retry
                    logger.warning(f"Server error {e.response.status_code} (attempt {attempt + 1}/{retries})")
                    if attempt == retries - 1:
                        raise
                    time.sleep(2 ** attempt)
                else:
                    # Client error - don't retry
                    logger.error(f"Client error: {e.response.status_code}")
                    raise
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {str(e)}")
                if attempt == retries - 1:
                    raise
                time.sleep(2 ** attempt)
        
        raise Exception("Max retries exceeded")

# Example: CRM API Tool
class CRMTool(APITool):
    """Tool for interacting with CRM system"""
    
    def get_customer_info(self, customer_id: str) -> str:
        """Retrieve customer information"""
        try:
            data = self._make_request("GET", f"customers/{customer_id}")
            return f"Customer: {data['name']}, Status: {data['status']}, Tier: {data['tier']}"
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return f"Customer {customer_id} not found"
            return f"Error retrieving customer: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def create_case(self, customer_id: str, description: str, priority: str = "medium") -> str:
        """Create a support case"""
        try:
            data = self._make_request(
                "POST",
                "cases",
                json_data={
                    "customer_id": customer_id,
                    "description": description,
                    "priority": priority
                }
            )
            return f"Created case {data['case_id']} with priority {priority}"
        except Exception as e:
            return f"Failed to create case: {str(e)}"

# Use with agent
crm = CRMTool(base_url="https://api.crm.com/v1", api_key="your-key")

crm_tools = [
    Tool(
        name="get_customer",
        func=crm.get_customer_info,
        description="Get customer information. Input: customer_id"
    ),
    Tool(
        name="create_case",
        func=lambda desc: crm.create_case("CUST-123", desc),
        description="Create support case. Input: issue description"
    )
]
```

> 📝 **EXAM TIP**
> 
> API integration is a common exam topic. Understand retry logic, timeout handling, and error responses. Know when to retry (5xx errors, timeouts) vs. when not to (4xx errors).


### 2.5 Multimodal Tool Integration

**Integrating Vision and Audio Models:**

```python
from langchain.tools import Tool
from langchain_nvidia_ai_endpoints import ChatNVIDIA
import base64
from PIL import Image
import io

class MultimodalTools:
    """Tools for handling images and audio"""
    
    def __init__(self, nvidia_api_key: str):
        self.api_key = nvidia_api_key
        # Initialize vision model
        self.vision_llm = ChatNVIDIA(
            model="microsoft/phi-3-vision-128k-instruct",
            nvidia_api_key=nvidia_api_key
        )
    
    def analyze_image(self, image_path: str, question: str) -> str:
        """Analyze an image and answer questions about it"""
        try:
            # Load and encode image
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode()
            
            # Create multimodal prompt
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                    ]
                }
            ]
            
            response = self.vision_llm.invoke(messages)
            return response.content
            
        except FileNotFoundError:
            return f"Image file not found: {image_path}"
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
    
    def generate_image_description(self, image_path: str) -> str:
        """Generate a detailed description of an image"""
        return self.analyze_image(
            image_path,
            "Provide a detailed description of this image, including objects, people, setting, and any text visible."
        )
    
    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from an image (OCR)"""
        return self.analyze_image(
            image_path,
            "Extract all text visible in this image. Return only the text, maintaining the original layout."
        )

# Create tools
multimodal = MultimodalTools(nvidia_api_key="your-key")

vision_tools = [
    Tool(
        name="analyze_image",
        func=lambda path: multimodal.analyze_image(path, "What is in this image?"),
        description="Analyze an image. Input: image file path"
    ),
    Tool(
        name="extract_text",
        func=multimodal.extract_text_from_image,
        description="Extract text from an image. Input: image file path"
    )
]

# Use in agent
from langchain.agents import create_react_agent, AgentExecutor

llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct")
agent = create_react_agent(llm, vision_tools, react_prompt)
executor = AgentExecutor(agent=agent, tools=vision_tools, verbose=True)

result = executor.invoke({
    "input": "Analyze the screenshot at /path/to/error_screenshot.png and tell me what error is shown"
})
```

---

## 3. Error Handling and Resilience

### 3.1 Error Handling Patterns

**Pattern 1: Retry Logic with Exponential Backoff**

```python
import time
from typing import Callable, Any, Optional
import logging

logger = logging.getLogger(__name__)

def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Callable:
    """Decorator for retry logic with exponential backoff"""
    
    def wrapper(*args, **kwargs) -> Any:
        delay = initial_delay
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                last_exception = e
                if attempt < max_retries - 1:
                    logger.warning(
                        f"Attempt {attempt + 1} failed: {str(e)}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                    delay *= backoff_factor
                else:
                    logger.error(f"All {max_retries} attempts failed")
        
        raise last_exception
    
    return wrapper

# Usage example
@retry_with_backoff(max_retries=3, initial_delay=1.0, exceptions=(requests.RequestException,))
def call_external_api(endpoint: str) -> dict:
    """Call external API with automatic retry"""
    response = requests.get(endpoint, timeout=5)
    response.raise_for_status()
    return response.json()

# Use in tool
def search_tool_with_retry(query: str) -> str:
    """Search tool with built-in retry logic"""
    try:
        results = call_external_api(f"https://api.search.com?q={query}")
        return f"Found: {results['summary']}"
    except requests.RequestException as e:
        return f"Search failed after retries: {str(e)}"
```

**Pattern 2: Circuit Breaker**

```python
from datetime import datetime, timedelta
from enum import Enum
from typing import Callable

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """Circuit breaker pattern for failing services"""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: int = 60,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        
        if self.state == CircuitState.OPEN:
            # Check if timeout has passed
            if datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout):
                self.state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker entering HALF_OPEN state")
            else:
                raise Exception("Circuit breaker is OPEN - service unavailable")
        
        try:
            result = func(*args, **kwargs)
            
            # Success - reset if in HALF_OPEN
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                logger.info("Circuit breaker CLOSED - service recovered")
            
            return result
            
        except self.expected_exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                logger.error(f"Circuit breaker OPEN after {self.failure_count} failures")
            
            raise

# Usage example
api_circuit_breaker = CircuitBreaker(
    failure_threshold=5,
    timeout=60,
    expected_exception=requests.RequestException
)

def call_unreliable_api(endpoint: str) -> dict:
    """Call API protected by circuit breaker"""
    def _call():
        response = requests.get(endpoint, timeout=5)
        response.raise_for_status()
        return response.json()
    
    try:
        return api_circuit_breaker.call(_call)
    except Exception as e:
        logger.error(f"API call failed: {str(e)}")
        # Return fallback response
        return {"status": "unavailable", "message": "Service temporarily unavailable"}

# Use in agent tool
def search_with_circuit_breaker(query: str) -> str:
    """Search tool with circuit breaker protection"""
    try:
        results = call_unreliable_api(f"https://api.search.com?q={query}")
        if results["status"] == "unavailable":
            return "Search service is temporarily unavailable. Please try again later."
        return f"Found: {results['summary']}"
    except Exception as e:
        return f"Search failed: {str(e)}"
```

**Pattern 3: Graceful Degradation**

```python
class GracefulAgent:
    """Agent with graceful degradation capabilities"""
    
    def __init__(self, primary_llm, fallback_llm, tools):
        self.primary_llm = primary_llm
        self.fallback_llm = fallback_llm
        self.tools = tools
        self.primary_failures = 0
        self.max_failures = 3
    
    def invoke(self, query: str) -> str:
        """Invoke agent with graceful degradation"""
        
        # Try primary LLM
        if self.primary_failures < self.max_failures:
            try:
                response = self._invoke_with_llm(self.primary_llm, query)
                self.primary_failures = 0  # Reset on success
                return response
            except Exception as e:
                logger.warning(f"Primary LLM failed: {str(e)}")
                self.primary_failures += 1
        
        # Fallback to secondary LLM
        try:
            logger.info("Using fallback LLM")
            return self._invoke_with_llm(self.fallback_llm, query)
        except Exception as e:
            logger.error(f"Fallback LLM also failed: {str(e)}")
            
            # Last resort: rule-based response
            return self._rule_based_response(query)
    
    def _invoke_with_llm(self, llm, query: str) -> str:
        """Invoke LLM with tools"""
        agent = create_react_agent(llm, self.tools, react_prompt)
        executor = AgentExecutor(agent=agent, tools=self.tools)
        result = executor.invoke({"input": query})
        return result["output"]
    
    def _rule_based_response(self, query: str) -> str:
        """Simple rule-based fallback"""
        query_lower = query.lower()
        
        if "help" in query_lower or "support" in query_lower:
            return "I'm experiencing technical difficulties. Please contact support at support@company.com"
        elif "status" in query_lower:
            return "System status: Degraded mode. Some features may be unavailable."
        else:
            return "I'm currently unable to process your request. Please try again later or contact support."

# Usage
from langchain_nvidia_ai_endpoints import ChatNVIDIA

primary = ChatNVIDIA(model="meta/llama-3.1-70b-instruct")  # Larger, better model
fallback = ChatNVIDIA(model="meta/llama-3.1-8b-instruct")  # Smaller, faster model

agent = GracefulAgent(primary, fallback, tools)
response = agent.invoke("What's the weather in Tokyo?")
```

> 📝 **EXAM TIP**
> 
> Error handling is critical for production agents. Understand the three patterns: Retry (transient failures), Circuit Breaker (cascading failures), Graceful Degradation (service unavailability). Know when to use each.


### 3.2 Timeout Management

**Implementing Timeouts:**

```python
import signal
from contextlib import contextmanager
from typing import Callable, Any

class TimeoutError(Exception):
    """Raised when operation times out"""
    pass

@contextmanager
def timeout(seconds: int):
    """Context manager for timeout"""
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Operation timed out after {seconds} seconds")
    
    # Set the signal handler
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)

# Usage in agent
def agent_with_timeout(query: str, max_time: int = 30) -> str:
    """Execute agent with timeout"""
    try:
        with timeout(max_time):
            result = agent_executor.invoke({"input": query})
            return result["output"]
    except TimeoutError:
        logger.error(f"Agent execution timed out after {max_time}s")
        return "I'm taking too long to process this request. Let me try a simpler approach."
    except Exception as e:
        logger.error(f"Agent execution failed: {str(e)}")
        return "I encountered an error processing your request."

# Alternative: Using concurrent.futures
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

def agent_with_thread_timeout(query: str, max_time: int = 30) -> str:
    """Execute agent with thread-based timeout"""
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(agent_executor.invoke, {"input": query})
        try:
            result = future.result(timeout=max_time)
            return result["output"]
        except FuturesTimeoutError:
            logger.error(f"Agent timed out after {max_time}s")
            return "Request timed out. Please try a simpler query."
        except Exception as e:
            logger.error(f"Agent failed: {str(e)}")
            return "An error occurred processing your request."
```

### 3.3 Error Recovery Strategies

**Strategy 1: Fallback Responses**

```python
class ErrorRecoveryAgent:
    """Agent with multiple error recovery strategies"""
    
    def __init__(self, agent_executor):
        self.agent_executor = agent_executor
        self.error_count = 0
    
    def invoke_with_recovery(self, query: str) -> str:
        """Invoke agent with error recovery"""
        
        # Strategy 1: Try normal execution
        try:
            result = self.agent_executor.invoke({"input": query})
            self.error_count = 0
            return result["output"]
        except Exception as e:
            logger.warning(f"Normal execution failed: {str(e)}")
            self.error_count += 1
        
        # Strategy 2: Simplify query and retry
        try:
            simplified_query = self._simplify_query(query)
            logger.info(f"Retrying with simplified query: {simplified_query}")
            result = self.agent_executor.invoke({"input": simplified_query})
            return result["output"]
        except Exception as e:
            logger.warning(f"Simplified execution failed: {str(e)}")
        
        # Strategy 3: Use cached response if available
        cached = self._get_cached_response(query)
        if cached:
            logger.info("Using cached response")
            return f"{cached} (Note: This is a cached response)"
        
        # Strategy 4: Return helpful error message
        return self._generate_error_response(query)
    
    def _simplify_query(self, query: str) -> str:
        """Simplify complex query"""
        # Remove complex clauses, focus on main question
        if "?" in query:
            return query.split("?")[0] + "?"
        return query[:100]  # Truncate long queries
    
    def _get_cached_response(self, query: str) -> Optional[str]:
        """Check cache for similar queries"""
        # Implementation would check vector store for similar queries
        return None
    
    def _generate_error_response(self, query: str) -> str:
        """Generate helpful error message"""
        return f"""I'm having trouble processing your request right now. Here's what you can try:

1. Rephrase your question more simply
2. Break your question into smaller parts
3. Try again in a moment
4. Contact support if the issue persists

Your query: {query[:100]}..."""
```

---

## 4. NVIDIA Platform Integration

### 4.1 NVIDIA NIM (Inference Microservices)

**NVIDIA NIM** provides optimized, production-ready inference for LLMs with 10-100x performance improvements.

**Key Benefits:**
- **High Performance** - TensorRT-LLM optimization
- **Scalability** - Automatic batching and load balancing
- **Production Ready** - Built-in monitoring and health checks
- **Easy Deployment** - Docker containers with simple configuration

**Deploying with NIM:**

```python
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# Connect to NVIDIA NIM endpoint
llm = ChatNVIDIA(
    model="meta/llama-3.1-70b-instruct",
    nvidia_api_key="your-api-key",
    base_url="https://integrate.api.nvidia.com/v1",
    temperature=0.7,
    max_tokens=1024,
    top_p=0.9
)

# NIM automatically handles:
# - Request batching for throughput
# - GPU memory management
# - Load balancing across instances
# - Caching for repeated queries

response = llm.invoke("Explain quantum computing")
print(response.content)
```

**Self-Hosted NIM Deployment:**

```bash
# Pull NIM container
docker pull nvcr.io/nim/meta/llama-3.1-70b-instruct:latest

# Run NIM container
docker run -d \
  --gpus all \
  --name llama-nim \
  -p 8000:8000 \
  -e NGC_API_KEY=your-ngc-key \
  -v $HOME/.cache/nim:/opt/nim/.cache \
  nvcr.io/nim/meta/llama-3.1-70b-instruct:latest

# Check health
curl http://localhost:8000/v1/health

# Use in agent
llm = ChatNVIDIA(
    base_url="http://localhost:8000/v1",
    model="meta/llama-3.1-70b-instruct"
)
```

**NIM Configuration for Production:**

```python
# config.yaml for NIM
nim_config = {
    "model": {
        "name": "meta/llama-3.1-70b-instruct",
        "max_batch_size": 32,
        "max_sequence_length": 4096
    },
    "inference": {
        "tensor_parallel_size": 4,  # Use 4 GPUs
        "pipeline_parallel_size": 1,
        "max_num_sequences": 256
    },
    "optimization": {
        "enable_chunked_prefill": True,
        "enable_prefix_caching": True,
        "gpu_memory_utilization": 0.9
    },
    "monitoring": {
        "enable_metrics": True,
        "metrics_port": 9090
    }
}
```

### 4.2 TensorRT-LLM Optimization

**TensorRT-LLM** optimizes LLM inference for NVIDIA GPUs, reducing latency by 2-8x.

**Key Optimizations:**
- **Kernel Fusion** - Combine operations for efficiency
- **Quantization** - FP16, INT8, INT4 precision
- **In-flight Batching** - Dynamic batching during generation
- **KV Cache Optimization** - Efficient attention caching

**Using TensorRT-LLM with Agents:**

```python
# TensorRT-LLM is integrated into NIM
# Configure optimization level when deploying

from langchain_nvidia_ai_endpoints import ChatNVIDIA

# High-performance configuration
llm_optimized = ChatNVIDIA(
    model="meta/llama-3.1-70b-instruct",
    nvidia_api_key="your-api-key",
    # NIM automatically uses TensorRT-LLM optimizations
    temperature=0.7,
    max_tokens=512  # Shorter responses = faster
)

# For latency-critical applications
llm_fast = ChatNVIDIA(
    model="meta/llama-3.1-8b-instruct",  # Smaller model
    nvidia_api_key="your-api-key",
    temperature=0.5,
    max_tokens=256
)

# Use in agent with timeout
from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_execution_time=5,  # 5 second timeout
    verbose=True
)
```

**Performance Comparison:**

| Configuration | Latency (ms) | Throughput (req/s) | Cost |
|---------------|--------------|-------------------|------|
| **Standard PyTorch** | 2000 | 10 | High |
| **TensorRT-LLM FP16** | 500 | 40 | Medium |
| **TensorRT-LLM INT8** | 250 | 80 | Low |
| **NIM (TensorRT-LLM + Batching)** | 200 | 100+ | Low |

> 📝 **EXAM TIP**
> 
> Understand the performance benefits of NIM and TensorRT-LLM. Know when to use different quantization levels (FP16 for accuracy, INT8 for speed, INT4 for maximum throughput).


### 4.3 Streaming Responses

**Real-time streaming** provides better user experience for long-running agent tasks.

**Implementing Streaming:**

```python
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler

# Custom streaming callback
class CustomStreamingCallback(BaseCallbackHandler):
    """Custom callback for streaming responses"""
    
    def __init__(self):
        self.tokens = []
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Called when new token is generated"""
        self.tokens.append(token)
        print(token, end="", flush=True)
    
    def on_llm_end(self, response, **kwargs) -> None:
        """Called when generation completes"""
        print("\n[Generation complete]")
    
    def on_llm_error(self, error: Exception, **kwargs) -> None:
        """Called on error"""
        print(f"\n[Error: {str(error)}]")

# Create streaming LLM
llm_streaming = ChatNVIDIA(
    model="meta/llama-3.1-70b-instruct",
    nvidia_api_key="your-api-key",
    streaming=True,
    callbacks=[CustomStreamingCallback()]
)

# Use with agent
from langchain.agents import create_react_agent, AgentExecutor

agent = create_react_agent(llm_streaming, tools, react_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    callbacks=[CustomStreamingCallback()],
    verbose=True
)

# Execute with streaming
response = agent_executor.invoke({"input": "Write a detailed analysis of market trends"})
```

**Streaming with Gradio UI:**

```python
import gradio as gr
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.agents import AgentExecutor, create_react_agent

def create_streaming_agent():
    """Create agent with streaming support"""
    llm = ChatNVIDIA(
        model="meta/llama-3.1-70b-instruct",
        nvidia_api_key="your-api-key",
        streaming=True,
        temperature=0.7
    )
    
    agent = create_react_agent(llm, tools, react_prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

def chat_with_streaming(message, history):
    """Chat function with streaming"""
    agent_executor = create_streaming_agent()
    
    # Stream response token by token
    response = ""
    for chunk in agent_executor.stream({"input": message}):
        if "output" in chunk:
            response = chunk["output"]
            yield response
        elif "intermediate_steps" in chunk:
            # Show thinking process
            for step in chunk["intermediate_steps"]:
                action, observation = step
                yield f"🤔 Thinking: {action.log}\n"

# Create Gradio interface
demo = gr.ChatInterface(
    fn=chat_with_streaming,
    title="Streaming Agent",
    description="Agent with real-time streaming responses",
    examples=[
        "Analyze the latest tech trends",
        "Help me debug this error",
        "Create a project plan"
    ]
)

demo.launch()
```

**Streaming Best Practices:**

```python
class StreamingAgent:
    """Production-ready streaming agent"""
    
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.agent = create_react_agent(llm, tools, react_prompt)
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=tools,
            max_iterations=5,
            handle_parsing_errors=True
        )
    
    def stream_response(self, query: str, callback=None):
        """Stream response with progress updates"""
        try:
            # Stream intermediate steps
            for chunk in self.executor.stream({"input": query}):
                if callback:
                    if "actions" in chunk:
                        # Agent is taking action
                        action = chunk["actions"][0]
                        callback({
                            "type": "action",
                            "tool": action.tool,
                            "input": action.tool_input
                        })
                    elif "steps" in chunk:
                        # Action completed
                        step = chunk["steps"][0]
                        callback({
                            "type": "observation",
                            "result": step[1]
                        })
                    elif "output" in chunk:
                        # Final output
                        callback({
                            "type": "output",
                            "content": chunk["output"]
                        })
                        
        except Exception as e:
            if callback:
                callback({
                    "type": "error",
                    "message": str(e)
                })

# Usage
def progress_callback(event):
    """Handle streaming events"""
    if event["type"] == "action":
        print(f"🔧 Using tool: {event['tool']}")
    elif event["type"] == "observation":
        print(f"📊 Result: {event['result'][:100]}...")
    elif event["type"] == "output":
        print(f"✅ Final: {event['content']}")
    elif event["type"] == "error":
        print(f"❌ Error: {event['message']}")

agent = StreamingAgent(llm_streaming, tools)
agent.stream_response("What's the weather in Tokyo?", callback=progress_callback)
```

---

## 5. Dynamic Conversation Flows

### 5.1 Conversation State Management

**Managing Multi-Turn Conversations:**

```python
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.chains import ConversationChain
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# Method 1: Buffer Memory (keep all messages)
memory_buffer = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Method 2: Summary Memory (summarize old messages)
llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct")
memory_summary = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True
)

# Create conversation chain
conversation = ConversationChain(
    llm=llm,
    memory=memory_buffer,
    verbose=True
)

# Multi-turn conversation
response1 = conversation.predict(input="My name is Alice")
# "Nice to meet you, Alice!"

response2 = conversation.predict(input="What's my name?")
# "Your name is Alice"

response3 = conversation.predict(input="I work in healthcare")
# "That's interesting, Alice. Healthcare is an important field."

# Memory persists context across turns
print(memory_buffer.load_memory_variables({}))
```

### 5.2 Context-Aware Routing

**Route conversations based on context:**

```python
from typing import Dict, Any
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class ContextAwareAgent:
    """Agent that routes based on conversation context"""
    
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.conversation_history = []
        self.user_profile = {}
    
    def process_message(self, message: str) -> str:
        """Process message with context awareness"""
        
        # Update context
        self.conversation_history.append({"role": "user", "content": message})
        
        # Analyze context
        context = self._analyze_context()
        
        # Route based on context
        if context["intent"] == "technical_support":
            response = self._handle_technical_support(message, context)
        elif context["intent"] == "general_inquiry":
            response = self._handle_general_inquiry(message, context)
        elif context["intent"] == "escalation":
            response = self._handle_escalation(message, context)
        else:
            response = self._handle_default(message, context)
        
        # Update history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def _analyze_context(self) -> Dict[str, Any]:
        """Analyze conversation context"""
        # Get recent messages
        recent = self.conversation_history[-5:]
        
        # Detect intent
        intent_prompt = f"""
        Analyze this conversation and determine the user's intent:
        {recent}
        
        Intent categories: technical_support, general_inquiry, escalation, other
        Intent:
        """
        
        intent_response = self.llm.invoke(intent_prompt)
        intent = intent_response.content.strip().lower()
        
        # Detect sentiment
        sentiment_prompt = f"""
        Analyze the sentiment of this message: {recent[-1]['content']}
        Sentiment (positive/neutral/negative):
        """
        
        sentiment_response = self.llm.invoke(sentiment_prompt)
        sentiment = sentiment_response.content.strip().lower()
        
        return {
            "intent": intent,
            "sentiment": sentiment,
            "turn_count": len(self.conversation_history) // 2,
            "user_profile": self.user_profile
        }
    
    def _handle_technical_support(self, message: str, context: Dict) -> str:
        """Handle technical support queries"""
        # Use specialized technical agent
        tech_agent = create_react_agent(self.llm, self.tools, tech_prompt)
        executor = AgentExecutor(agent=tech_agent, tools=self.tools)
        result = executor.invoke({"input": message})
        return result["output"]
    
    def _handle_escalation(self, message: str, context: Dict) -> str:
        """Handle escalation to human"""
        return """I understand this is frustrating. Let me connect you with a human specialist 
who can better assist you. Please hold for a moment."""
```

### 5.3 Adaptive Response Generation

**Adapt responses based on user preferences:**

```python
class AdaptiveAgent:
    """Agent that adapts to user preferences"""
    
    def __init__(self, llm):
        self.llm = llm
        self.user_preferences = {
            "verbosity": "medium",  # low, medium, high
            "technical_level": "intermediate",  # beginner, intermediate, expert
            "format": "conversational"  # conversational, formal, concise
        }
    
    def generate_response(self, query: str) -> str:
        """Generate response adapted to user preferences"""
        
        # Build adaptive prompt
        prompt = self._build_adaptive_prompt(query)
        
        # Generate response
        response = self.llm.invoke(prompt)
        
        return response.content
    
    def _build_adaptive_prompt(self, query: str) -> str:
        """Build prompt based on user preferences"""
        
        # Verbosity instructions
        verbosity_map = {
            "low": "Be extremely concise. Use 1-2 sentences maximum.",
            "medium": "Provide a balanced response with key points.",
            "high": "Provide a detailed, comprehensive explanation."
        }
        
        # Technical level instructions
        technical_map = {
            "beginner": "Explain in simple terms, avoid jargon.",
            "intermediate": "Use technical terms but explain them.",
            "expert": "Use technical terminology freely, assume deep knowledge."
        }
        
        # Format instructions
        format_map = {
            "conversational": "Use a friendly, conversational tone.",
            "formal": "Use professional, formal language.",
            "concise": "Use bullet points and short sentences."
        }
        
        prompt = f"""
{verbosity_map[self.user_preferences['verbosity']]}
{technical_map[self.user_preferences['technical_level']]}
{format_map[self.user_preferences['format']]}

User Query: {query}

Response:
"""
        
        return prompt
    
    def update_preferences(self, feedback: Dict[str, str]):
        """Update preferences based on user feedback"""
        if "too_long" in feedback:
            self.user_preferences["verbosity"] = "low"
        elif "too_short" in feedback:
            self.user_preferences["verbosity"] = "high"
        
        if "too_technical" in feedback:
            self.user_preferences["technical_level"] = "beginner"
        elif "too_simple" in feedback:
            self.user_preferences["technical_level"] = "expert"

# Usage
agent = AdaptiveAgent(llm)

# Initial response
response1 = agent.generate_response("Explain machine learning")

# User provides feedback
agent.update_preferences({"too_technical": True})

# Adapted response
response2 = agent.generate_response("Explain machine learning")
# Now uses simpler language
```


---

## 6. Evaluation and Refinement

### 6.1 Agent Performance Metrics

**Key Metrics for Agent Evaluation:**

| Metric | Description | Target | Measurement |
|--------|-------------|--------|-------------|
| **Task Success Rate** | % of tasks completed successfully | >90% | Successful completions / Total attempts |
| **Average Response Time** | Mean time to generate response | <2s | Σ(response times) / count |
| **Tool Call Accuracy** | % of correct tool selections | >95% | Correct calls / Total calls |
| **Error Rate** | % of requests resulting in errors | <5% | Errors / Total requests |
| **User Satisfaction** | User rating of responses | >4/5 | Average user rating |
| **Cost per Request** | Average cost per interaction | <$0.01 | Total cost / Total requests |

**Implementing Metrics Collection:**

```python
import time
from datetime import datetime
from typing import Dict, Any, List
import json

class AgentMetrics:
    """Collect and analyze agent performance metrics"""
    
    def __init__(self):
        self.metrics = []
    
    def record_interaction(
        self,
        query: str,
        response: str,
        success: bool,
        response_time: float,
        tools_used: List[str],
        error: Optional[str] = None,
        cost: float = 0.0
    ):
        """Record a single interaction"""
        self.metrics.append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "success": success,
            "response_time": response_time,
            "tools_used": tools_used,
            "error": error,
            "cost": cost
        })
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics"""
        if not self.metrics:
            return {}
        
        total = len(self.metrics)
        successful = sum(1 for m in self.metrics if m["success"])
        
        return {
            "total_interactions": total,
            "success_rate": successful / total * 100,
            "average_response_time": sum(m["response_time"] for m in self.metrics) / total,
            "error_rate": (total - successful) / total * 100,
            "total_cost": sum(m["cost"] for m in self.metrics),
            "average_cost": sum(m["cost"] for m in self.metrics) / total,
            "most_used_tools": self._get_tool_usage()
        }
    
    def _get_tool_usage(self) -> Dict[str, int]:
        """Get tool usage statistics"""
        tool_counts = {}
        for metric in self.metrics:
            for tool in metric["tools_used"]:
                tool_counts[tool] = tool_counts.get(tool, 0) + 1
        return dict(sorted(tool_counts.items(), key=lambda x: x[1], reverse=True))

# Usage with agent
class MonitoredAgent:
    """Agent with built-in metrics collection"""
    
    def __init__(self, agent_executor):
        self.agent_executor = agent_executor
        self.metrics = AgentMetrics()
    
    def invoke(self, query: str) -> str:
        """Invoke agent and collect metrics"""
        start_time = time.time()
        tools_used = []
        error = None
        success = False
        response = ""
        
        try:
            result = self.agent_executor.invoke({"input": query})
            response = result["output"]
            success = True
            
            # Extract tools used
            if "intermediate_steps" in result:
                tools_used = [step[0].tool for step in result["intermediate_steps"]]
            
        except Exception as e:
            error = str(e)
            response = "An error occurred"
        
        finally:
            response_time = time.time() - start_time
            
            # Estimate cost (example: $0.002 per 1K tokens)
            estimated_tokens = len(query.split()) + len(response.split())
            cost = (estimated_tokens / 1000) * 0.002
            
            # Record metrics
            self.metrics.record_interaction(
                query=query,
                response=response,
                success=success,
                response_time=response_time,
                tools_used=tools_used,
                error=error,
                cost=cost
            )
        
        return response
    
    def get_performance_report(self) -> str:
        """Generate performance report"""
        summary = self.metrics.get_summary()
        
        report = f"""
Agent Performance Report
========================

Total Interactions: {summary['total_interactions']}
Success Rate: {summary['success_rate']:.2f}%
Error Rate: {summary['error_rate']:.2f}%
Average Response Time: {summary['average_response_time']:.3f}s
Total Cost: ${summary['total_cost']:.4f}
Average Cost per Request: ${summary['average_cost']:.6f}

Most Used Tools:
"""
        for tool, count in summary['most_used_tools'].items():
            report += f"  - {tool}: {count} times\n"
        
        return report

# Usage
monitored_agent = MonitoredAgent(agent_executor)

# Run multiple queries
queries = [
    "What's the weather in Tokyo?",
    "Calculate 15% of 250",
    "Search for recent AI news"
]

for query in queries:
    response = monitored_agent.invoke(query)
    print(f"Q: {query}\nA: {response}\n")

# Get performance report
print(monitored_agent.get_performance_report())
```

### 6.2 A/B Testing for Agents

**Compare different agent configurations:**

```python
import random
from typing import Dict, List

class ABTestingFramework:
    """Framework for A/B testing agent configurations"""
    
    def __init__(self, variant_a, variant_b, split_ratio=0.5):
        self.variant_a = variant_a
        self.variant_b = variant_b
        self.split_ratio = split_ratio
        self.results_a = []
        self.results_b = []
    
    def route_request(self, query: str) -> tuple:
        """Route request to variant A or B"""
        if random.random() < self.split_ratio:
            variant = "A"
            response = self.variant_a.invoke(query)
            self.results_a.append({
                "query": query,
                "response": response,
                "variant": "A"
            })
        else:
            variant = "B"
            response = self.variant_b.invoke(query)
            self.results_b.append({
                "query": query,
                "response": response,
                "variant": "B"
            })
        
        return variant, response
    
    def collect_feedback(self, variant: str, rating: int):
        """Collect user feedback"""
        if variant == "A":
            self.results_a[-1]["rating"] = rating
        else:
            self.results_b[-1]["rating"] = rating
    
    def analyze_results(self) -> Dict[str, Any]:
        """Analyze A/B test results"""
        avg_rating_a = sum(r.get("rating", 0) for r in self.results_a) / len(self.results_a) if self.results_a else 0
        avg_rating_b = sum(r.get("rating", 0) for r in self.results_b) / len(self.results_b) if self.results_b else 0
        
        return {
            "variant_a": {
                "count": len(self.results_a),
                "average_rating": avg_rating_a
            },
            "variant_b": {
                "count": len(self.results_b),
                "average_rating": avg_rating_b
            },
            "winner": "A" if avg_rating_a > avg_rating_b else "B",
            "improvement": abs(avg_rating_a - avg_rating_b) / min(avg_rating_a, avg_rating_b) * 100
        }

# Example: Test different prompt strategies
variant_a = MonitoredAgent(agent_executor_detailed)  # Detailed prompts
variant_b = MonitoredAgent(agent_executor_concise)   # Concise prompts

ab_test = ABTestingFramework(variant_a, variant_b)

# Run test
for query in test_queries:
    variant, response = ab_test.route_request(query)
    print(f"Variant {variant}: {response}")
    
    # Simulate user feedback
    rating = random.randint(3, 5)  # In production, get real user ratings
    ab_test.collect_feedback(variant, rating)

# Analyze results
results = ab_test.analyze_results()
print(f"Winner: Variant {results['winner']}")
print(f"Improvement: {results['improvement']:.2f}%")
```

### 6.3 Iterative Refinement Process

**Continuous improvement workflow:**

```python
class AgentRefinementPipeline:
    """Pipeline for iterative agent refinement"""
    
    def __init__(self, agent, test_cases):
        self.agent = agent
        self.test_cases = test_cases
        self.refinement_history = []
    
    def evaluate_current_version(self) -> Dict[str, Any]:
        """Evaluate current agent version"""
        results = []
        
        for test_case in self.test_cases:
            response = self.agent.invoke(test_case["query"])
            
            # Evaluate response quality
            score = self._evaluate_response(
                response,
                test_case["expected_behavior"]
            )
            
            results.append({
                "query": test_case["query"],
                "response": response,
                "score": score,
                "passed": score >= test_case["threshold"]
            })
        
        avg_score = sum(r["score"] for r in results) / len(results)
        pass_rate = sum(1 for r in results if r["passed"]) / len(results) * 100
        
        return {
            "average_score": avg_score,
            "pass_rate": pass_rate,
            "results": results
        }
    
    def _evaluate_response(self, response: str, expected: str) -> float:
        """Evaluate response quality (0-1 score)"""
        # In production, use LLM-based evaluation or human review
        # Simple example: check if key terms are present
        key_terms = expected.lower().split()
        response_lower = response.lower()
        
        matches = sum(1 for term in key_terms if term in response_lower)
        return matches / len(key_terms)
    
    def identify_failure_patterns(self, evaluation: Dict) -> List[str]:
        """Identify common failure patterns"""
        failures = [r for r in evaluation["results"] if not r["passed"]]
        
        patterns = []
        
        # Analyze failures
        if len(failures) > len(evaluation["results"]) * 0.3:
            patterns.append("High failure rate - review prompt template")
        
        # Check for specific failure types
        tool_failures = [f for f in failures if "tool" in f["query"].lower()]
        if tool_failures:
            patterns.append(f"Tool usage issues in {len(tool_failures)} cases")
        
        return patterns
    
    def suggest_improvements(self, patterns: List[str]) -> List[str]:
        """Suggest improvements based on patterns"""
        suggestions = []
        
        for pattern in patterns:
            if "prompt template" in pattern:
                suggestions.append("Refine prompt template with more specific instructions")
            elif "tool usage" in pattern:
                suggestions.append("Improve tool descriptions and examples")
            elif "timeout" in pattern:
                suggestions.append("Optimize for latency or increase timeout")
        
        return suggestions
    
    def run_refinement_cycle(self):
        """Run one refinement cycle"""
        print("=== Refinement Cycle ===\n")
        
        # Step 1: Evaluate
        print("Step 1: Evaluating current version...")
        evaluation = self.evaluate_current_version()
        print(f"Average Score: {evaluation['average_score']:.2f}")
        print(f"Pass Rate: {evaluation['pass_rate']:.1f}%\n")
        
        # Step 2: Identify patterns
        print("Step 2: Identifying failure patterns...")
        patterns = self.identify_failure_patterns(evaluation)
        for pattern in patterns:
            print(f"  - {pattern}")
        print()
        
        # Step 3: Suggest improvements
        print("Step 3: Suggesting improvements...")
        suggestions = self.suggest_improvements(patterns)
        for suggestion in suggestions:
            print(f"  - {suggestion}")
        print()
        
        # Record history
        self.refinement_history.append({
            "evaluation": evaluation,
            "patterns": patterns,
            "suggestions": suggestions
        })
        
        return suggestions

# Usage
test_cases = [
    {
        "query": "What's the weather in Tokyo?",
        "expected_behavior": "weather tokyo temperature",
        "threshold": 0.7
    },
    {
        "query": "Calculate 15% of 250",
        "expected_behavior": "calculate 15 250 37.5",
        "threshold": 0.8
    }
]

pipeline = AgentRefinementPipeline(monitored_agent, test_cases)

# Run multiple refinement cycles
for cycle in range(3):
    print(f"\n{'='*50}")
    print(f"CYCLE {cycle + 1}")
    print(f"{'='*50}\n")
    
    suggestions = pipeline.run_refinement_cycle()
    
    # In production: implement suggestions and update agent
    # agent = apply_improvements(agent, suggestions)
```

> 📝 **EXAM TIP**
> 
> Evaluation and refinement is critical for production agents. Understand key metrics (success rate, latency, cost), A/B testing methodology, and iterative improvement processes.


---

## 7. Troubleshooting Guide

### 7.1 Common Development Issues

**Issue 1: Agent Gets Stuck in Loops**

**Symptoms:**
- Agent repeatedly calls the same tool
- Exceeds max_iterations limit
- No progress toward goal

**Diagnosis:**
```python
# Enable verbose mode to see agent reasoning
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # See each step
    max_iterations=10
)

# Check intermediate steps
result = agent_executor.invoke({"input": query}, return_intermediate_steps=True)
for i, (action, observation) in enumerate(result["intermediate_steps"]):
    print(f"Step {i+1}:")
    print(f"  Action: {action.tool} - {action.tool_input}")
    print(f"  Observation: {observation}")
```

**Solutions:**
1. **Add loop detection:**
```python
class LoopDetectionAgent:
    def __init__(self, agent_executor):
        self.agent_executor = agent_executor
        self.action_history = []
    
    def invoke(self, query: str) -> str:
        self.action_history = []
        
        # Custom callback to track actions
        class LoopDetectionCallback(BaseCallbackHandler):
            def __init__(self, parent):
                self.parent = parent
            
            def on_agent_action(self, action, **kwargs):
                action_sig = f"{action.tool}:{action.tool_input}"
                self.parent.action_history.append(action_sig)
                
                # Check for loops
                if len(self.parent.action_history) >= 3:
                    last_three = self.parent.action_history[-3:]
                    if len(set(last_three)) == 1:
                        raise Exception("Loop detected: same action repeated 3 times")
        
        try:
            result = self.agent_executor.invoke(
                {"input": query},
                callbacks=[LoopDetectionCallback(self)]
            )
            return result["output"]
        except Exception as e:
            return f"Agent stopped due to: {str(e)}"
```

2. **Improve tool descriptions:**
```python
# BAD: Vague description
Tool(name="search", func=search, description="Search for information")

# GOOD: Specific description with examples
Tool(
    name="search",
    func=search,
    description="""Search for information on the web. 
    Input should be a specific search query.
    Example: 'weather in Tokyo' or 'Python tutorial'
    Do NOT repeat the same search query."""
)
```

3. **Add state tracking:**
```python
class StatefulAgent:
    def __init__(self, agent_executor):
        self.agent_executor = agent_executor
        self.completed_actions = set()
    
    def invoke(self, query: str) -> str:
        # Modify prompt to include completed actions
        context = f"Already completed: {', '.join(self.completed_actions)}"
        modified_query = f"{context}\n\nNew task: {query}"
        
        result = self.agent_executor.invoke({"input": modified_query})
        return result["output"]
```

**Issue 2: Tool Calls Fail Frequently**

**Symptoms:**
- High error rate in tool execution
- Agent returns "Tool execution failed" messages
- Timeouts or connection errors

**Diagnosis:**
```python
# Add detailed error logging
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_tool(func):
    """Decorator to debug tool execution"""
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Success: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed: {str(e)}", exc_info=True)
            raise
    return wrapper

@debug_tool
def my_tool(input_str: str) -> str:
    # Tool implementation
    pass
```

**Solutions:**
1. **Add input validation:**
```python
from pydantic import BaseModel, Field, validator

class ToolInput(BaseModel):
    query: str = Field(description="Search query")
    
    @validator('query')
    def validate_query(cls, v):
        if not v or len(v) < 3:
            raise ValueError("Query must be at least 3 characters")
        if len(v) > 200:
            raise ValueError("Query too long (max 200 characters)")
        return v

class ValidatedTool(BaseTool):
    name = "search"
    description = "Search for information"
    args_schema = ToolInput
    
    def _run(self, query: str) -> str:
        # Input is already validated
        return perform_search(query)
```

2. **Implement retry logic:**
```python
# Already covered in section 3.1
@retry_with_backoff(max_retries=3, exceptions=(requests.RequestException,))
def reliable_tool(input_str: str) -> str:
    # Tool implementation with automatic retry
    pass
```

3. **Add fallback responses:**
```python
def tool_with_fallback(input_str: str) -> str:
    """Tool with fallback behavior"""
    try:
        return primary_implementation(input_str)
    except PrimaryServiceError:
        logger.warning("Primary service failed, using fallback")
        return fallback_implementation(input_str)
    except Exception as e:
        logger.error(f"All implementations failed: {str(e)}")
        return "Service temporarily unavailable. Please try again later."
```

**Issue 3: Slow Response Times**

**Symptoms:**
- Responses take >5 seconds
- Users experience timeouts
- High latency in production

**Diagnosis:**
```python
import time
from functools import wraps

def profile_execution(func):
    """Profile function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"{func.__name__} took {duration:.3f}s")
        return result
    return wrapper

@profile_execution
def agent_invoke(query: str) -> str:
    return agent_executor.invoke({"input": query})

# Profile each component
@profile_execution
def llm_call(prompt: str) -> str:
    return llm.invoke(prompt)

@profile_execution
def tool_call(input_str: str) -> str:
    return tool.run(input_str)
```

**Solutions:**
1. **Use smaller/faster models:**
```python
# For simple queries, use smaller model
from langchain_nvidia_ai_endpoints import ChatNVIDIA

fast_llm = ChatNVIDIA(
    model="meta/llama-3.1-8b-instruct",  # Smaller, faster
    temperature=0.7,
    max_tokens=256  # Limit output length
)

# For complex queries, use larger model
powerful_llm = ChatNVIDIA(
    model="meta/llama-3.1-70b-instruct",
    temperature=0.7,
    max_tokens=1024
)

# Route based on complexity
def get_llm_for_query(query: str):
    if len(query.split()) < 20 and "?" in query:
        return fast_llm
    return powerful_llm
```

2. **Implement caching:**
```python
from functools import lru_cache
import hashlib

class CachedAgent:
    def __init__(self, agent_executor):
        self.agent_executor = agent_executor
        self.cache = {}
    
    def invoke(self, query: str) -> str:
        # Create cache key
        cache_key = hashlib.md5(query.encode()).hexdigest()
        
        # Check cache
        if cache_key in self.cache:
            logger.info("Cache hit")
            return self.cache[cache_key]
        
        # Execute and cache
        result = self.agent_executor.invoke({"input": query})
        self.cache[cache_key] = result["output"]
        
        return result["output"]
```

3. **Optimize tool calls:**
```python
# BAD: Sequential tool calls
result1 = tool1.run(input1)
result2 = tool2.run(input2)
result3 = tool3.run(input3)

# GOOD: Parallel tool calls
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:
    future1 = executor.submit(tool1.run, input1)
    future2 = executor.submit(tool2.run, input2)
    future3 = executor.submit(tool3.run, input3)
    
    result1 = future1.result()
    result2 = future2.result()
    result3 = future3.result()
```

**Issue 4: Inconsistent Responses**

**Symptoms:**
- Same query produces different answers
- Quality varies significantly
- Unpredictable behavior

**Solutions:**
1. **Lower temperature:**
```python
# More deterministic
llm = ChatNVIDIA(
    model="meta/llama-3.1-70b-instruct",
    temperature=0.1,  # Lower = more consistent
    top_p=0.9
)
```

2. **Use structured outputs:**
```python
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class StructuredResponse(BaseModel):
    answer: str = Field(description="The main answer")
    confidence: float = Field(description="Confidence score 0-1")
    sources: List[str] = Field(description="Sources used")

parser = PydanticOutputParser(pydantic_object=StructuredResponse)

prompt = PromptTemplate(
    template="Answer the question.\n{format_instructions}\n{query}",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Response will always follow the structure
```

3. **Add validation:**
```python
def validate_response(response: str, query: str) -> bool:
    """Validate response quality"""
    # Check minimum length
    if len(response) < 10:
        return False
    
    # Check if response addresses query
    query_terms = set(query.lower().split())
    response_terms = set(response.lower().split())
    overlap = len(query_terms & response_terms) / len(query_terms)
    
    if overlap < 0.3:
        return False
    
    return True

def agent_with_validation(query: str, max_retries: int = 3) -> str:
    """Agent with response validation"""
    for attempt in range(max_retries):
        response = agent_executor.invoke({"input": query})["output"]
        
        if validate_response(response, query):
            return response
        
        logger.warning(f"Response validation failed (attempt {attempt + 1})")
    
    return "Unable to generate satisfactory response. Please rephrase your question."
```

### 7.2 Debugging Checklist

When troubleshooting agent issues, check:

- [ ] **Prompt Template** - Is it clear and specific?
- [ ] **Tool Descriptions** - Are they detailed with examples?
- [ ] **Error Handling** - Are exceptions caught and logged?
- [ ] **Iteration Limits** - Is max_iterations set appropriately?
- [ ] **Timeout Settings** - Are timeouts configured?
- [ ] **Memory Management** - Is context window managed?
- [ ] **Model Selection** - Is the right model being used?
- [ ] **Temperature** - Is it appropriate for the task?
- [ ] **Logging** - Is verbose mode enabled?
- [ ] **Metrics** - Are performance metrics being collected?

### 7.3 Performance Optimization Checklist

To optimize agent performance:

- [ ] Use **NVIDIA NIM** for inference
- [ ] Enable **TensorRT-LLM** optimizations
- [ ] Implement **caching** for repeated queries
- [ ] Use **smaller models** for simple tasks
- [ ] **Parallelize** independent tool calls
- [ ] Set appropriate **max_tokens** limits
- [ ] Implement **streaming** for long responses
- [ ] Add **circuit breakers** for failing services
- [ ] Use **connection pooling** for APIs
- [ ] Monitor and optimize **token usage**


---

## 8. Best Practices and Anti-Patterns

### 8.1 Development Best Practices

✅ **DO:**

1. **Start with Simple Prompts, Iterate**
   ```python
   # Start simple
   prompt_v1 = "Answer the question: {query}"
   
   # Add structure
   prompt_v2 = "You are a helpful assistant. Answer: {query}"
   
   # Add constraints
   prompt_v3 = """You are a helpful assistant.
   Answer concisely in 2-3 sentences.
   Question: {query}"""
   ```

2. **Use Type Hints and Validation**
   ```python
   from typing import List, Dict, Optional
   from pydantic import BaseModel, Field
   
   class ToolInput(BaseModel):
       query: str = Field(min_length=1, max_length=500)
       filters: Optional[List[str]] = Field(default=None)
   
   def my_tool(input: ToolInput) -> str:
       # Type-safe implementation
       pass
   ```

3. **Implement Comprehensive Logging**
   ```python
   import logging
   
   logger = logging.getLogger(__name__)
   logger.setLevel(logging.INFO)
   
   def agent_invoke(query: str) -> str:
       logger.info(f"Processing query: {query}")
       try:
           result = agent_executor.invoke({"input": query})
           logger.info(f"Success: {len(result['output'])} chars")
           return result["output"]
       except Exception as e:
           logger.error(f"Failed: {str(e)}", exc_info=True)
           raise
   ```

4. **Test with Edge Cases**
   ```python
   test_cases = [
       "",  # Empty input
       "a" * 10000,  # Very long input
       "!@#$%^&*()",  # Special characters
       "SELECT * FROM users",  # SQL injection attempt
       "../../etc/passwd",  # Path traversal attempt
   ]
   
   for test in test_cases:
       try:
           response = agent.invoke(test)
           print(f"✓ Handled: {test[:50]}")
       except Exception as e:
           print(f"✗ Failed: {test[:50]} - {str(e)}")
   ```

5. **Monitor Production Metrics**
   ```python
   # Already covered in section 6.1
   monitored_agent = MonitoredAgent(agent_executor)
   ```

6. **Version Your Prompts**
   ```python
   PROMPT_VERSION = "2.1.0"
   
   PROMPT_TEMPLATE = f"""
   # Version: {PROMPT_VERSION}
   # Last Updated: 2024-01-15
   # Changes: Added error handling instructions
   
   You are a helpful assistant...
   """
   ```

7. **Use Environment Variables for Secrets**
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   # NEVER hardcode API keys
   # BAD: api_key = "nvapi-abc123..."
   
   # GOOD: Load from environment
   api_key = os.getenv("NVIDIA_API_KEY")
   if not api_key:
       raise ValueError("NVIDIA_API_KEY not set")
   ```

8. **Implement Rate Limiting**
   ```python
   from time import time, sleep
   
   class RateLimitedAgent:
       def __init__(self, agent, max_requests_per_minute=60):
           self.agent = agent
           self.max_requests = max_requests_per_minute
           self.requests = []
       
       def invoke(self, query: str) -> str:
           # Remove old requests
           now = time()
           self.requests = [t for t in self.requests if now - t < 60]
           
           # Check rate limit
           if len(self.requests) >= self.max_requests:
               sleep_time = 60 - (now - self.requests[0])
               logger.warning(f"Rate limit reached, sleeping {sleep_time:.1f}s")
               sleep(sleep_time)
           
           # Record request
           self.requests.append(now)
           
           return self.agent.invoke(query)
   ```

### 8.2 Anti-Patterns to Avoid

❌ **DON'T:**

1. **Don't Ignore Errors**
   ```python
   # BAD
   try:
       result = agent.invoke(query)
   except:
       pass  # Silent failure
   
   # GOOD
   try:
       result = agent.invoke(query)
   except Exception as e:
       logger.error(f"Agent failed: {str(e)}")
       return fallback_response()
   ```

2. **Don't Use Unbounded Loops**
   ```python
   # BAD
   while not done:
       action = agent.decide()
       execute(action)
   
   # GOOD
   max_iterations = 10
   for i in range(max_iterations):
       if done:
           break
       action = agent.decide()
       execute(action)
   ```

3. **Don't Hardcode Prompts**
   ```python
   # BAD
   response = llm.invoke("You are a helpful assistant. Answer: " + query)
   
   # GOOD
   from langchain.prompts import PromptTemplate
   
   template = PromptTemplate(
       input_variables=["query"],
       template="You are a helpful assistant. Answer: {query}"
   )
   response = llm.invoke(template.format(query=query))
   ```

4. **Don't Skip Input Validation**
   ```python
   # BAD
   def process(user_input: str):
       return agent.invoke(user_input)
   
   # GOOD
   def process(user_input: str):
       if not user_input or len(user_input) > 1000:
           raise ValueError("Invalid input length")
       
       # Sanitize input
       sanitized = user_input.strip()
       
       return agent.invoke(sanitized)
   ```

5. **Don't Neglect Token Limits**
   ```python
   # BAD
   conversation_history.append(message)  # Unbounded growth
   
   # GOOD
   from langchain.memory import ConversationBufferWindowMemory
   
   memory = ConversationBufferWindowMemory(k=10)  # Keep last 10 messages
   ```

6. **Don't Use Synchronous Calls for I/O**
   ```python
   # BAD: Blocks on each call
   results = []
   for item in items:
       result = api_call(item)
       results.append(result)
   
   # GOOD: Parallel execution
   from concurrent.futures import ThreadPoolExecutor
   
   with ThreadPoolExecutor() as executor:
       results = list(executor.map(api_call, items))
   ```

7. **Don't Expose Internal Errors to Users**
   ```python
   # BAD
   try:
       result = agent.invoke(query)
   except Exception as e:
       return f"Error: {str(e)}"  # Exposes stack traces
   
   # GOOD
   try:
       result = agent.invoke(query)
   except Exception as e:
       logger.error(f"Internal error: {str(e)}", exc_info=True)
       return "I encountered an issue. Please try again or contact support."
   ```

---

## 9. Exam Focus Areas

### 9.1 High-Priority Topics

Based on the 15% exam weight for this domain, focus on:

1. **Prompt Engineering** (Very Common)
   - Dynamic prompt chains
   - Few-shot learning
   - Chain-of-thought prompting
   - Conditional prompting

2. **Tool Integration** (Very Common)
   - Defining custom tools
   - API integration patterns
   - Multimodal tools
   - Tool error handling

3. **Error Handling** (Very Common)
   - Retry logic with exponential backoff
   - Circuit breaker pattern
   - Graceful degradation
   - Timeout management

4. **NVIDIA Platform** (Common)
   - NIM deployment and configuration
   - TensorRT-LLM optimization
   - Performance tuning
   - Streaming responses

5. **Evaluation** (Moderate)
   - Performance metrics
   - A/B testing
   - Iterative refinement

### 9.2 Sample Exam Scenarios

**Scenario 1: Error Handling**
> "An agent calls an external API that fails 10% of the time with 503 errors. The API usually recovers within 5 seconds. Users expect responses within 10 seconds. What error handling strategy should you implement?"

**Answer:** Retry logic with exponential backoff (1s, 2s, 4s delays) for up to 3 attempts. This handles transient 503 errors while staying within the 10-second timeout (1+2+4 = 7s max retry time + initial attempt).

**Scenario 2: Performance Optimization**
> "An agent using Llama-3.1-70B takes 5 seconds per response. 80% of queries are simple FAQs. How can you reduce average latency while maintaining quality for complex queries?"

**Answer:** Implement hybrid approach: route simple queries to Llama-3.1-8B (faster) and complex queries to Llama-3.1-70B. Use query complexity classifier or confidence threshold to route. Deploy both models via NVIDIA NIM for optimal performance.

**Scenario 3: Tool Integration**
> "You're building an agent that needs to query a database, call a weather API, and send emails. The database query takes 2s, weather API takes 1s, and email takes 0.5s. How can you minimize total execution time?"

**Answer:** Parallelize independent operations using ThreadPoolExecutor or async/await. If database and weather queries are independent, execute them concurrently (2s total instead of 3s sequential). Send email after gathering required data.

**Scenario 4: Prompt Engineering**
> "An agent needs to analyze customer feedback and categorize it as positive, negative, or neutral, then suggest appropriate responses. What prompting strategy is most effective?"

**Answer:** Use chain-of-thought prompting with few-shot examples. First step: analyze sentiment with reasoning. Second step: generate response based on sentiment. Provide 2-3 examples of each category to guide the model.

### 9.3 Key Formulas and Concepts

**Exponential Backoff Formula:**
```
delay = initial_delay * (backoff_factor ^ attempt_number)
Example: 1s * (2 ^ 0) = 1s, 1s * (2 ^ 1) = 2s, 1s * (2 ^ 2) = 4s
```

**Circuit Breaker States:**
- **CLOSED**: Normal operation, requests pass through
- **OPEN**: Failure threshold exceeded, requests rejected
- **HALF_OPEN**: Testing if service recovered

**Performance Metrics:**
- **Latency**: Time from request to response
- **Throughput**: Requests processed per second
- **Error Rate**: Failed requests / Total requests
- **Token Usage**: Input tokens + Output tokens per request

---

## 10. Summary and Key Takeaways

### Core Concepts to Remember

1. **Prompt Engineering:**
   - Use clear, structured prompts with examples
   - Implement dynamic chains for complex tasks
   - Apply chain-of-thought for multi-step reasoning
   - Adapt prompts based on context and user preferences

2. **Tool Integration:**
   - Define tools with clear descriptions and examples
   - Implement robust error handling in tools
   - Use Pydantic for input validation
   - Support multimodal capabilities when needed

3. **Error Handling:**
   - Retry with exponential backoff for transient failures
   - Circuit breaker for cascading failures
   - Graceful degradation for service unavailability
   - Always implement timeouts

4. **NVIDIA Platform:**
   - Use NIM for production-grade inference
   - TensorRT-LLM provides 2-8x speedup
   - Implement streaming for better UX
   - Monitor performance metrics

5. **Evaluation:**
   - Track success rate, latency, cost
   - Use A/B testing for improvements
   - Iterate based on metrics and feedback
   - Validate responses before returning

### Decision Framework

When developing agents, consider:

1. **Prompt Strategy:** Simple → Few-shot → Chain-of-thought
2. **Error Handling:** Retry → Circuit Breaker → Graceful Degradation
3. **Performance:** Caching → Smaller Models → Parallel Execution → NIM
4. **Quality:** Validation → Structured Outputs → Lower Temperature
5. **Monitoring:** Logging → Metrics → A/B Testing → Refinement

---

## 11. Practice Questions

### Question 1
An agent repeatedly calls the same search tool with identical queries. What's the most likely cause and solution?

**Answer:** The agent is stuck in a loop due to unclear tool descriptions or lack of state tracking. Solution: Improve tool descriptions with examples, add loop detection logic, or implement state tracking to prevent repeated actions.

### Question 2
Your agent needs to call 5 independent APIs, each taking 1 second. Sequential execution takes 5 seconds, but users expect <2 second responses. What should you do?

**Answer:** Parallelize API calls using ThreadPoolExecutor or async/await. All 5 calls can execute concurrently, reducing total time to ~1 second (plus overhead). Ensure APIs can handle concurrent requests.

### Question 3
An external API fails with 503 errors during peak hours. Your agent should handle this gracefully. What pattern should you implement?

**Answer:** Implement circuit breaker pattern. After N consecutive failures (e.g., 5), open the circuit and reject requests immediately for a timeout period (e.g., 60s). After timeout, enter half-open state to test if service recovered. This prevents cascading failures and reduces load on failing service.

---

## 12. Additional Resources

### Official NVIDIA Documentation
- [NVIDIA NIM Documentation](https://docs.nvidia.com/nim)
- [TensorRT-LLM Guide](https://docs.nvidia.com/tensorrt-llm)
- [NVIDIA AI Endpoints](https://docs.nvidia.com/ai-endpoints)

### Related Modules
- **Module 1:** Agent Architecture and Design (foundations)
- **Module 3:** Evaluation and Tuning (advanced evaluation)
- **Module 6:** NVIDIA Platform (deep dive on NVIDIA tools)
- **Module 7:** Monitoring and Maintenance (production operations)

### Recommended Reading
- LangChain Documentation on Agents
- "Prompt Engineering Guide" (DAIR.AI)
- "Building Production-Ready RAG Applications"
- Circuit Breaker Pattern (Martin Fowler)

---

## 13. Self-Assessment Checklist

Before moving to the next module, ensure you can:

- [ ] Write effective prompts with clear instructions and examples
- [ ] Implement dynamic prompt chains for multi-step tasks
- [ ] Define custom tools with proper error handling
- [ ] Integrate external APIs with retry logic
- [ ] Implement circuit breaker pattern for failing services
- [ ] Deploy agents using NVIDIA NIM
- [ ] Optimize inference with TensorRT-LLM
- [ ] Implement streaming responses
- [ ] Collect and analyze performance metrics
- [ ] Conduct A/B testing for agent improvements
- [ ] Debug common agent issues (loops, failures, latency)
- [ ] Apply best practices and avoid anti-patterns

**Next Steps:** Proceed to **Module 3: Evaluation and Tuning** to learn advanced evaluation methodologies and optimization techniques.

---

*This module covers 15% of the NCP-AAI exam content. Master these concepts through hands-on practice in the accompanying Jupyter notebooks.*


---

## Related Materials

### Hands-On Practice

**Interactive Notebooks:**
- [01-prompt-engineering.ipynb](../../notebooks/module-02/01-prompt-engineering.ipynb)
- [02-tool-integration.ipynb](../../notebooks/module-02/02-tool-integration.ipynb)
- [03-error-handling-patterns.ipynb](../../notebooks/module-02/03-error-handling-patterns.ipynb)
- [04-streaming-responses.ipynb](../../notebooks/module-02/04-streaming-responses.ipynb)

**Practice Labs:**
- [Lab: Lab 01 Basic Rag Agent](../../labs/lab-01-basic-rag-agent/README.md)
- [Lab: Lab 02 Multi Agent Research](../../labs/lab-02-multi-agent-research/README.md)

### Assessment

**Exam Questions:**
- [Domain 02 Development](../../exam-questions/domain-02-development.md)
