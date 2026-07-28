from pricing import (
    ANNUAL_COMMITMENT_DISCOUNT,
    AZURE_AI_SEARCH_TIERS,
    AZURE_OPENAI_MODELS,
    AZURE_OPENAI_PTU_HOURLY_RATE,
    DEFAULT_IMPLEMENTATION_HOURLY_RATE,
    DEFAULT_SUPPORT_HOURLY_RATE,
    M365_COPILOT_LICENSE,
)
from models import CostBreakdown, CostCategory, CostLineItem, DeploymentInput

HOURS_PER_MONTH = 730  # average hours in a month, used for PTU monthly cost


def calculate_cost_breakdown(deployment: DeploymentInput) -> CostBreakdown:
    licensing = _calculate_licensing(deployment)
    ai_usage = _calculate_ai_usage(deployment)
    infrastructure = _calculate_infrastructure(deployment)
    support = _calculate_support(deployment)
    one_time_implementation = _calculate_implementation(deployment)

    total_monthly_recurring = (
        licensing.monthly + ai_usage.monthly + infrastructure.monthly + support.monthly
    )
    total_annual_recurring = (
        licensing.annual + ai_usage.annual + infrastructure.annual + support.annual
    )
    total_first_year = total_annual_recurring + one_time_implementation

    return CostBreakdown(
        licensing=licensing,
        ai_usage=ai_usage,
        infrastructure=infrastructure,
        support=support,
        one_time_implementation=round(one_time_implementation, 2),
        total_monthly_recurring=round(total_monthly_recurring, 2),
        total_annual_recurring=round(total_annual_recurring, 2),
        total_first_year=round(total_first_year, 2),
    )


def _calculate_licensing(deployment: DeploymentInput) -> CostCategory:
    lic = deployment.licensing
    tier = M365_COPILOT_LICENSE[lic.tier]
    monthly_per_seat = tier["monthly_per_seat"]
    if lic.annual_commitment:
        monthly_per_seat *= 1 - ANNUAL_COMMITMENT_DISCOUNT

    monthly = lic.seats * monthly_per_seat
    items = [
        CostLineItem(
            label=f"{tier['label']} ({lic.seats} seats)",
            monthly=round(monthly, 2),
            annual=round(monthly * 12, 2),
        )
    ]
    return CostCategory(
        label="Licensing", monthly=round(monthly, 2), annual=round(monthly * 12, 2), items=items
    )


def _calculate_ai_usage(deployment: DeploymentInput) -> CostCategory:
    ai = deployment.azure_openai
    items: list[CostLineItem] = []
    monthly = 0.0

    if ai.enabled:
        if ai.use_ptu:
            ptu_monthly = ai.ptu_units * AZURE_OPENAI_PTU_HOURLY_RATE * HOURS_PER_MONTH
            monthly += ptu_monthly
            items.append(
                CostLineItem(
                    label=f"Azure OpenAI PTU ({ai.ptu_units} units)",
                    monthly=round(ptu_monthly, 2),
                    annual=round(ptu_monthly * 12, 2),
                )
            )
        else:
            model = AZURE_OPENAI_MODELS[ai.model]
            input_cost = (ai.monthly_input_tokens / 1000) * model["input_per_1k"]
            output_cost = (ai.monthly_output_tokens / 1000) * model["output_per_1k"]
            token_monthly = input_cost + output_cost
            monthly += token_monthly
            items.append(
                CostLineItem(
                    label=f"Azure OpenAI {model['label']} (pay-as-you-go)",
                    monthly=round(token_monthly, 2),
                    annual=round(token_monthly * 12, 2),
                )
            )

    return CostCategory(
        label="AI Usage", monthly=round(monthly, 2), annual=round(monthly * 12, 2), items=items
    )


def _calculate_infrastructure(deployment: DeploymentInput) -> CostCategory:
    infra = deployment.infrastructure
    items: list[CostLineItem] = []
    monthly = 0.0

    if infra.azure_ai_search_enabled:
        tier = AZURE_AI_SEARCH_TIERS[infra.azure_ai_search_tier]
        monthly += tier["monthly"]
        items.append(
            CostLineItem(
                label=f"Azure AI Search ({tier['label']})",
                monthly=round(tier["monthly"], 2),
                annual=round(tier["monthly"] * 12, 2),
            )
        )

    if infra.other_monthly_infra_cost:
        monthly += infra.other_monthly_infra_cost
        items.append(
            CostLineItem(
                label="Other infrastructure",
                monthly=round(infra.other_monthly_infra_cost, 2),
                annual=round(infra.other_monthly_infra_cost * 12, 2),
            )
        )

    return CostCategory(
        label="Infrastructure",
        monthly=round(monthly, 2),
        annual=round(monthly * 12, 2),
        items=items,
    )


def _calculate_support(deployment: DeploymentInput) -> CostCategory:
    support = deployment.support
    rate = support.hourly_rate if support.hourly_rate is not None else DEFAULT_SUPPORT_HOURLY_RATE
    monthly = support.monthly_hours * rate
    items = []
    if monthly:
        items.append(
            CostLineItem(
                label=f"Ongoing support ({support.monthly_hours} hrs/mo @ ${rate:.2f}/hr)",
                monthly=round(monthly, 2),
                annual=round(monthly * 12, 2),
            )
        )
    return CostCategory(
        label="Support", monthly=round(monthly, 2), annual=round(monthly * 12, 2), items=items
    )


def _calculate_implementation(deployment: DeploymentInput) -> float:
    impl = deployment.implementation
    rate = impl.hourly_rate if impl.hourly_rate is not None else DEFAULT_IMPLEMENTATION_HOURLY_RATE
    return impl.hours * rate
