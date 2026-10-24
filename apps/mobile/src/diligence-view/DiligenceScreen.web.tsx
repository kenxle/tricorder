import { createElement } from "react";
import { View } from "react-native";

export default function DiligenceScreen() {
  return (
    <View style={{ flex: 1 }}>
      {createElement("iframe", {
        src: "/prototype/index.html",
        title: "Tricorder diligence prototype",
        style: { border: 0, height: "100%", width: "100%" },
      })}
    </View>
  );
}
