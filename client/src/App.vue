<script setup>
import { onMounted, ref } from "vue";
import InputForm from "./components/InputForm.vue";
import CostBreakdown from "./components/CostBreakdown.vue";
import { fetchPricingReference, calculateCost } from "./api.js";

const pricing = ref(null);
const breakdown = ref(null);
const error = ref(null);
const pricingError = ref(null);
const loading = ref(false);

onMounted(async () => {
  try {
    pricing.value = await fetchPricingReference();
  } catch (e) {
    pricingError.value = `Could not reach the backend API: ${e.message}`;
  }
});

async function handleCalculate(deployment) {
  error.value = null;
  loading.value = true;
  try {
    breakdown.value = await calculateCost(deployment);
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="app-shell">
    <header>
      <h1>Microsoft AI Deployment Cost Modeling</h1>
      <p class="subtitle">
        Estimate total cost of ownership for a Microsoft 365 Copilot / Azure OpenAI deployment —
        licensing, AI usage, infrastructure, and implementation effort.
      </p>
    </header>

    <main v-if="pricing">
      <section class="form-panel">
        <InputForm :pricing="pricing" @calculate="handleCalculate" />
      </section>

      <section class="results-panel">
        <p v-if="loading">Calculating…</p>
        <p v-if="error" class="error">{{ error }}</p>
        <CostBreakdown v-if="breakdown" :breakdown="breakdown" />
        <p v-else-if="!loading" class="hint">Fill in the deployment details and click "Calculate cost".</p>
      </section>
    </main>
    <p v-else-if="pricingError" class="error">
      {{ pricingError }} — is the backend running on http://localhost:8000?
    </p>
    <p v-else>Loading pricing reference…</p>

    <footer>
      Estimates are based on approximate list pricing and are for planning purposes only —
      not a quote. Confirm current pricing with Microsoft before committing budget.
    </footer>
  </div>
</template>

<style>
:root {
  color-scheme: light;
}

body {
  margin: 0;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  background: #f9f9f7;
  color: #0b0b0b;
}

@media (prefers-color-scheme: dark) {
  body {
    background: #0d0d0d;
    color: #ffffff;
  }
}

.app-shell {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

header h1 {
  font-size: 1.6rem;
  margin-bottom: 0.4rem;
}

.subtitle {
  color: #52514e;
  max-width: 65ch;
}

main {
  display: grid;
  grid-template-columns: minmax(280px, 380px) 1fr;
  gap: 2rem;
  align-items: start;
}

@media (max-width: 800px) {
  main {
    grid-template-columns: 1fr;
  }
}

.error {
  color: #d03b3b;
  font-weight: 600;
}

.hint {
  color: #898781;
}

footer {
  font-size: 0.8rem;
  color: #898781;
  border-top: 1px solid rgba(11, 11, 11, 0.1);
  padding-top: 1rem;
}
</style>
