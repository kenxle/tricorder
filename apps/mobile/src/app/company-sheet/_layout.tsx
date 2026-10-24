import { Stack, router, useLocalSearchParams } from "expo-router";

import { Action, useReadoutColors } from "../../readout/ui";

export const unstable_settings = { anchor: "index" };

const DoneButton = () => {
  const params = useLocalSearchParams<{ company?: string | string[] }>();
  const company = Array.isArray(params.company)
    ? params.company[0]
    : params.company;
  const close = () => {
    router.dismissTo({ params: company ? { company } : {}, pathname: "/" });
  };
  return <Action compact title="Done" onPress={close} />;
};

const CompanySheetLayout = () => {
  const colors = useReadoutColors();
  return (
    <Stack
      screenOptions={{
        contentStyle: { backgroundColor: colors.bg },
        headerRight: DoneButton,
        headerStyle: { backgroundColor: colors.surface },
        headerTintColor: colors.accent,
      }}
    >
      <Stack.Screen name="index" options={{ title: "Company details" }} />
      <Stack.Screen name="evidence" options={{ title: "Evidence" }} />
    </Stack>
  );
};

export default CompanySheetLayout;
