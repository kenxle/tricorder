# Establish a working environment

Before implementation, identify the setup needed to build and exercise the
change. Use the project's setup and testing instructions. Check again before
final proof, especially after switching worktrees or restarting services.

- Confirm dependencies, tool versions, and configuration names. Check required
  keys are available without printing their values or copying them into evidence.
- Check backing services, migrations, permissions, and representative test data.
  Use isolated data and accounts appropriate to the environment.
- Start or locate the actual application and required workers. Verify the
  intended revision, URL or entry point, and a real request or command. A process
  running does not prove that the application works.
- Record missing prerequisites, their owner, and the next action in
  [Progress](progress-and-handoffs.md). Do independent work while resolving them.

Prefer the project's repeatable setup and health commands over manual repair.
Do not invent a passing result, replace required services with mocks for final
proof, or disclose secrets to explain a blocker. A local test environment does
not establish readiness of the deployed environment.

Missing required setup blocks shipping under the
[hard shipping rule](verification-and-release.md#hard-shipping-rule). Fix the
setup and run the full suite in the corrected environment. If a prerequisite is
unavailable, name it and report shipping blocked.
