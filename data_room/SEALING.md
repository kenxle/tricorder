# Sealing a variant room

This is for a person outside the Tricorder build. You make a second data room that the build team has never seen, and you keep its answer key to yourself until the demo. On stage, Tricorder runs on your room. Then you open the key and show what was planted.

The build team can read `generate.py`, so they know how every flag works. They must not learn which flags you chose or which seed you used. Do not tell them.

Every name, number and company in the room is fictional.

## 1. Pick the flags and the seed

Choose which of the eight flags to plant. Plant at least four and leave at least one out. A flag you leave out gives a room that is honest on that point, which tests whether Tricorder stays quiet.

| Id | What it plants |
|---|---|
| PF1 | The pilot is counted as ARR in the model |
| PF2 | The deck's ARR is higher than the model's ARR |
| PF2b | The pitch video's spoken ARR is higher than the deck's |
| PF3 | The cohort tab leaves out early leavers, so retention looks better |
| PF4 | The model pays for 8 hires, the hiring plan has 24, so burn and runway look better |
| PF5 | The deck says no customer is above 9% of ARR, but one is much larger |
| PF6 | Gross margin leaves out hosting, model usage and support staff |
| PF7 | Cumulative sign-ups are shown as active clinics |

Pick a whole number for the seed that nobody on the build team knows. Do not use 20261024, which is the main room's seed. Write the flags and the seed in a private note. Do not put them in the repo, in chat, or in a commit message.

## 2. Run the generator

Send the answer key straight to a private place with `--key-out`. Use a path outside the repo.

```
data_room/.venv/bin/python data_room/generate.py --seed 4417 --plants PF1,PF3,PF4,PF6,PF7 --key-out ~/private/variant_key.json
```

Replace the seed and the flag list with your own.

- The room is written to `data_room/hollis_voice_variant/`, and its first-tier copy to `data_room/hollis_voice_variant_seed_drop/`.
- The command prints no flag ids and no figures. It only says where the files went.
- If it stops with "does not give a valid room", that seed makes one of your flags too small to count as a real gap. Pick a different seed and run it again.
- If you leave out `--key-out`, the key goes to `data_room/answer_key_variant.json`, which git ignores. A private path outside the repo is safer.
- The same seed and flag list always give the same room, down to the byte. If the folder is lost, run the same command again.

## 3. Check that the room matches the key

```
data_room/.venv/bin/python data_room/check.py --room data_room/hollis_voice_variant --key ~/private/variant_key.json
```

It should end with `0 failed`. The first line of its output names your flags, so run it yourself and do not paste or share the output.

## 4. Keep the key sealed

- Keep the key file outside the repo, or in a private note. Do not open it near the build team.
- The variant folders are ignored by git. Hand the room to the demo laptop by copying the two folders, not by committing them.
- The room folders hold no answer key and no list of flags.
- Do not run the generator again with a different flag list and the same output folder. It overwrites the room.

## 5. At the demo

1. Point Tricorder at `hollis_voice_variant/`, first the seed drop, then the full room.
2. Show what Tricorder reports.
3. Open your key. Show which flags were planted, which were left out, and where each one sits.
4. If someone doubts the key, run the check from step 3 on stage. It reads the room back and shows the key matches the files.

The clean room is separate. `generate.py --plants off` writes `hollis_voice_clean/` and `answer_key_clean.json`. It has no flags and needs no sealing. It is there to show that Tricorder reports nothing when nothing is wrong.
