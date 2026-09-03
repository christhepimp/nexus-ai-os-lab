# Nexus AI OS Lab

**Goal:** use a *rooted Android emulator* as a Linux laboratory, then grow an **AI control plane** that behaves like the operating system — until, much later, pieces of Linux can be replaced.

This is a research repo, not a finished kernel. Replacing Linux is a multi-year systems problem. The useful work starts *above* the kernel: observe the host, decide policy, then take over userspace.

Repo: https://github.com/christhepimp/nexus-ai-os-lab

---

## What “the OS is the AI” actually means

Not: a chatbot that boots instead of `init`.

Yes:

1. **Sense** — the AI reads kernel and userspace state (`/proc`, `/sys`, logs, cgroups).
2. **Decide** — scheduling, memory pressure, networking, what to start or kill.
3. **Act** — through syscalls, cgroups, eBPF, later custom kernel modules.
4. **Talk** — natural language is the shell, not a bolted-on app.

Linux stays the hardware contract for a long time. The *personality* of the OS moves into the AI layer.

Related research (read these, do not copy claims blindly):

- LDOS — Learning-Directed Operating System (NSF Expeditions)
- Maya — AI-native kernel experiment in Rust
- Oxide OS — microkernel designed around agents
- openKylin 3.0 / HUMAIN OS — AI *on* Linux, not instead of it

---

## Why an Android emulator

Android **is** a Linux kernel (Goldfish / Ranchu in the official emulator) plus a Java/ART userspace.

A rooted emulator gives you:

- a disposable Linux kernel you can crash
- `adb` as the debug pipe
- no bricked phone

It does **not** give you a clean slate to delete `vmlinux` and drop in a neural net. The kernel still owns interrupts, paging, and drivers.

### Emulator paths that actually have root

Prefer official tooling first.

| Path | Root? | Notes |
| --- | --- | --- |
| AVD **Google APIs** image (not Play Store) | Usually yes | `adb root` then `adb shell` is `#` |
| AVD **Google Play** image | No by default | Play-certified; use research tools like [AERoot](https://github.com/quarkslab/AERoot) only on *your* emulator |
| [rootAVD](https://github.com/newbit1/rootAVD) + Magisk | Yes | Common for security labs |
| Genymotion | Often yes | Separate product |

Start here:

```bash
# Android SDK emulator + Google APIs system image (x86_64)
adb devices
adb root          # works on Google APIs images
adb shell id      # expect uid=0(root)
uname -a          # Linux ... qemu / ranchu
cat /proc/version
```

Play Store images: launch with the QEMU GDB stub if you use AERoot (`emulator @AVD -qemu -s`). That is emulator memory patching, not a general root exploit for phones.

Details: [docs/01-rooted-emulators.md](docs/01-rooted-emulators.md)

---

## How we “get inside Linux”

You are already inside Linux the moment you have a root shell on the AVD.

```bash
adb shell
# then:
ps -A
cat /proc/cpuinfo
ls /sys/kernel
dmesg | tail
mount
cat /proc/1/cmdline          # init / systemd-ish / init on Android
```

Android userspace is *not* a desktop distro. PID 1 is Android `init`. Binder, zygote, and ART sit on top of the same kernel syscalls.

See [docs/02-linux-on-android.md](docs/02-linux-on-android.md).

---

## How we replace Linux *slowly*

Do not rewrite `mm/` on day one. Replace *policy*, then *mechanism*.

| Phase | What we replace | Still Linux? |
| --- | --- | --- |
| 0 Lab | nothing — get root + scripts | yes |
| 1 Sense | human `top` → AI host probe | yes |
| 2 Shell | `sh` → AI shell that runs tools | yes |
| 3 Policy | CFS nice/cgroups → AI decisions | yes |
| 4 Hooks | eBPF / tiny kernel module | yes |
| 5 Twin | separate QEMU microkernel / unikernel | new kernel, not Android |
| 6 Host | only if the twin is safer and faster | maybe |

Architecture notes: [docs/03-ai-os-architecture.md](docs/03-ai-os-architecture.md)  
Roadmap: [docs/roadmap.md](docs/roadmap.md)

---

## Repo layout

```
docs/          research notes
lab/           Python probes you can run on the host (or via adb)
  probe_host.py
  ai_shell.py
```

### Run the lab on your machine (no emulator required for the mock)

```bash
python3 lab/probe_host.py
python3 lab/ai_shell.py
```

`probe_host.py` reads `/proc` on Linux. On macOS/Windows it prints a clear fallback. Against an emulator:

```bash
adb push lab/probe_host.py /data/local/tmp/
adb shell python3 /data/local/tmp/probe_host.py
# if the AVD has no python: run probe on the host and feed `adb shell cat /proc/...`
```

---

## Hard limits (read this)

- An LLM is not a scheduler. Inference latency is milliseconds to seconds; CFS runs in microseconds.
- You cannot “swap Linux for AI” while keeping Android apps. Apps depend on Bionic, Binder, and the Android ABI.
- Root on an *emulator you own* is fine. Do not use these notes on phones or devices you do not own.
- This repo does not ship exploits, kernel patches that break other people’s devices, or Play-integrity bypass kits.

---

## License

MIT. Experiments welcome. Kernel fairy tales are not.
