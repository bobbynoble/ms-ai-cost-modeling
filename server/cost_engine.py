from pricing import (
    ANNUAL_COMMITMENT_DISCOUNT,
    DEFAULT_IMPLEMENTATION_HOURLY_RATE,
    DEFAULT_SUPPORT_HOURLY_RATE,
    HOURS_PER_MONTH,
    INFRASTRUCTURE_CATALOG,
    LICENSE_CATALOG,
    MODEL_CATALOG,
    PROVIDERS,
    RESERVED_THROUGHPUT_HOURLY_RATE,
)
from models import CostBreakdown, CostCategory, CostLineItem, DeploymentInput


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
    items: list[CostLineItem] = []
    monthly = 0.0

    for line in deployment.licensing:
        tier = LICENSE_CATALOG[line.provider][line.tier]
        rate = tier["monthly_per_seat"]
        if line.annual_commitment:
            rate *= 1 - ANNUAL_COMMITMENT_DISCOUNT
        line_monthly = line.seats * rate
        monthly += line_monthly
        items.append(
            CostLineItem(
                label=f"{PROVIDERS[line.provider]} — {tier['label']} ({line.seats} seats)",
                monthly=round(line_monthly, 2),
                annual=round(line_monthly * 12, 2),
            )
        )

    return CostCategory(
        label="Licensing", monthly=round(monthly, 2), annual=round(monthly * 12, 2), items=items
    )


def _calculate_ai_usage(deployment: DeploymentInput) -> CostCategory:
    items: list[CostLineItem] = []
    monthly = 0.0

    for line in deployment.ai_usage:
        if line.use_reserved:
            hourly_rate = RESERVED_THROUGHPUT_HOURLY_RATE[line.provider]
            line_monthly = line.reserved_units * hourly_rate * HOURS_PER_MONTH
            label = f"{PROVIDERS[line.provider]} — reserved throughput ({line.reserved_units} units)"
        else:
            model = MODEL_CATALOG[line.provider][line.model]
            input_cost = (line.monthly_input_tokens / 1000) * model["input_per_1k"]
            output_cost = (line.monthly_output_tokens / 1000) * model["output_per_1k"]
            line_monthly = input_cost + output_cost
            label = f"{PROVIDERS[line.provider]} — {model['label']} (pay-as-you-go)"

        monthly += line_monthly
        items.append(
            CostLineItem(label=label, monthly=round(line_monthly, 2), annual=round(line_monthly * 12, 2))
        )

    return CostCategory(
        label="AI Usage", monthly=round(monthly, 2), annual=round(monthly * 12, 2), items=items
    )


def _calculate_infrastructure(deployment: DeploymentInput) -> CostCategory:
    items: list[CostLineItem] = []
    monthly = 0.0

    for line in deployment.infrastructure:
        entry = INFRASTRUCTURE_CATALOG[line.provider][line.item]
        monthly += entry["monthly"]
        items.append(
            CostLineItem(
                label=f"{PROVIDERS[line.provider]} — {entry['label']}",
                monthly=round(entry["monthly"], 2),
                annual=round(entry["monthly"] * 12, 2),
            )
        )

    if deployment.other_monthly_infra_cost:
        monthly += deployment.other_monthly_infra_cost
        items.append(
            CostLineItem(
                label="Other infrastructure",
                monthly=round(deployment.other_monthly_infra_cost, 2),
                annual=round(deployment.other_monthly_infra_cost * 12, 2),
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
