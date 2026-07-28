AI processing will only run for emails that pass duplicate checks and placement-email filters.

## Change in AI Strategy (Gemini → Ollama)

- Original plan: use Gemini API for email summarization and extraction.
- Updated plan: use Ollama to run a local model (Gemma 3 or Phi-3 Mini) for AI tasks.
- Reason:
  - No external API keys.
  - No recurring costs.
  - Data stays on my local machine.
- Impact on roadmap:
  - AI steps now call `ai_service.py` → Ollama instead of Gemini.
  - The prompt aims to return structured JSON with fields:
    `category`, `company`, `role`, `deadline`, `eligibility`, `registration_link`, `summary`.