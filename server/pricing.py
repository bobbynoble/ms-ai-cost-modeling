"""
Pricing assumptions for the Microsoft AI deployment TCO model.

All figures are list-price USD approximations as of mid-2026 and are meant as
a planning estimate, not a quote. Update these constants as Microsoft's
published pricing changes.
"""

# Microsoft 365 Copilot licensing (per user / month, USD)
M365_COPILOT_LICENSE = {
    "m365_copilot": {"label": "Microsoft 365 Copilot", "monthly_per_seat": 30.00},
    "copilot_studio": {"label": "Copilot Studio (message pack add-on)", "monthly_per_seat": 20.00},
}

# Annual (upfront) commitment discount applied to the monthly license rate
ANNUAL_COMMITMENT_DISCOUNT = 0.10

# Azure OpenAI pay-as-you-go pricing (USD per 1,000 tokens)
AZURE_OPENAI_MODELS = {
    "gpt-4o": {"label": "GPT-4o", "input_per_1k": 0.0025, "output_per_1k": 0.010},
    "gpt-4o-mini": {"label": "GPT-4o mini", "input_per_1k": 0.00015, "output_per_1k": 0.0006},
    "gpt-4-turbo": {"label": "GPT-4 Turbo", "input_per_1k": 0.010, "output_per_1k": 0.030},
    "o1": {"label": "o1", "input_per_1k": 0.015, "output_per_1k": 0.060},
}

# Provisioned Throughput Units (PTU) - hourly cost per PTU (monthly reserved rate, USD)
AZURE_OPENAI_PTU_HOURLY_RATE = 1.00

# Azure AI Search tiers (monthly USD)
AZURE_AI_SEARCH_TIERS = {
    "basic": {"label": "Basic", "monthly": 75.00},
    "standard_s1": {"label": "Standard S1", "monthly": 250.00},
    "standard_s2": {"label": "Standard S2", "monthly": 1000.00},
    "standard_s3": {"label": "Standard S3", "monthly": 2000.00},
}

# Default hourly rate assumptions for implementation and ongoing support (USD)
DEFAULT_IMPLEMENTATION_HOURLY_RATE = 175.00
DEFAULT_SUPPORT_HOURLY_RATE = 150.00
