from typing import Literal, Optional

from pydantic import BaseModel, Field

from pricing import AZURE_AI_SEARCH_TIERS, AZURE_OPENAI_MODELS, M365_COPILOT_LICENSE


LicenseTier = Literal[tuple(M365_COPILOT_LICENSE.keys())]
OpenAIModel = Literal[tuple(AZURE_OPENAI_MODELS.keys())]
SearchTier = Literal[tuple(AZURE_AI_SEARCH_TIERS.keys())]


class LicensingInput(BaseModel):
    seats: int = Field(..., ge=0, description="Number of licensed users")
    tier: LicenseTier = "m365_copilot"
    annual_commitment: bool = Field(False, description="Upfront annual commitment discount")


class AzureOpenAIInput(BaseModel):
    enabled: bool = True
    model: OpenAIModel = "gpt-4o"
    monthly_input_tokens: int = Field(0, ge=0, description="Total input tokens per month")
    monthly_output_tokens: int = Field(0, ge=0, description="Total output tokens per month")
    use_ptu: bool = Field(False, description="Use Provisioned Throughput Units instead of pay-as-you-go")
    ptu_units: int = Field(0, ge=0, description="Number of PTUs reserved, if use_ptu is true")


class InfrastructureInput(BaseModel):
    azure_ai_search_enabled: bool = False
    azure_ai_search_tier: SearchTier = "basic"
    other_monthly_infra_cost: float = Field(0, ge=0, description="Other monthly infra (storage, App Service, networking, etc.)")


class ImplementationInput(BaseModel):
    hours: float = Field(0, ge=0, description="One-time implementation/integration effort")
    hourly_rate: Optional[float] = Field(None, ge=0, description="Overrides default implementation hourly rate")


class SupportInput(BaseModel):
    monthly_hours: float = Field(0, ge=0, description="Ongoing monthly support/maintenance effort")
    hourly_rate: Optional[float] = Field(None, ge=0, description="Overrides default support hourly rate")


class DeploymentInput(BaseModel):
    licensing: LicensingInput
    azure_openai: AzureOpenAIInput
    infrastructure: InfrastructureInput
    implementation: ImplementationInput
    support: SupportInput


class CostLineItem(BaseModel):
    label: str
    monthly: float
    annual: float


class CostCategory(BaseModel):
    label: str
    monthly: float
    annual: float
    items: list[CostLineItem]


class CostBreakdown(BaseModel):
    licensing: CostCategory
    ai_usage: CostCategory
    infrastructure: CostCategory
    support: CostCategory
    one_time_implementation: float
    total_monthly_recurring: float
    total_annual_recurring: float
    total_first_year: float
