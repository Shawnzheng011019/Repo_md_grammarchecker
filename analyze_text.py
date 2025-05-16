import openai
from openai import OpenAI

def analyze_with_llm(text, md_path, api_key):
    """Analyze text with OpenAI and get suggestions"""
    try:
        client = OpenAI(api_key=api_key)
        
        prompt = f"""You are a professional technical documentation editor. Analyze the following text for grammar errors, Chinglish expressions, and awkward phrasing. Provide detailed feedback with line numbers if possible.

Example output format:
1. **Issue**: Missing article
   **Location**: Line 5
   **Original**: "She went to store."
   **Suggestion**: "She went to the store."

2. **Issue**: Chinglish expression
   **Location**: Line 12
   **Original**: "The data is very clear and can be understood easily."
   **Suggestion**: "The data is very clear and easy to understand."

Text to analyze:{text}
Provide structured feedback for all issues found. If no issues are found, return "No issues found" exactly."""
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a technical documentation editor specialized in English grammar and style. Analyze text and provide detailed, actionable feedback."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Text analysis error ({md_path}): {e}")
        return f"Error: {str(e)}"

def parse_analysis_results(analysis_text):
    """Parse LLM analysis results to extract identified issues"""
    if "No issues found" in analysis_text:
        return []
    
    issues = []
    lines = analysis_text.strip().split('\n')
    
    current_issue = None
    
    for line in lines:
        if line.startswith("1. **Issue**") or line.startswith("1.**Issue**"):
            if current_issue:
                issues.append(current_issue)
            current_issue = {"issue": line.split("**Issue**:")[-1].strip()}
        elif line.startswith("**Location**") and current_issue:
            current_issue["location"] = line.split("**Location**:")[-1].strip()
        elif line.startswith("**Original**") and current_issue:
            current_issue["original"] = line.split("**Original**:")[-1].strip()
        elif line.startswith("**Suggestion**") and current_issue:
            current_issue["suggestion"] = line.split("**Suggestion**:")[-1].strip()
        elif line.strip() == "" and current_issue:
            issues.append(current_issue)
            current_issue = None
    
    if current_issue:
        issues.append(current_issue)
    
    return issues    