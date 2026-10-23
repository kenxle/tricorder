# Record which code was tested

A passing result belongs to the contents and conditions actually exercised.
Record commands, observations, owners, and limits in the Plan's verification
table. Include the commit and uncommitted state. A commit name alone cannot
distinguish edits made after a passing test.

Use `scripts/forge_support.py` from the Feature Forge skill to capture a command:

```sh
python3 scripts/forge_support.py --repo <repository> --evidence <new-run-directory> -- <command> <arguments>
```

The helper runs an argument list without a shell and returns the command's exit
status. If capturing provenance fails after the command, it records the actual
command status and a `capture_error`, preserves output, and returns a failure.
It saves combined output in `output.log` and metadata in `result.json`.
Choose a new directory for each run. Existing logs or results are refused.
Keep evidence outside the code tree or in a project-ignored folder so later runs
do not fingerprint previous logs as source.

The record includes before and after manifests with paths, file modes, kinds,
and SHA-256 hashes of working contents. Git tracked paths include deleted files.
Untracked non-ignored files are included. The evidence directory is excluded.
Without Git, the helper records directory files without Git ignore rules and
reports that scope. Symlinks record the link's hash, not the target's contents.
Submodule directories and special files are marked as unfingerprinted.

Use `--context <setup.json>` before `--` to attach a JSON object describing
relevant tool versions, configuration names, data fixtures, service identities,
and external conditions. Describe settings without secret values. The helper
does not inspect environment variables or establish that the supplied context is
true. Identify ignored setup and external state that the manifest cannot prove.
Do not pass secrets in command arguments or print them into captured output.

If contents, revision, or described setup change during the command,
`changed_during_run` is true. Investigate and rerun relevant checks on the intended
final state. Equal snapshots cannot rule out a concurrent change that was
reverted during execution. Keep the tested work isolated from other writers.
Treat results as observations, not an automatic pass cache or shipping verdict.
Later changes to relevant code or conditions require new proof. Preserve prior
logs and independent review findings rather than overwriting them.
