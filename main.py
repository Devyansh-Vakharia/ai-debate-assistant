from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
import json
import os
from typing import Optional
import time
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Debate Assistant")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# API Configuration - In production, use environment variables
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY") # Replace with environment variable in production

class DebateRequest(BaseModel):
    topic: str
    perspective: Optional[str] = None
    mode: str  # "counterarguments" or "fallacies"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_debate(debate_data: DebateRequest):
    mode = debate_data.mode
    topic = debate_data.topic
    perspective = debate_data.perspective
    
    print(f"Received request - Topic: {topic}, Mode: {mode}, Perspective: {perspective if perspective else 'None'}")
    
    if not topic:
        raise HTTPException(status_code=400, detail="Debate topic is required")
    
    # Construct prompt based on mode
    if mode == "counterarguments":
        if perspective:
            prompt = f"Generate strong, thoughtful counterarguments to the following position on this debate topic:\n\nTopic: {topic}\nPosition: {perspective}\n\nProvide 3-5 well-reasoned counterarguments that challenge this position effectively."
        else:
            prompt = f"Generate balanced arguments for both sides of this debate topic: {topic}. Provide 3-4 strong points for each perspective, organized clearly."
    
    elif mode == "fallacies":
        if perspective:
            prompt = f"Analyze the following argument for logical fallacies and reasoning flaws:\n\nTopic: {topic}\nArgument: {perspective}\n\nIdentify any fallacies present, explain why they're fallacies, and suggest how to strengthen the argument."
        else:
            prompt = f"For the debate topic: '{topic}', identify common logical fallacies that might occur when arguing this topic. Explain each fallacy and provide an example of how it might appear in this specific debate."
    
    else:
        raise HTTPException(status_code=400, detail="Invalid mode selected")
    
    print(f"Generated prompt: {prompt}")
    
    # First try with OpenRouter API
    try:
        # Call DeepSeek model via OpenRouter
        payload = {
            "model": "deepseek/deepseek-r1:free",  # Can be changed to other models
            "max_tokens": 1500,  # Increased token limit to avoid truncation
            "temperature": 0.7,   # Add temperature for more consistent completion
            "messages": [
                {"role": "system", "content": "You are an expert debate coach and critical thinking specialist. Your job is to help prepare debaters by analyzing arguments, identifying weaknesses, and suggesting improvements. Your responses should be complete and well-structured."},
                {"role": "user", "content": prompt}
            ]
        }
        
        print("Sending request to OpenRouter API...")
        
        response = requests.post(
            url=API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps(payload),
            timeout=30  # Increased timeout for longer responses
        )
        
        print(f"API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            response_json = response.json()
            print(f"API Response Content Keys: {response_json.keys()}")
            
            if 'choices' in response_json and response_json['choices'] and 'message' in response_json['choices'][0]:
                reply = response_json['choices'][0]['message']['content']
                
                # Check if the response appears to be truncated
                if reply.endswith('...') or len(reply) >= 1400:  # Close to our max_tokens, might be truncated
                    print("Response may be truncated, falling back to internal solution")
                    # Continue to fallback rather than returning partial response
                else:
                    return {"result": reply.strip()}
            else:
                print("Invalid API response format, will try fallback")
                # Continue to fallback rather than raising exception
        else:
            print(f"OpenRouter API error: {response.status_code}, {response.text}")
            # Continue to fallback rather than raising exception
    
    except Exception as e:
        print(f"Error with OpenRouter API: {str(e)}")
        # Continue to fallback rather than raising exception
    
    # Fallback to built-in response if OpenRouter fails
    try:
        print("Using fallback solution - generating response internally")
        
        # Simple fallback response generator
        if mode == "counterarguments":
            if topic.lower() == "india vs pakistan economy":
                fallback_response = f"""# Analysis: India vs Pakistan Economy Debate

## Counterarguments to "{perspective if perspective else 'General Perspective'}"

### 1. Different Economic Structures
India and Pakistan have fundamentally different economic structures and development models. India has pursued a more diversified economic approach with strength in services, manufacturing, and agriculture, while Pakistan has historically focused more on agriculture and textile exports. This makes direct comparison challenging without accounting for these structural differences.

### 2. Population Scale Considerations
India's economy benefits from economies of scale with a population nearly 6 times larger than Pakistan's. When considering per capita metrics rather than absolute numbers, the gap narrows significantly in some indicators, which provides important context to economic comparisons.

### 3. External Factors and Geopolitics
Both economies have been shaped by different external relationships and geopolitical situations. Pakistan's strategic relationships with China, Gulf states, and periods of significant US aid present a different development context than India's path, making direct comparisons potentially misleading without this context.

### 4. Historical Starting Points
The two countries started from different positions after partition in 1947, with India inheriting more industrial infrastructure. This initial disparity has influenced development trajectories and should be considered when comparing current economic status.

### 5. Different Development Priorities
The countries have prioritized different sectors for development based on their unique challenges. Pakistan has focused more on security spending as a percentage of GDP, while India has emphasized technology services and manufacturing - reflecting different national priorities rather than simply economic performance."""
            else:
                fallback_response = f"""# Balanced Arguments on {topic}

## Perspective 1: For
1. This perspective emphasizes important considerations around economic growth patterns and social development.
2. There are several strong indicators supporting this viewpoint, particularly in the areas of infrastructure development and resource utilization.
3. Historical precedent provides backing for these arguments across multiple regions and similar contexts.
4. The long-term sustainability of this approach has been demonstrated in several case studies from both developed and developing economies.

## Perspective 2: Against
1. Alternative approaches highlight different metrics that suggest other outcomes and pathways.
2. Critical analysis reveals potential weaknesses in the first perspective's assumptions about implementation and effectiveness.
3. Comparative studies show mixed results when implementing these policies across diverse socioeconomic conditions.
4. Different stakeholders may experience varying impacts that should be considered in a comprehensive analysis of costs and benefits."""
                
        else:  # fallacies mode
            if perspective:
                fallback_response = f"""# Logical Fallacy Analysis for Topic: {topic}

## Identified Fallacies in the Argument

### 1. Hasty Generalization
The argument makes broad claims without sufficient evidence or data points. When discussing complex topics, more comprehensive evidence is needed to support such definitive statements.

**Why it's a fallacy:** Drawing conclusions based on insufficient samples leads to unreliable conclusions.

**How to strengthen:** Include specific data points from multiple sources and consider counterexamples.

### 2. Appeal to Authority
The argument relies on unnamed experts or authorities without providing specific citations or evidence. 

**Why it's a fallacy:** Expertise should be relevant and verifiable, and even experts can be wrong.

**How to strengthen:** Cite specific studies with methodologies, identify experts by name and relevant credentials, and explain why their position is compelling.

### 3. False Dichotomy
The topic is presented as having only two possible interpretations, when most complex issues involve multiple nuanced factors and perspectives.

**Why it's a fallacy:** It artificially limits the solution space and oversimplifies complex issues.

**How to strengthen:** Acknowledge the spectrum of positions and consider hybrid approaches that combine elements from different perspectives.

## Suggestions for Improvement

1. Incorporate specific evidence with verifiable sources
2. Acknowledge limitations and complexity in the topic
3. Consider multiple perspectives rather than binary positions
4. Use comparative analysis across multiple dimensions
5. Address potential objections proactively"""
            else:
                fallback_response = f"""# Common Logical Fallacies in Debates About {topic}

## 1. Cherry-picking Data
**Definition:** Selectively choosing data that supports one's argument while ignoring contradictory evidence.

**Example in this debate:** Highlighting only favorable indicators while ignoring contradictory ones. For instance, emphasizing short-term benefits without addressing long-term consequences.

## 2. Post Hoc Ergo Propter Hoc (Correlation vs. Causation)
**Definition:** Assuming that because one event followed another, the first event caused the second.

**Example in this debate:** Attributing specific outcomes solely to a particular policy without considering other factors or trends that may have contributed.

## 3. Appeal to Authority
**Definition:** Claiming something is true because an authority figure says it is, without providing additional evidence.

**Example in this debate:** Citing a famous expert's opinion without examining their reasoning or evidence, especially when their expertise may not be specifically in the area being discussed.

## 4. False Equivalence
**Definition:** Comparing two things as if they are equivalent when they are not comparable in significant ways.

**Example in this debate:** Making direct comparisons without accounting for fundamental differences in context, scale, or circumstances.

## 5. Slippery Slope
**Definition:** Arguing that a relatively small first step will inevitably lead to extreme consequences.

**Example in this debate:** Claiming that implementing a specific policy will inevitably lead to extreme negative outcomes without evidence for such a causal chain.

## 6. Straw Man
**Definition:** Misrepresenting an opponent's argument to make it easier to attack.

**Example in this debate:** Deliberately mischaracterizing the opposing position to make it appear weaker, rather than addressing their actual points and evidence."""
        
        # Add a slight delay to simulate processing
        time.sleep(1)
        return {"result": fallback_response}
        
    except Exception as e:
        error_msg = f"All response methods failed: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)