<script setup>
import { reactive } from "vue";

const props = defineProps({
  pricing: { type: Object, required: true },
});

const emit = defineEmits(["calculate"]);

const licensingProviders = Object.keys(props.pricing.licensing);
const modelProviders = Object.keys(props.pricing.models);
const infraProviders = Object.keys(props.pricing.infrastructure);

function firstTier(provider) {
  return Object.keys(props.pricing.licensing[provider])[0];
}
function firstModel(provider) {
  return Object.keys(props.pricing.models[provider])[0];
}
function firstInfraItem(provider) {
  return Object.keys(props.pricing.infrastructure[provider])[0];
}
function supportsReserved(provider) {
  return provider in props.pricing.reserved_throughput_hourly_rate;
}

function newLicenseLine() {
  const provider = licensingProviders[0];
  return { provider, tier: firstTier(provider), seats: 100, annual_commitment: false };
}
function newUsageLine() {
  const provider = modelProviders[0];
  return {
    provider,
    model: firstModel(provider),
    monthly_input_tokens: 5000000,
    monthly_output_tokens: 1500000,
    use_reserved: false,
    reserved_units: 0,
  };
}
function newInfraLine() {
  const provider = infraProviders[0];
  return { provider, item: firstInfraItem(provider) };
}

const form = reactive({
  licensing: [newLicenseLine()],
  ai_usage: [newUsageLine()],
  infrastructure: [],
  other_monthly_infra_cost: 0,
  implementation: { hours: 160, hourly_rate: null },
  support: { monthly_hours: 20, hourly_rate: null },
});

function onLicenseProviderChange(line) {
  line.tier = firstTier(line.provider);
}
function onUsageProviderChange(line) {
  line.model = firstModel(line.provider);
  line.use_reserved = false;
  line.reserved_units = 0;
}
function onInfraProviderChange(line) {
  line.item = firstInfraItem(line.provider);
}

function submit() {
  emit("calculate", JSON.parse(JSON.stringify(form)));
}
</script>

<template>
  <form class="input-form" @submit.prevent="submit">
    <fieldset>
      <legend>Licensing (per-seat)</legend>
      <div v-for="(line, i) in form.licensing" :key="i" class="line-item">
        <label>
          Provider
          <select v-model="line.provider" @change="onLicenseProviderChange(line)">
            <option v-for="p in licensingProviders" :key="p" :value="p">{{ pricing.providers[p] }}</option>
          </select>
        </label>
        <label>
          Tier
          <select v-model="line.tier">
            <option v-for="(v, k) in pricing.licensing[line.provider]" :key="k" :value="k">
              {{ v.label }} (${{ v.monthly_per_seat.toFixed(2) }}/seat/mo)
            </option>
          </select>
        </label>
        <label>
          Seats
          <input v-model.number="line.seats" type="number" min="0" />
        </label>
        <label class="checkbox">
          <input v-model="line.annual_commitment" type="checkbox" />
          Annual commitment discount
        </label>
        <button type="button" class="remove" @click="form.licensing.splice(i, 1)">Remove</button>
      </div>
      <button type="button" class="add" @click="form.licensing.push(newLicenseLine())">+ Add licensing line</button>
    </fieldset>

    <fieldset>
      <legend>AI usage</legend>
      <div v-for="(line, i) in form.ai_usage" :key="i" class="line-item">
        <label>
          Provider
          <select v-model="line.provider" @change="onUsageProviderChange(line)">
            <option v-for="p in modelProviders" :key="p" :value="p">{{ pricing.providers[p] }}</option>
          </select>
        </label>
        <label v-if="supportsReserved(line.provider)" class="checkbox">
          <input v-model="line.use_reserved" type="checkbox" />
          Use reserved/provisioned throughput
        </label>
        <template v-if="!line.use_reserved">
          <label>
            Model
            <select v-model="line.model">
              <option v-for="(v, k) in pricing.models[line.provider]" :key="k" :value="k">{{ v.label }}</option>
            </select>
          </label>
          <label>
            Monthly input tokens
            <input v-model.number="line.monthly_input_tokens" type="number" min="0" />
          </label>
          <label>
            Monthly output tokens
            <input v-model.number="line.monthly_output_tokens" type="number" min="0" />
          </label>
        </template>
        <label v-else>
          Reserved units
          <input v-model.number="line.reserved_units" type="number" min="0" />
        </label>
        <button type="button" class="remove" @click="form.ai_usage.splice(i, 1)">Remove</button>
      </div>
      <button type="button" class="add" @click="form.ai_usage.push(newUsageLine())">+ Add usage line</button>
    </fieldset>

    <fieldset>
      <legend>Infrastructure</legend>
      <div v-for="(line, i) in form.infrastructure" :key="i" class="line-item">
        <label>
          Provider
          <select v-model="line.provider" @change="onInfraProviderChange(line)">
            <option v-for="p in infraProviders" :key="p" :value="p">{{ pricing.providers[p] }}</option>
          </select>
        </label>
        <label>
          Item
          <select v-model="line.item">
            <option v-for="(v, k) in pricing.infrastructure[line.provider]" :key="k" :value="k">
              {{ v.label }} (${{ v.monthly.toFixed(2) }}/mo)
            </option>
          </select>
        </label>
        <button type="button" class="remove" @click="form.infrastructure.splice(i, 1)">Remove</button>
      </div>
      <button type="button" class="add" @click="form.infrastructure.push(newInfraLine())">+ Add infrastructure line</button>
      <label>
        Other monthly infrastructure cost ($)
        <input v-model.number="form.other_monthly_infra_cost" type="number" min="0" />
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

    <button type="submit" class="submit">Calculate cost</button>
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
  gap: 0.75rem;
}

legend {
  font-weight: 600;
  padding: 0 0.4rem;
}

.line-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.75rem;
  border: 1px solid var(--border-hairline, rgba(11, 11, 11, 0.08));
  border-radius: 6px;
  background: rgba(42, 120, 214, 0.03);
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

button.add,
button.remove {
  align-self: flex-start;
  padding: 0.35rem 0.8rem;
  border-radius: 6px;
  border: 1px solid rgba(11, 11, 11, 0.2);
  background: transparent;
  cursor: pointer;
  font-size: 0.85rem;
}

button.remove {
  color: #d03b3b;
  border-color: #d03b3b;
}

button.submit {
  align-self: flex-start;
  padding: 0.6rem 1.4rem;
  border-radius: 6px;
  border: none;
  background: #2a78d6;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

button.submit:hover {
  background: #1c5cab;
}
</style>
