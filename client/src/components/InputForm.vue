<script setup>
import { reactive } from "vue";

const props = defineProps({
  pricing: { type: Object, required: true },
});

const emit = defineEmits(["calculate"]);

const form = reactive({
  licensing: { seats: 500, tier: "m365_copilot", annual_commitment: false },
  azure_openai: {
    enabled: true,
    model: "gpt-4o",
    monthly_input_tokens: 20000000,
    monthly_output_tokens: 6000000,
    use_ptu: false,
    ptu_units: 0,
  },
  infrastructure: {
    azure_ai_search_enabled: false,
    azure_ai_search_tier: "basic",
    other_monthly_infra_cost: 0,
  },
  implementation: { hours: 160, hourly_rate: null },
  support: { monthly_hours: 20, hourly_rate: null },
});

function submit() {
  emit("calculate", JSON.parse(JSON.stringify(form)));
}
</script>

<template>
  <form class="input-form" @submit.prevent="submit">
    <fieldset>
      <legend>Licensing</legend>
      <label>
        Seats
        <input v-model.number="form.licensing.seats" type="number" min="0" />
      </label>
      <label>
        License tier
        <select v-model="form.licensing.tier">
          <option v-for="(v, k) in pricing.licensing" :key="k" :value="k">
            {{ v.label }} (${{ v.monthly_per_seat.toFixed(2) }}/seat/mo)
          </option>
        </select>
      </label>
      <label class="checkbox">
        <input v-model="form.licensing.annual_commitment" type="checkbox" />
        Annual commitment discount
      </label>
    </fieldset>

    <fieldset>
      <legend>Azure OpenAI usage</legend>
      <label class="checkbox">
        <input v-model="form.azure_openai.enabled" type="checkbox" />
        Include Azure OpenAI usage
      </label>
      <template v-if="form.azure_openai.enabled">
        <label class="checkbox">
          <input v-model="form.azure_openai.use_ptu" type="checkbox" />
          Use Provisioned Throughput (PTU) instead of pay-as-you-go
        </label>
        <template v-if="!form.azure_openai.use_ptu">
          <label>
            Model
            <select v-model="form.azure_openai.model">
              <option v-for="(v, k) in pricing.azure_openai_models" :key="k" :value="k">
                {{ v.label }}
              </option>
            </select>
          </label>
          <label>
            Monthly input tokens
            <input v-model.number="form.azure_openai.monthly_input_tokens" type="number" min="0" />
          </label>
          <label>
            Monthly output tokens
            <input v-model.number="form.azure_openai.monthly_output_tokens" type="number" min="0" />
          </label>
        </template>
        <template v-else>
          <label>
            PTU units
            <input v-model.number="form.azure_openai.ptu_units" type="number" min="0" />
          </label>
        </template>
      </template>
    </fieldset>

    <fieldset>
      <legend>Infrastructure</legend>
      <label class="checkbox">
        <input v-model="form.infrastructure.azure_ai_search_enabled" type="checkbox" />
        Include Azure AI Search
      </label>
      <label v-if="form.infrastructure.azure_ai_search_enabled">
        Search tier
        <select v-model="form.infrastructure.azure_ai_search_tier">
          <option v-for="(v, k) in pricing.azure_ai_search_tiers" :key="k" :value="k">
            {{ v.label }} (${{ v.monthly.toFixed(2) }}/mo)
          </option>
        </select>
      </label>
      <label>
        Other monthly infrastructure cost ($)
        <input v-model.number="form.infrastructure.other_monthly_infra_cost" type="number" min="0" />
      </label>
    </fieldset>

    <fieldset>
      <legend>Implementation (one-time)</legend>
      <label>
        Hours
        <input v-model.number="form.implementation.hours" type="number" min="0" />
      </label>
      <label>
        Hourly rate ($, default {{ pricing.default_implementation_hourly_rate }})
        <input v-model.number="form.implementation.hourly_rate" type="number" min="0" placeholder="default" />
      </label>
    </fieldset>

    <fieldset>
      <legend>Ongoing support</legend>
      <label>
        Monthly hours
        <input v-model.number="form.support.monthly_hours" type="number" min="0" />
      </label>
      <label>
        Hourly rate ($, default {{ pricing.default_support_hourly_rate }})
        <input v-model.number="form.support.hourly_rate" type="number" min="0" placeholder="default" />
      </label>
    </fieldset>

    <button type="submit">Calculate cost</button>
  </form>
</template>

<style scoped>
.input-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

fieldset {
  border: 1px solid var(--border-hairline, rgba(11, 11, 11, 0.1));
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

legend {
  font-weight: 600;
  padding: 0 0.4rem;
}

label {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.9rem;
}

label.checkbox {
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
}

input[type="number"],
select {
  padding: 0.4rem 0.5rem;
  border-radius: 6px;
  border: 1px solid var(--border-hairline, rgba(11, 11, 11, 0.2));
  font-size: 0.95rem;
}

button {
  align-self: flex-start;
  padding: 0.6rem 1.4rem;
  border-radius: 6px;
  border: none;
  background: #2a78d6;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

button:hover {
  background: #1c5cab;
}
</style>
