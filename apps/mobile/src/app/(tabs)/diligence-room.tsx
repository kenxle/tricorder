// Temporary preview route for the room view. ?room=partial shows the partly-in state.
import type { Href } from "expo-router";
import { useLocalSearchParams, useRouter } from "expo-router";

import { RoomView } from "../../diligence/room-view";

const MEMO = "/diligence-memo" as Href;

const DiligenceRoomPreview = () => {
  const { room } = useLocalSearchParams<{ room?: string }>();
  const router = useRouter();
  return (
    <RoomView
      onMemo={() => router.push(MEMO)}
      onSteer={() => router.push(MEMO)}
      state={room === "partial" ? "partial" : "full"}
    />
  );
};

export default DiligenceRoomPreview;
