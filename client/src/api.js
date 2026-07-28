const BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

export async function fetchPricingReference() {
  const res = await fetch(`${BASE_URL}/api/pricing-reference`);
  if (!res.ok) throw new Error("Failed to load pricing reference");
  return res.json();
}

export async function calculateCost(deployment) {
  const res = await fetch(`${BASE_URL}/api/calculate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(deployment),
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => null);
    throw new Error(detail?.detail ? JSON.stringify(detail.detail) : "Calculation failed");
  }
  return res.json();
}
