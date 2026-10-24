// Words the page shows for schema values. BRAND.md owns the wording.
import type { Piece } from "@tricorder/schema";

export const PIECE_LABEL: Record<Piece["name"], string> = {
  burn_and_runway: "Burn and runway",
  comps: "Comps",
  customers: "Customers",
  market: "Market",
  retention: "Retention",
  team: "Team",
  the_pitch_itself: "The pitch itself",
  traction_and_revenue: "Traction and revenue",
  unit_economics: "Unit economics",
};

export const VERDICT_LABEL: Record<Piece["verdict"], string> = {
  looking_strong: "Looking strong",
  looking_weak: "Looking weak",
  mixed: "Mixed",
  not_enough_in_the_room: "Not enough in the room",
};
