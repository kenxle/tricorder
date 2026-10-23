#!/bin/sh
# Run the checklist coverage spike on every room and stage the feature docs quote,
# then rebuild the prototype with the fresh output inlined. Run from the repo root:
#   sh docs/features/20261022.13_checklist_coverage/spike/run_all.sh
set -e
S=docs/features/20261022.13_checklist_coverage/spike
G=$S/sample_gaps_seed_drop.json
for st in series_a seed pre_seed; do
  python3 $S/coverage_spike.py data_room/hollis_voice_seed_drop --stage $st --gaps $G --out $S/out/seed_drop_$st.json
done
python3 $S/coverage_spike.py data_room/hollis_voice_seed_drop --out $S/out/seed_drop_auto.json
for st in series_a seed pre_seed; do
  python3 $S/coverage_spike.py data_room/hollis_voice --stage $st --out $S/out/full_room_$st.json
done
python3 $S/coverage_spike.py data_room/hollis_voice --out $S/out/full_room_auto.json
python3 $S/coverage_spike.py data_room/brasswick --out $S/out/brasswick_auto.json
python3 $S/coverage_spike.py data_room/hollis_voice_seed_drop --stage series_b --out $S/out/stage_unknown.json
python3 $S/build_prototype.py
