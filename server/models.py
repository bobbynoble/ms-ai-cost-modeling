from typing import Optional

from pydantic import BaseModel, Field


class LicenseLine(BaseModel):
    provider: str = Field(..., description="Key into LICENSE_CATALOG, e.g. 'microsoft'")
    tier: str = Field(..., description="Key into LICENSE_CATALOG[provider]")
    seats: int = Field(..., ge=0)
    annual_commitment: bool = Field(False, description="Upfront annual commitment discount")


class UsageLine(BaseModel):
    provider: str = Field(..., description="Key into MODEL_CATALOG, e.g. 'anthropic'")
    model: str = Field(..., description="Key into MODEL_CATALOG[provider]")
    monthly_input_tokens: int = Field(0, ge=0)
    monthly_output_tokens: int = Field(0, ge=0)
    use_reserved: bool = Field(False, description="Use reserved/provisioned throughput instead of pay-as-you-go")
    reserved_units: int = Field(0, ge=0, description="Reserved throughput units, if use_reserved is true")


class InfrastructureLine(BaseModel):
    provider: str = Field(..., description="Key into INFRASTRUCTURE_CATALOG, e.g. 'aws'")
    item: str = Field(..., description="Key into INFRASTRUCTURE_CATALOG[provider]")


class ImplementationInput(BaseModel):
    hours: float = Field(0, ge=0, description="One-time implementation/integration effort")
    hourly_rate: Optional[float] = Field(None, ge=0, description="Overrides default implementation hourly rate")


class SupportInput(BaseModel):
    monthly_hours: float = Field(0, ge=0, description="Ongoing monthly support/maintenance effort")
    hourly_rate: Optional[float] = Field(None, ge=0, description="Overrides default support hourly rate")


class DeploymentInput(BaseModel):
    licensing: list[LicenseLine] = Field(default_factory=list)
    ai_usage: list[UsageLine] = Field(default_factory=list)
    infrastructure: list[InfrastructureLine] = Field(default_factory=list)
    other_monthly_infra_cost: float = Field(0, ge=0)
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
