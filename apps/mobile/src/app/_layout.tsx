import { useFonts } from "expo-font";
import { DarkTheme, DefaultTheme, ThemeProvider } from "expo-router";
import { ActivityIndicator, View, useColorScheme } from "react-native";
import { KeyboardProvider } from "react-native-keyboard-controller";

import Archivo from "../../assets/fonts/Archivo.ttf";
import ArchivoBold from "../../assets/fonts/ArchivoBold.ttf";
import ArchivoDisplay from "../../assets/fonts/ArchivoDisplay.ttf";
import PlexMono from "../../assets/fonts/PlexMono.ttf";
import AppTabs from "../components/app-tabs";
import { useReadoutColors } from "../readout/ui";

export default function RootLayout() {
  const scheme = useColorScheme();
  const colors = useReadoutColors();
  const [fontsLoaded, fontError] = useFonts({
    Archivo,
    ArchivoBold,
    ArchivoDisplay,
    PlexMono,
  });
  if (!fontsLoaded && !fontError) {
    return (
      <View
        style={{
          backgroundColor: colors.bg,
          flex: 1,
          justifyContent: "center",
        }}
      >
        <ActivityIndicator
          accessibilityLabel="Loading Tricorder"
          color={colors.accent}
        />
      </View>
    );
  }
  return (
    <ThemeProvider
      value={{
        ...(scheme === "dark" ? DarkTheme : DefaultTheme),
        colors: {
          ...(scheme === "dark" ? DarkTheme : DefaultTheme).colors,
          background: colors.bg,
          border: colors.line,
          card: colors.surface,
          primary: colors.accent,
          text: colors.fg,
        },
      }}
    >
      <KeyboardProvider>
        <AppTabs />
      </KeyboardProvider>
    </ThemeProvider>
  );
}
