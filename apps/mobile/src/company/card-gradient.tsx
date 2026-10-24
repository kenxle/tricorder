import { Image } from "expo-image";
import { StyleSheet } from "react-native";

// Expo UI's Compose/universal layer does not yet expose gradient fills.
// The installed image renderer paints the same static gradient on Android.
export const CardGradient = ({ colors }: { colors: string[] }) => {
  const stops = colors
    .map(
      (color, index) =>
        `<stop offset="${index / (colors.length - 1)}" stop-color="${color}"/>`
    )
    .join("");
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">${stops}</linearGradient></defs><path fill="url(#g)" d="M0 0h100v100H0z"/></svg>`;
  return (
    <Image
      accessible={false}
      pointerEvents="none"
      source={{ uri: `data:image/svg+xml,${encodeURIComponent(svg)}` }}
      contentFit="fill"
      style={StyleSheet.absoluteFill}
    />
  );
};
