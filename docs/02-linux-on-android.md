# Linux inside Android

Android = Linux kernel + Bionic libc + `init` + Binder + Zygote + ART.

The official emulator kernel is **Goldfish** (older) or **Ranchu** (newer virtio-ish board). `uname -a` on an AVD will say Linux and mention the emulator machine.

## First map (run as root)

```bash
uname -a
cat /proc/version
cat /proc/cmdline
ls /sys/devices
getprop ro.build.version.release
getprop ro.kernel.qemu          # 1 on emulator
ps -A | head
cat /proc/1/cmdline | tr '\0' ' '; echo
```

PID 1 is Android `init`, not systemd. Property service, ueventd, and zygote are started from `init.rc` language files under `/system/etc/init/`.

## Kernel vs userspace

| Layer | Examples | Can we replace soon? |
| --- | --- | --- |
| Hardware virt | QEMU / Goldfish / virtio | no — that *is* the emulator |
| Kernel | scheduler, mm, drivers | only via custom kernel build |
| Native userspace | Bionic, toolbox, binder | slowly |
| Java framework | system_server, apps | not the point |
| Our AI plane | probe + policy + shell | **yes, this week** |

## Where an AI OS plugs in without forking the kernel

- **cgroups v2** — CPU/memory limits as the AI's actuator
- **nice / ionice / taskset** — cheap scheduling hints
- **eBPF** — observe syscalls and packets; later enforce
- **init replacement** — only in a custom system image, not a Play AVD

## Building a real kernel later

If Phase 5 happens, stop using Android as the *target*. Use:

- QEMU + a tiny Rust or C kernel (see Maya / Oxide OS / MIT Fractal as inspiration)
- or a Linux kernel you compiled with extra sysfs knobs for the AI

Android is the *classroom*. The eventual AI kernel is a different tree.
