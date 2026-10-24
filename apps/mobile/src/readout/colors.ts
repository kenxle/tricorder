import { useColorScheme } from "react-native";

export const useReadoutColors = () =>
  useColorScheme() === "dark"
    ? {
        accent: "#d3bf8e",
        amber: "#d3bf8e",
        bg: "#131210",
        buttonBg: "#d3bf8e",
        buttonFg: "#16140f",
        fg: "#eeebe4",
        green: "#7dc4a0",
        line: "#45413a",
        muted: "#bdb7ab",
        red: "#f08c78",
        surface: "#1a1916",
      }
    : {
        accent: "#85692f",
        amber: "#85692f",
        bg: "#ffffff",
        buttonBg: "#1c1b18",
        buttonFg: "#eadbb4",
        fg: "#1c1b18",
        green: "#1e7550",
        line: "#cdc7ba",
        muted: "#47443d",
        red: "#b3402e",
        surface: "#ffffff",
      };
