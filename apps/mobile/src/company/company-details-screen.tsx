import {
  FieldGroup,
  Host,
  Picker,
  RNHostView,
  Text as NativeText,
} from "@expo/ui";
import { router, useLocalSearchParams } from "expo-router";
import { ScrollView, View } from "react-native";

import { AnnotationScope } from "../annotations/context";
import { Action, Field, Note, useReadoutColors } from "../readout/ui";
import {
  fieldLabels,
  setupFor,
  stages,
  useCompanyState,
} from "./company-state";
import { data } from "./data";
import { EvidenceContent } from "./evidence-content";
import { resolveCompany } from "./model";
import type { Company, SetupField } from "./model";

const fieldProvenance = (field: SetupField | undefined): string => {
  if (field?.edited) {
    return "Corrected by you";
  }
  if (field?.source) {
    return data.sources[field.source]?.title ?? "Source unavailable";
  }
  return "Not in the saved files";
};

const CompanyDetails = ({ company }: { company: Company }) => {
  const colors = useReadoutColors();
  const { fields, stage, setField, changeStage } = useCompanyState(company);
  return (
    <Host style={{ flex: 1 }} seedColor={colors.accent}>
      <FieldGroup>
        <FieldGroup.Section title="Saved company details">
          <FieldGroup.SectionFooter>
            <NativeText>
              Matched from the saved YC directory. Corrections apply to this
              readout and the request draft.
            </NativeText>
          </FieldGroup.SectionFooter>
          {Object.entries(fieldLabels).map(([key, label]) => (
            <RNHostView key={key} matchContents={{ vertical: true }}>
              <View style={{ gap: 8 }}>
                <Field
                  label={label}
                  value={fields[key]?.value ?? ""}
                  onChangeText={(value) => setField(key, value)}
                />
                <Note>{fieldProvenance(fields[key])}</Note>
                {fields[key]?.source && (
                  <Action
                    title={`Source for ${label.toLowerCase()}`}
                    onPress={() =>
                      router.push({
                        params: { company: company.website, field: key },
                        pathname: "/company-sheet/evidence",
                      })
                    }
                  />
                )}
              </View>
            </RNHostView>
          ))}
        </FieldGroup.Section>
        <FieldGroup.Section title="Stage">
          <Picker
            selectedValue={stage}
            onValueChange={changeStage}
            testID="Company stage"
          >
            {stages.map((entry) => (
              <Picker.Item
                key={entry.id}
                label={entry.title}
                value={entry.id}
              />
            ))}
          </Picker>
          <FieldGroup.SectionFooter>
            <NativeText>
              {fields.stage.edited
                ? "Corrected by you"
                : (fields.stage.note ?? "From the saved research")}
            </NativeText>
          </FieldGroup.SectionFooter>
        </FieldGroup.Section>
      </FieldGroup>
    </Host>
  );
};

export const CompanyDetailsScreen = () => {
  const params = useLocalSearchParams<{ company?: string | string[] }>();
  const url = Array.isArray(params.company)
    ? params.company[0]
    : params.company;
  const company = url ? resolveCompany(url, data.companies) : null;
  return company ? (
    <CompanyDetails company={company} />
  ) : (
    <Note>Company unavailable. Close this sheet and open a saved readout.</Note>
  );
};

export const CompanyFieldEvidenceScreen = () => {
  const params = useLocalSearchParams<{
    company?: string | string[];
    field?: string | string[];
  }>();
  const url = Array.isArray(params.company)
    ? params.company[0]
    : params.company;
  const field = Array.isArray(params.field) ? params.field[0] : params.field;
  const company = url ? resolveCompany(url, data.companies) : null;
  const saved = company && field ? setupFor(company)[field] : undefined;
  const label = Object.entries(fieldLabels).find(([key]) => key === field)?.[1];
  const colors = useReadoutColors();
  return (
    <ScrollView
      style={{ backgroundColor: colors.bg }}
      contentContainerStyle={{ gap: 16, padding: 24 }}
    >
      {saved && label && company ? (
        <AnnotationScope
          id={`company:${company.slug}/details:${field}`}
          label={`${company.name} · ${label}`}
        >
          <EvidenceContent
            claim={{
              source: saved.source,
              text: `${label} in the saved record: ${saved.value}`,
            }}
          />
        </AnnotationScope>
      ) : (
        <Note>Source unavailable in this saved record.</Note>
      )}
    </ScrollView>
  );
};
