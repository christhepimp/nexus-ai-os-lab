# Architecture: the OS is the AI

```
[ human intent in natural language ]
                 |
                 v
        +-------------------+
        |  Nexus control    |   policy, memory of goals
        |  plane (AI)       |
        +-------------------+
           | sense    | act
           v          v
        /proc /sys   cgroups, kill, exec, eBPF
                 |
                 v
        +-------------------+
        |  Linux kernel     |   still owns IRQ, page tables, drivers
        +-------------------+
                 |
                 v
              hardware / QEMU
```

## Control plane responsibilities

1. **World model** — compact snapshot of processes, memory, IO, thermal.
2. **Goals** — “keep ssh up”, “compile this”, “do not OOM the editor”.
3. **Policy net** — later a tiny learned model; today, rules + an LLM for *slow* decisions.
4. **Actuators** — only documented interfaces. No silent memory patches on production kernels.
5. **Audit log** — every action the AI takes is a first-class OS event.

## Timing split (important)

- Fast path (microseconds): stay in kernel / eBPF / classic CFS.
- Slow path (milliseconds+): LLM plans, explains, changes *policies*, not every context switch.

Papers that put a neural net *in* the scheduler still run a tiny model, not a 7B chat model, in the hot path.

## What “replace Linux” looks like in code

Year 0: `lab/ai_shell.py` is the face of the machine.

Year 1: a daemon owns cgroups and is PID 2-ish on a custom image.

Year n: a new kernel boots on QEMU with AI policy modules. Android emulator is retired as host.
