// Words the page shows for schema values. BRAND.md owns the wording.
import type { Piece } from "../../schema/ts/claim";

export const PIECE_LABEL: Record<Piece["name"], string> = {
  traction_and_revenue: "Traction and revenue",
  retention: "Retention",
  burn_and_runway: "Burn and runway",
  unit_economics: "Unit economics",
  customers: "Customers",
  market: "Market",
  comps: "Comps",
  team: "Team",
  the_pitch_itself: "The pitch itself",
};

export const VERDICT_LABEL: Record<Piece["verdict"], string> = {
  looking_strong: "Looking strong",
  looking_weak: "Looking weak",
  mixed: "Mixed",
  not_enough_in_the_room: "Not enough in the room",
};
