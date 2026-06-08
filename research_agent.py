import anthropic
from ddgs import DDGS
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

system_prompt = """You are a business research analyst. When given a company name, 
you research it thoroughly and produce a structured report covering:
- What the company does
- Business model and revenue streams
- Key metrics (revenue, employees, growth if available)
- Main competitors
- Recent news or developments
- Opportunities for AI automation in their business

Use web search to find current, accurate information. Search multiple times to get 
comprehensive data. Maximum 5 searches. Then produce a clean structured report."""

tools = [
    {
        "name": "web_search",
        "description": "Search the web for current information about a company",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    }
]

def search_web(query):
    results = DDGS().text(query, max_results=3)
    output = ""
    for r in results:
        output += f"Title: {r['title']}\nSummary: {r['body']}\n\n"
    return output

def research_company(company_name):
    messages = [
        {
            "role": "user",
            "content": f"Research this company and give me a full report: {company_name}"
        }
    ]
    
    search_count = 0
    max_searches = 5
    
    print(f"\nResearching {company_name}...\n")
    
    while True:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            system=system_prompt,
            tools=tools,
            tool_choice={"type": "auto"},
            messages=messages
        )
        
        if message.stop_reason == "tool_use" and search_count < max_searches:
            tool_use_block = next(b for b in message.content if b.type == "tool_use")
            query = tool_use_block.input["query"]
            search_count += 1
            print(f"[Search {search_count}/{max_searches}: {query}]")
            
            search_results = search_web(query)
            
            messages.append({
                "role": "assistant",
                "content": [
                    {
                        "type": "tool_use",
                        "id": tool_use_block.id,
                        "name": tool_use_block.name,
                        "input": tool_use_block.input
                    }
                ]
            })
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use_block.id,
                    "content": search_results
                }]
            })
            
        else:
            final_response = next(b.text for b in message.content if hasattr(b, "text"))
            return final_response

print("Company Research Agent")
print("=" * 40)

while True:
    company = input("\nEnter company name (or 'quit'): ")
    if company.lower() == "quit":
        break
    report = research_company(company)
    print("\n" + "=" * 40)
    print(report)
    print("=" * 40)