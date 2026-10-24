# blind-room

A room Tricorder has never seen, and a room with nothing planted.

- **Status today:** partly built. Left: the outside person picks flags and seals the variant room's key.
- **Who builds it:** agent and an outside person.
- **Waits on:** data-room. Ken finds the person outside the build.
- **Horizon:** Now to Friday night
- **Checked against:** data_room/hollis_voice_clean and answer_key_clean.json exist, variant key not sealed by an outside person.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

A room Tricorder has never seen, and a room with nothing planted. The team wrote the room, planted the flags, wrote the answer key and then wrote one check per flag, so a perfect score on that room proves nothing to a partner ([critique_judge.md](../../features/20261022.01_hackathon_plan/critique_judge.md), finding 1). A clean room that comes back clean is the strongest ten seconds against "rigged" ([critique_demo.md](../../features/20261022.01_hackathon_plan/critique_demo.md), finding 7).

**Waits on:** data-room. Ken finds the person outside the build.

**Includes:**

- A plants-off switch in `data_room/generate.py`. The data room research describes one, and the generator has none (demo critique, finding 7). With plants off, it writes the clean room: the same company with no planted flags.
- A second seed. Run with it, the generator moves the values and writes the variant room.
- Someone outside the build picks which flags the variant room carries: a teammate who is not writing the engine, or a friend. The judge's version drops or adds one flag. An agent that has not seen the check list runs the generator for them.
- The variant room's answer key is sealed. The person who picked the flags keeps it and sends it to the captain at the 3:30 PM freeze. Nobody building the engine opens it before then.
- Both rooms sit beside the others in `data_room/`, with no answer key inside either room folder.
- The variant room now in `data_room/` is a smoke test with seed 77. It was run while the generator was built, and its flags are known, so it cannot be the sealed room ([data_room/README.md](../../../data_room/README.md)). The outside person writes a new one with their own seed and `--key-out` to a private path.

**Status:** the plants-off switch, the clean room (`hollis_voice_clean/`, with `answer_key_clean.json`) and the `--seed` and `--plants` options are built. The outside person and the sealed variant are not.

**Done when:**

- With plants off, the reference checks find nothing.
- The variant room exists, its key is with the outside person, and nobody on the build has opened it.
- On Saturday, the readout runs on the variant room and the clean room, and the real numbers are read out in one line ([demo-freeze](demo-freeze.md)).

**Who:** agent for the switch and the second seed. The person outside the build picks the flags and seals the key.

**Judgment:** yes.
