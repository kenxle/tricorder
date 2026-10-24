// Report charts drawn with plain Views (the app has no chart library).
import { StyleSheet, View } from "react-native";

import { Body, Note, useReadoutColors } from "../readout/ui";
import type { CashChart, RevenueChart } from "./room-data";
import { usd } from "./room-data";

const BAR_HEIGHT = 160;

export function RevenueBars({ chart }: { chart: RevenueChart }) {
  const colors = useReadoutColors();
  const totals = chart.months.map(
    (_, i) => (chart.recurring[i] ?? 0) + (chart.one_time[i] ?? 0)
  );
  const max = Math.max(chart.deck_monthly, ...totals);
  const deckTop = BAR_HEIGHT - (chart.deck_monthly / max) * BAR_HEIGHT;
  return (
    <View accessibilityLabel="Monthly revenue by month" style={styles.wrap}>
      <View style={[styles.plot, { borderColor: colors.line }]}>
        <View
          style={[styles.deckLine, { borderColor: colors.red, top: deckTop }]}
        />
        {chart.months.map((m, i) => {
          const rec = chart.recurring[i] ?? 0;
          const one = chart.one_time[i] ?? 0;
          return (
            <View key={m} style={styles.col}>
              <View
                style={{
                  backgroundColor: colors.amber,
                  height: (one / max) * BAR_HEIGHT,
                  width: 36,
                }}
              />
              <View
                style={{
                  backgroundColor: colors.fg,
                  height: (rec / max) * BAR_HEIGHT,
                  width: 36,
                }}
              />
              <Note style={styles.axis}>{m}</Note>
              <Note style={styles.axis}>{usd(rec)}</Note>
            </View>
          );
        })}
      </View>
      <View style={styles.legend}>
        <Legend color={colors.fg} label={chart.recurring_label} />
        <Legend color={colors.amber} label={chart.one_time_label} />
        <Legend color={colors.red} label={chart.deck_label} />
      </View>
    </View>
  );
}

export function RunwayBars({ chart }: { chart: CashChart }) {
  const colors = useReadoutColors();
  const months = chart.series.map((s) => s.points.at(-1)?.[0] ?? 0);
  const max = Math.max(chart.baseline, ...months);
  return (
    <View accessibilityLabel="Months of runway by scenario" style={styles.wrap}>
      <Note>Months until the cash runs out, from {chart.as_of}</Note>
      {chart.series.map((s, i) => (
        <View key={s.name} style={styles.hrow}>
          <Body style={styles.hlabel}>{s.name}</Body>
          <View style={[styles.htrack, { borderColor: colors.line }]}>
            <View
              style={{
                backgroundColor: i === 0 ? colors.fg : colors.muted,
                height: 18,
                width: `${((months[i] ?? 0) / max) * 100}%`,
              }}
            />
            <View
              style={[
                styles.baseline,
                {
                  borderColor: colors.red,
                  left: `${(chart.baseline / max) * 100}%`,
                },
              ]}
            />
          </View>
          <Note>{s.end}</Note>
        </View>
      ))}
      <Legend color={colors.red} label={chart.baseline_label} />
    </View>
  );
}

function Legend({ color, label }: { color: string; label: string }) {
  return (
    <View style={styles.legendItem}>
      <View style={{ backgroundColor: color, height: 10, width: 10 }} />
      <Note style={styles.axis}>{label}</Note>
    </View>
  );
}

const styles = StyleSheet.create({
  axis: { fontSize: 12, lineHeight: 16 },
  baseline: { borderLeftWidth: 2, bottom: -4, position: "absolute", top: -4 },
  col: { alignItems: "center", flex: 1, justifyContent: "flex-end" },
  deckLine: { borderTopWidth: 2, left: 0, position: "absolute", right: 0 },
  hlabel: { fontSize: 14 },
  hrow: { gap: 4 },
  htrack: { borderBottomWidth: 1, position: "relative" },
  legend: { flexDirection: "row", flexWrap: "wrap", gap: 12 },
  legendItem: { alignItems: "center", flexDirection: "row", gap: 6 },
  plot: {
    borderBottomWidth: 1,
    flexDirection: "row",
    height: BAR_HEIGHT + 40,
    paddingTop: 8,
    position: "relative",
  },
  wrap: { gap: 10, marginVertical: 8 },
});
