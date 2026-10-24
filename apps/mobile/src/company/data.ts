import snapshot from "../../../../docs/features/20261024.02_first_steps_ui/prototype/data.json";
import type { ChecklistItem, Company, Research } from "./model";

interface Source {
  title: string;
  path: string;
  url: string | null;
}
interface Snapshot {
  built: string;
  companies: Company[];
  research: Record<string, Research>;
  checklist: ChecklistItem[];
  sources: Record<string, Source>;
  list_source: string;
  yc_founders: Record<string, { name: string; source: string }[]>;
}
export const data: Snapshot = snapshot;
