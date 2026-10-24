import { DarkTheme, DefaultTheme, ThemeProvider } from "expo-router";
import { useColorScheme } from "react-native";
import { KeyboardProvider } from "react-native-keyboard-controller";

import AppTabs from "../components/app-tabs";

export default function RootLayout() {
  const scheme = useColorScheme();
  return (
    <ThemeProvider value={scheme === "dark" ? DarkTheme : DefaultTheme}>
      <KeyboardProvider>
        <AppTabs />
      </KeyboardProvider>
    </ThemeProvider>
  );
}
