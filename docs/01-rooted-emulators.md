# Rooted Android emulators

Use only emulators and images **you created**. This is a lab, not a phone-rooting guide.

## Recommended: Google APIs AVD (official)

1. Install Android Studio or command-line SDK (`emulator`, `avdmanager`, `sdkmanager`).
2. Download a **Google APIs** system image, not Google Play.
3. Create an AVD (x86_64 is easiest on PCs).
4. Start it, then:

```bash
adb wait-for-device
adb root
adb shell id
```

If `adb root` says the daemon cannot run as root, you picked a Play Store image.

On Google APIs images, `adbd` is allowed to restart as uid 0. That is the intended developer path.

## Play Store images

Play images keep `adbd` unprivileged. Research tools that patch *emulator* kernel memory via the QEMU GDB stub:

- [AERoot](https://github.com/quarkslab/AERoot) — current rewrite
- [android_emuroot](https://github.com/airbus-seclab/android_emuroot) — original Airbus paper/tool

Typical lab launch (from their docs):

```text
emulator @Your_AVD -qemu -s
```

Then the tool attaches GDB to the emulator and patches creds of a process. This only works on the official emulator with a matching kernel map. It is not Magisk and it does not persist across a cold boot unless you repeat it.

## Magisk on AVD

Security testers often use **rootAVD** to inject Magisk into an official AVD. After that, `adb shell su` works like a rooted phone. Useful if you need Magisk modules. Heavier than `adb root` on Google APIs.

## What root buys this project

- read all of `/proc` and `/sys`
- write cgroup knobs
- inspect kernel logs
- later: load a test kernel module (still hard on production Android images)

What it does **not** buy:

- a writable `vmlinux` you can swap for a PyTorch graph
- Binder-compatible “AI init” that still runs Play apps
