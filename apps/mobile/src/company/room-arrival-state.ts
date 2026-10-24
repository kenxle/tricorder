import type { CompanyRoomArrival } from "@tricorder/schema/company-room";
import { z } from "zod";

const sequenceSchema = z.union([z.literal(0), z.literal(1), z.literal(2)]);
const savedRoomStateSchema = z
  .strictObject({
    company: z.string().min(1),
    opened: sequenceSchema,
    received: sequenceSchema,
    roomId: z.string().min(1).nullable(),
    snapshotAt: z.string().min(1).nullable(),
    version: z.literal(1),
  })
  .refine((state) => state.opened <= state.received)
  .refine((state) =>
    state.received === 0
      ? state.roomId === null && state.snapshotAt === null
      : state.roomId !== null && state.snapshotAt !== null
  );

export type RoomArrivalState = z.infer<typeof savedRoomStateSchema>;
export type RoomStage = CompanyRoomArrival["stage"];

export const emptyRoomState = (company: string): RoomArrivalState => ({
  company,
  opened: 0,
  received: 0,
  roomId: null,
  snapshotAt: null,
  version: 1,
});

export const restoreRoomState = (company: string, serialized?: string) => {
  if (!serialized) {
    return emptyRoomState(company);
  }
  const state = savedRoomStateSchema.parse(JSON.parse(serialized));
  if (state.company !== company) {
    throw new Error("The saved arrival belongs to another company.");
  }
  return state;
};

export const stageForSequence = (sequence: 1 | 2): RoomStage =>
  sequence === 1 ? "partial" : "full";

export const validateRoomArrival = (
  state: RoomArrivalState,
  arrival: CompanyRoomArrival,
  expectedStage?: RoomStage
) => {
  if (
    arrival.version !== 1 ||
    arrival.provenance !== "saved-synthetic-replay" ||
    arrival.company?.slug !== state.company ||
    !arrival.roomId ||
    !arrival.arrivalId ||
    !arrival.snapshotAt ||
    !arrival.syntheticNotice ||
    ![1, 2].includes(arrival.sequence) ||
    arrival.stage !== stageForSequence(arrival.sequence) ||
    (expectedStage !== undefined && arrival.stage !== expectedStage) ||
    (state.roomId !== null && state.roomId !== arrival.roomId) ||
    (state.snapshotAt !== null && state.snapshotAt !== arrival.snapshotAt)
  ) {
    throw new Error(
      "The saved arrival does not match this company and room snapshot."
    );
  }
};

export const receiveRoomArrival = (
  state: RoomArrivalState,
  arrival: CompanyRoomArrival
): RoomArrivalState => {
  validateRoomArrival(state, arrival);
  if (arrival.sequence <= state.received) {
    return state;
  }
  return {
    ...state,
    received: arrival.sequence,
    roomId: arrival.roomId,
    snapshotAt: arrival.snapshotAt,
  };
};

export const openRoomArrival = (
  state: RoomArrivalState,
  arrival: CompanyRoomArrival
): RoomArrivalState => {
  validateRoomArrival(state, arrival);
  if (arrival.sequence > state.received) {
    throw new Error("Receive this arrival before opening it.");
  }
  return arrival.sequence <= state.opened
    ? state
    : { ...state, opened: arrival.sequence };
};
