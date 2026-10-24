import { createContext, useContext, useMemo, useState } from "react";
import type { PropsWithChildren } from "react";

import { savedRequestStage } from "../request-ui/session";
import { data } from "./data";
import type { Company, SetupField, Stage } from "./model";

export const stages: {
  id: Stage;
  title: string;
}[] = [
  { id: "pre_seed", title: "Pre-seed" },
  { id: "seed", title: "Seed" },
  { id: "series_a", title: "Series A" },
];
export const fieldLabels = {
  batch: "Batch",
  founders: "Founders",
  location: "Location",
  name: "Name",
  team_size: "Team size",
  website: "Website",
};
export const setupFor = (company: Company): Record<string, SetupField> => {
  const saved = data.research[company.slug]?.setup;
  if (saved) {
    return Object.fromEntries(
      Object.entries(saved).map(([key, value]) => [key, { ...value }])
    );
  }
  const founders = data.yc_founders[company.slug];
  return {
    batch: { source: data.list_source, value: company.batch },
    founders: {
      source: founders?.[0]?.source,
      value: founders?.map((founder) => founder.name).join(", ") ?? "",
    },
    location: { source: data.list_source, value: company.regions[0] ?? "" },
    name: { source: data.list_source, value: company.name },
    stage: {
      note: "Set by the associate; not confirmed by research",
      value: "seed",
    },
    team_size: { source: data.list_source, value: String(company.team_size) },
    website: { source: data.list_source, value: company.website },
  };
};

interface CompanyState {
  fields: Record<string, SetupField>;
  stage: Stage;
}
const initialCompanyState = (company: Company): CompanyState => {
  const fields = setupFor(company);
  const saved = savedRequestStage(company.slug) ?? fields.stage.value;
  return {
    fields,
    stage: saved === "pre_seed" || saved === "series_a" ? saved : "seed",
  };
};
const CompanyStateContext = createContext<{
  records: Record<string, CompanyState>;
  update: (
    company: Company,
    change: (current: CompanyState) => CompanyState
  ) => void;
} | null>(null);

export const CompanyStateProvider = ({ children }: PropsWithChildren) => {
  const [records, setRecords] = useState<Record<string, CompanyState>>({});
  const value = useMemo(
    () => ({
      records,
      update: (
        company: Company,
        change: (current: CompanyState) => CompanyState
      ) => {
        setRecords((current) => ({
          ...current,
          [company.slug]: change(
            current[company.slug] ?? initialCompanyState(company)
          ),
        }));
      },
    }),
    [records]
  );
  return (
    <CompanyStateContext.Provider value={value}>
      {children}
    </CompanyStateContext.Provider>
  );
};

export const useCompanyState = (company: Company) => {
  const context = useContext(CompanyStateContext);
  if (!context) {
    throw new Error("Company screens require CompanyStateProvider.");
  }
  const initial = useMemo(() => initialCompanyState(company), [company]);
  const state = context.records[company.slug] ?? initial;
  return {
    ...state,
    changeStage: (stage: Stage) =>
      context.update(company, (current) => ({
        ...current,
        fields: {
          ...current.fields,
          stage: { ...current.fields.stage, edited: true, value: stage },
        },
        stage,
      })),
    setField: (key: string, value: string) =>
      context.update(company, (current) => ({
        ...current,
        fields: {
          ...current.fields,
          [key]: { ...current.fields[key], edited: true, value },
        },
      })),
  };
};
