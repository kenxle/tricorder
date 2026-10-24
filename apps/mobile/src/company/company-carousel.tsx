// Adapted from Reacticx's VerticalPageCarousel:
// https://github.com/rit3zh/reacticx/blob/main/src/components/molecules/vertical-page-carousel/index.tsx
// MIT License — Copyright (c) 2026 rit3zh
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

import { impactAsync, ImpactFeedbackStyle } from "expo-haptics";
import { useCallback, useState } from "react";
import {
  Pressable,
  StyleSheet,
  Text,
  View,
  useColorScheme,
  useWindowDimensions,
} from "react-native";
import Animated, {
  Extrapolation,
  interpolate,
  useAnimatedScrollHandler,
  useAnimatedStyle,
  useReducedMotion,
  useSharedValue,
} from "react-native-reanimated";
import type { SharedValue } from "react-native-reanimated";

import { useReadoutColors } from "../readout/ui";
import { CardGradient } from "./card-gradient";
import { data } from "./data";
import type { Company } from "./model";

// Only these companies have the saved readouts offered by the entry screen.
const companies = ["ploy", "sazabi"].flatMap((slug) =>
  data.companies.filter((company) => company.slug === slug)
);
const CARD_SPACING = 20;

const styles = StyleSheet.create({
  card: { borderRadius: 32, borderWidth: 1, width: "100%" },
  cardClip: { borderRadius: 31, flex: 1, overflow: "hidden" },
  cardContent: { gap: 32, padding: 28 },
  content: { flexGrow: 1 },
  cta: { fontFamily: "Archivo", fontSize: 18, fontWeight: "600" },
  description: { fontFamily: "Archivo", fontSize: 22, lineHeight: 31 },
  detail: { fontFamily: "PlexMono", fontSize: 12, lineHeight: 19 },
  item: {
    alignSelf: "center",
    justifyContent: "center",
    maxWidth: 720,
    paddingHorizontal: 24,
    width: "100%",
  },
  name: { fontFamily: "ArchivoDisplay", fontSize: 46, letterSpacing: -1.5 },
  pressable: { flex: 1, justifyContent: "center" },
  screen: { flex: 1 },
  summary: { gap: 16 },
});

const CompanyPage = ({
  company,
  index,
  itemHeight,
  scrollY,
  onSelect,
  onMeasure,
}: {
  company: Company;
  index: number;
  itemHeight: number;
  scrollY: SharedValue<number>;
  onSelect: (url: string) => void;
  onMeasure: (slug: string, height: number) => void;
}) => {
  const colors = useReadoutColors();
  const dark = useColorScheme() === "dark";
  const gradient = dark
    ? ["#343027", "#1a1916", "#24211b"]
    : ["#f7f2e6", "#e5d7bc", "#fbfaf7"];
  const sazabiGradient = dark
    ? ["#2b3436", "#171b1d", "#262b2a"]
    : ["#f4f1e9", "#dce4e4", "#f8f8f4"];
  const reducedMotion = useReducedMotion();
  const animatedStyle = useAnimatedStyle(() => ({
    opacity: reducedMotion
      ? 1
      : interpolate(
          scrollY.get(),
          [index - 1, index, index + 1],
          [0.5, 1, 0.5],
          Extrapolation.CLAMP
        ),
    transform: [
      {
        scale: reducedMotion
          ? 1
          : interpolate(
              scrollY.get(),
              [index - 1, index, index + 1],
              [0.9, 1, 0.9],
              Extrapolation.CLAMP
            ),
      },
    ],
  }));

  return (
    <View style={[styles.item, { height: itemHeight + CARD_SPACING }]}>
      <Animated.View
        style={[
          styles.card,
          {
            backgroundColor: colors.surface,
            borderColor: colors.line,
            boxShadow: [
              {
                blurRadius: 24,
                color: dark ? "rgba(0, 0, 0, 0.28)" : "rgba(52, 41, 28, 0.14)",
                offsetX: 0,
                offsetY: 10,
                spreadDistance: -6,
              },
              {
                blurRadius: 6,
                color: dark ? "rgba(0, 0, 0, 0.18)" : "rgba(52, 41, 28, 0.06)",
                offsetX: 0,
                offsetY: 2,
                spreadDistance: -2,
              },
            ],
            height: itemHeight,
          },
          animatedStyle,
        ]}
      >
        <View style={styles.cardClip}>
          <CardGradient
            colors={company.slug === "sazabi" ? sazabiGradient : gradient}
          />
          <Pressable
            accessibilityRole="button"
            accessibilityLabel={`Open ${company.name} saved readout`}
            accessibilityHint={`${index + 1} of ${companies.length}. ${company.one_liner}`}
            testID={`company-card-${company.slug}`}
            onPress={() => onSelect(company.website)}
            style={({ pressed }) => [
              styles.pressable,
              { opacity: pressed ? 0.7 : 1 },
            ]}
          >
            <View
              style={styles.cardContent}
              onLayout={(event) =>
                onMeasure(company.slug, event.nativeEvent.layout.height)
              }
            >
              <Text
                style={[styles.detail, { color: colors.muted }]}
              >{`SAVED READOUT / ${String(index + 1).padStart(2, "0")} · ${companies.length}`}</Text>
              <View style={styles.summary}>
                <Text style={[styles.name, { color: colors.fg }]}>
                  {company.name}
                </Text>
                <Text style={[styles.description, { color: colors.fg }]}>
                  {company.one_liner}
                </Text>
                <Text style={[styles.detail, { color: colors.muted }]}>
                  {company.host} · YC {company.batch}
                </Text>
              </View>
              <View style={styles.summary}>
                <Text style={[styles.detail, { color: colors.muted }]}>
                  Saved public research · {data.built.slice(0, 10)}
                </Text>
                <Text style={[styles.cta, { color: colors.accent }]}>
                  Open readout →
                </Text>
              </View>
            </View>
          </Pressable>
        </View>
      </Animated.View>
    </View>
  );
};

export const CompanyCarousel = ({
  onSelect,
}: {
  onSelect: (url: string) => void;
}) => {
  const { fontScale } = useWindowDimensions();
  const [viewportHeight, setViewportHeight] = useState(0);
  const [contentHeights, setContentHeights] = useState<Record<string, number>>(
    {}
  );
  const measureContent = useCallback((slug: string, height: number) => {
    setContentHeights((current) =>
      current[slug] === height ? current : { ...current, [slug]: height }
    );
  }, []);
  const scrollY = useSharedValue(0);
  const reducedMotion = useReducedMotion();
  const itemHeight = Math.max(
    360 * fontScale,
    viewportHeight * 0.7,
    ...Object.values(contentHeights)
  );
  const interval = itemHeight + CARD_SPACING;
  const edgePadding = Math.max(0, (viewportHeight - interval) / 2);
  const onScroll = useAnimatedScrollHandler((event) => {
    scrollY.set(event.contentOffset.y / interval);
  });

  return (
    <View
      style={styles.screen}
      onLayout={(event) => setViewportHeight(event.nativeEvent.layout.height)}
    >
      <Animated.FlatList
        data={companies}
        keyExtractor={(company) => company.slug}
        automaticallyAdjustContentInsets={false}
        contentInsetAdjustmentBehavior="never"
        contentContainerStyle={[
          styles.content,
          { paddingVertical: edgePadding },
        ]}
        onScroll={onScroll}
        scrollEventThrottle={16}
        // Oversized Dynamic Type cards stay freely scrollable so every line is reachable.
        snapToOffsets={
          itemHeight <= viewportHeight
            ? companies.map((_, index) => index * interval)
            : undefined
        }
        decelerationRate="fast"
        onScrollEndDrag={() => {
          if (!reducedMotion && scrollY.get() >= 0) {
            void impactAsync(ImpactFeedbackStyle.Medium).catch(() => null);
          }
        }}
        renderItem={({ item, index }) => (
          <CompanyPage
            company={item}
            index={index}
            itemHeight={itemHeight}
            scrollY={scrollY}
            onSelect={onSelect}
            onMeasure={measureContent}
          />
        )}
      />
    </View>
  );
};
