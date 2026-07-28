"""
Pricing assumptions for the multi-provider AI deployment TCO model.

All figures are approximate list-price USD estimates as of mid-2026 and are
meant for planning purposes, not a quote. Update these constants as vendors'
published pricing changes.
"""

PROVIDERS = {
    "microsoft": "Microsoft",
    "anthropic": "Anthropic (Claude)",
    "aws": "AWS",
}

# Per-seat / per-user monthly licensing, grouped by provider
LICENSE_CATALOG = {
    "microsoft": {
        "m365_copilot": {"label": "Microsoft 365 Copilot", "monthly_per_seat": 30.00},
        "copilot_studio": {"label": "Copilot Studio (message pack add-on)", "monthly_per_seat": 20.00},
    },
    "anthropic": {
        "claude_team": {"label": "Claude for Work (Team)", "monthly_per_seat": 25.00},
        "claude_enterprise": {"label": "Claude Enterprise", "monthly_per_seat": 60.00},
    },
    "aws": {
        "q_business_lite": {"label": "Amazon Q Business Lite", "monthly_per_seat": 3.00},
        "q_business_pro": {"label": "Amazon Q Business Pro", "monthly_per_seat": 20.00},
    },
}

# Annual (upfront) commitment discount applied to the monthly license rate
ANNUAL_COMMITMENT_DISCOUNT = 0.10

# Model usage pricing, grouped by provider (USD per 1,000 tokens)
MODEL_CATALOG = {
    "microsoft": {
        "gpt-4o": {"label": "Azure OpenAI GPT-4o", "input_per_1k": 0.0025, "output_per_1k": 0.010},
        "gpt-4o-mini": {"label": "Azure OpenAI GPT-4o mini", "input_per_1k": 0.00015, "output_per_1k": 0.0006},
        "gpt-4-turbo": {"label": "Azure OpenAI GPT-4 Turbo", "input_per_1k": 0.010, "output_per_1k": 0.030},
        "o1": {"label": "Azure OpenAI o1", "input_per_1k": 0.015, "output_per_1k": 0.060},
    },
    "anthropic": {
        "claude-opus": {"label": "Claude Opus (API)", "input_per_1k": 0.015, "output_per_1k": 0.075},
        "claude-sonnet": {"label": "Claude Sonnet (API)", "input_per_1k": 0.003, "output_per_1k": 0.015},
        "claude-haiku": {"label": "Claude Haiku (API)", "input_per_1k": 0.0008, "output_per_1k": 0.004},
    },
    "aws": {
        "bedrock-claude-sonnet": {"label": "Claude Sonnet (Amazon Bedrock)", "input_per_1k": 0.003, "output_per_1k": 0.015},
        "bedrock-titan-text-premier": {"label": "Amazon Titan Text Premier (Bedrock)", "input_per_1k": 0.0005, "output_per_1k": 0.0015},
        "bedrock-llama3-70b": {"label": "Llama 3 70B (Bedrock)", "input_per_1k": 0.00265, "output_per_1k": 0.0035},
    },
}

# Provisioned/reserved throughput - hourly cost per unit (USD), where a provider offers it
RESERVED_THROUGHPUT_HOURLY_RATE = {
    "microsoft": 1.00,  # Azure OpenAI PTU
}

# Supporting infrastructure (e.g. vector search / retrieval), grouped by provider (monthly USD)
INFRASTRUCTURE_CATALOG = {
    "microsoft": {
        "azure_ai_search_basic": {"label": "Azure AI Search (Basic)", "monthly": 75.00},
        "azure_ai_search_s1": {"label": "Azure AI Search (Standard S1)", "monthly": 250.00},
        "azure_ai_search_s2": {"label": "Azure AI Search (Standard S2)", "monthly": 1000.00},
        "azure_ai_search_s3": {"label": "Azure AI Search (Standard S3)", "monthly": 2000.00},
    },
    "aws": {
        "opensearch_serverless": {"label": "Amazon OpenSearch Serverless (baseline OCUs)", "monthly": 700.00},
        "kendra_developer": {"label": "Amazon Kendra (Developer Edition)", "monthly": 810.00},
        "kendra_enterprise": {"label": "Amazon Kendra (Enterprise Edition)", "monthly": 1400.00},
    },
}

HOURS_PER_MONTH = 730  # average hours in a month, used for reserved-throughput monthly cost

# Default hourly rate assumptions for implementation and ongoing support (USD)
DEFAULT_IMPLEMENTATION_HOURLY_RATE = 175.00
DEFAULT_SUPPORT_HOURLY_RATE = 150.00
