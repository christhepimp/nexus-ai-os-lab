# Roadmap

## Phase 0 — Lab is real (this repo)

- [x] Charter and docs
- [x] Host probe + toy AI shell
- [ ] You: Google APIs AVD + `adb root` screenshot / log in `lab/notes/`

## Phase 1 — Sense

- Parse `/proc/stat`, `/proc/meminfo`, `/proc/*/status` over `adb`
- Emit a JSON world-model the model can read

## Phase 2 — Act (safe)

- AI may `renice` and set cgroup max on *named* lab processes only
- Hard denylist: `init`, `adbd`, `system_server`

## Phase 3 — Language as shell

- Tool-calling loop: list / inspect / limit / explain
- All tools logged

## Phase 4 — Kernel-adjacent

- eBPF tracepoints for scheduler and syscalls (host Linux first, AVD if kernel allows)
- Optional out-of-tree module on a *custom* kernel, never a random Play image

## Phase 5 — Twin kernel

- New repo or `kernel/` tree: boot a hello-world kernel in QEMU
- Add a policy interface the control plane already speaks

## Done looks like

Not “Linux deleted.” Done is: the human talks to Nexus, Nexus keeps the machine alive, and Linux is an implementation detail you could swap.
