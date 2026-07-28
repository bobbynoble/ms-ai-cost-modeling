<script setup>
import { computed, ref } from "vue";

const props = defineProps({
  breakdown: { type: Object, required: true },
});

const categories = computed(() => [
  { key: "licensing", ...props.breakdown.licensing },
  { key: "ai_usage", ...props.breakdown.ai_usage },
  { key: "infrastructure", ...props.breakdown.infrastructure },
  { key: "support", ...props.breakdown.support },
]);

const totalMonthly = computed(() => props.breakdown.total_monthly_recurring || 1);

const segments = computed(() =>
  categories.value.map((c) => ({
    ...c,
    pct: (c.monthly / totalMonthly.value) * 100,
  }))
);

const hovered = ref(null);

function currency(n) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
}
</script>

<template>
  <div class="viz-root">
    <div class="stat-row">
      <div class="stat-tile">
        <div class="stat-label">Monthly recurring</div>
        <div class="stat-value">{{ currency(breakdown.total_monthly_recurring) }}</div>
      </div>
      <div class="stat-tile">
        <div class="stat-label">Annual recurring</div>
        <div class="stat-value">{{ currency(breakdown.total_annual_recurring) }}</div>
      </div>
      <div class="stat-tile">
        <div class="stat-label">One-time implementation</div>
        <div class="stat-value">{{ currency(breakdown.one_time_implementation) }}</div>
      </div>
      <div class="stat-tile stat-tile-primary">
        <div class="stat-label">Total first-year cost</div>
        <div class="stat-value">{{ currency(breakdown.total_first_year) }}</div>
      </div>
    </div>

    <div class="chart-card">
      <h3>Monthly recurring cost composition</h3>
      <div class="legend">
        <span v-for="c in categories" :key="c.key" class="legend-item">
          <span class="legend-swatch" :class="`swatch-${c.key}`"></span>
          {{ c.label }}
        </span>
      </div>
      <div class="stacked-bar" role="img" aria-label="Monthly recurring cost by category">
        <div
          v-for="c in segments"
          :key="c.key"
          class="bar-segment"
          :class="`segment-${c.key}`"
          :style="{ width: c.pct + '%' }"
          tabindex="0"
          @pointerenter="hovered = c.key"
          @pointerleave="hovered = null"
          @focus="hovered = c.key"
          @blur="hovered = null"
        >
          <div v-if="hovered === c.key" class="tooltip">
            <span class="tooltip-value">{{ currency(c.monthly) }}/mo</span>
            <span class="tooltip-label">{{ c.label }}</span>
          </div>
        </div>
      </div>
    </div>

    <table class="breakdown-table">
      <thead>
        <tr>
          <th>Category</th>
          <th>Item</th>
          <th>Monthly</th>
          <th>Annual</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="c in categories" :key="c.key">
          <tr v-for="(item, idx) in c.items" :key="item.label">
            <td v-if="idx === 0" :rowspan="c.items.length || 1">
              <span class="legend-swatch" :class="`swatch-${c.key}`"></span>
              {{ c.label }}
            </td>
            <td>{{ item.label }}</td>
            <td class="num">{{ currency(item.monthly) }}</td>
            <td class="num">{{ currency(item.annual) }}</td>
          </tr>
          <tr v-if="c.items.length === 0">
            <td>
              <span class="legend-swatch" :class="`swatch-${c.key}`"></span>
              {{ c.label }}
            </td>
            <td class="muted">Not included</td>
            <td class="num">{{ currency(0) }}</td>
            <td class="num">{{ currency(0) }}</td>
          </tr>
        </template>
        <tr class="row-implementation">
          <td colspan="2">Implementation (one-time)</td>
          <td class="num">—</td>
          <td class="num">{{ currency(breakdown.one_time_implementation) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.viz-root {
  color-scheme: light;
  --surface-1: #fcfcfb;
  --text-primary: #0b0b0b;
  --text-secondary: #52514e;
  --text-muted: #898781;
  --gridline: #e1e0d9;
  --border: rgba(11, 11, 11, 0.1);
  --series-1: #2a78d6;
  --series-2: #eb6834;
  --series-3: #1baf7a;
  --series-4: #eda100;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

@media (prefers-color-scheme: dark) {
  :root:where(:not([data-theme="light"])) .viz-root {
    color-scheme: dark;
    --surface-1: #1a1a19;
    --text-primary: #ffffff;
    --text-secondary: #c3c2b7;
    --text-muted: #898781;
    --gridline: #2c2c2a;
    --border: rgba(255, 255, 255, 0.1);
    --series-1: #3987e5;
    --series-2: #d95926;
    --series-3: #199e70;
    --series-4: #c98500;
  }
}
:root[data-theme="dark"] .viz-root {
  color-scheme: dark;
  --surface-1: #1a1a19;
  --text-primary: #ffffff;
  --text-secondary: #c3c2b7;
  --text-muted: #898781;
  --gridline: #2c2c2a;
  --border: rgba(255, 255, 255, 0.1);
  --series-1: #3987e5;
  --series-2: #d95926;
  --series-3: #199e70;
  --series-4: #c98500;
}

.stat-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1rem;
}

.stat-tile {
  background: var(--surface-1);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem;
}

.stat-tile-primary {
  border-color: var(--series-1);
}

.stat-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 0.35rem;
}

.stat-value {
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--text-primary);
}

.chart-card {
  background: var(--surface-1);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.25rem;
}

.chart-card h3 {
  margin: 0 0 0.75rem;
  font-size: 1rem;
  color: var(--text-primary);
}

.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 0.75rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.legend-swatch {
  width: 10px;
  height: 10px;
  border-radius: 2px;
  display: inline-block;
}

.swatch-licensing {
  background: var(--series-1);
}
.swatch-ai_usage {
  background: var(--series-2);
}
.swatch-infrastructure {
  background: var(--series-3);
}
.swatch-support {
  background: var(--series-4);
}

.stacked-bar {
  display: flex;
  height: 24px;
  border-radius: 4px;
  overflow: visible;
  background: var(--gridline);
}

.bar-segment {
  position: relative;
  height: 100%;
  outline: none;
  border-right: 2px solid var(--surface-1);
}

.bar-segment:last-child {
  border-right: none;
}

.bar-segment:first-child {
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;
}

.bar-segment:last-child {
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
}

.segment-licensing {
  background: var(--series-1);
}
.segment-ai_usage {
  background: var(--series-2);
}
.segment-infrastructure {
  background: var(--series-3);
}
.segment-support {
  background: var(--series-4);
}

.bar-segment:hover,
.bar-segment:focus {
  filter: brightness(1.08);
}

.tooltip {
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  background: var(--text-primary);
  color: var(--surface-1);
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
  font-size: 0.8rem;
  white-space: nowrap;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 10;
  pointer-events: none;
}

.tooltip-value {
  font-weight: 700;
}

.tooltip-label {
  color: var(--text-muted);
}

.breakdown-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
  color: var(--text-primary);
}

.breakdown-table th,
.breakdown-table td {
  text-align: left;
  padding: 0.5rem 0.6rem;
  border-bottom: 1px solid var(--gridline);
}

.breakdown-table th {
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.num {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

.muted {
  color: var(--text-muted);
}

.row-implementation td {
  font-weight: 600;
  border-top: 2px solid var(--gridline);
}
</style>
