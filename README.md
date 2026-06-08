# Company Research Agent

An AI agent that researches any company and produces a structured business report with AI automation opportunities.

## What it does

1. Takes a company name as input
2. Runs up to 5 targeted web searches
3. Synthesizes findings into a structured report covering:
   - Company overview and business model
   - Key metrics (revenue, employees, growth)
   - Main competitors
   - Recent news and developments
   - AI automation opportunities specific to that company

## Built with

- Python
- Anthropic Claude API (Haiku)
- DuckDuckGo Search API

## Use case

Built for consultants and sales teams who need deep company intelligence before client meetings or outreach. Replaces 30-60 minutes of manual research with a 30-second automated report.

## Setup

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Set your `ANTHROPIC_API_KEY` environment variable
4. Run: `python research_agent.py`

## Example output

Input: `Burger King Scandinavia`

Output: Full structured report including ownership structure, market position, competitor analysis, and 10 specific AI automation opportunities.