# Ecosystem and cache discovery

Use the project toolchain as the authority. The examples below accelerate discovery; they do not limit supported languages or prescribe fixed image templates.

## General method

For every build unit:

1. Find the canonical manifest, exact dependency lock, toolchain version, frozen install command, build command, test command, and runtime artifact.
2. Determine whether dependencies contain native code and which OS, CPU, libc, accelerator, or VM version they target.
3. Separate caches for downloaded dependencies, compiler/incremental output, test tooling, and final artifacts.
4. Keep caches out of the runtime image. Copy only the verified runtime closure from the builder.
5. Key incompatible caches by lockfile digest, toolchain, target triple/platform, build profile, and material feature set. Avoid overspecifying keys that destroy reuse without preventing contamination.
6. Consult official toolchain documentation for an unfamiliar ecosystem rather than guessing paths or flags.

## Common evidence patterns

| Ecosystem | Dependency and toolchain evidence | Typical reusable cache | Runtime result and main caveat |
|---|---|---|---|
| C/C++ | CMake, Meson, Autotools, Conan/vcpkg manifests and locks | compiler cache plus package-manager downloads | binary and shared libraries; inspect dynamic linkage and CPU baseline |
| Go | `go.mod`, `go.sum`, workspace and toolchain directives | module and build caches | binary; `CGO_ENABLED=0` is not implied, and CGO fixes the runtime ABI |
| Rust | `Cargo.toml`, `Cargo.lock`, target and feature configuration | registry, Git sources, `target`, or compiler cache | binary/library; target triple and native crates determine musl/glibc and shared libraries |
| JVM languages | Maven/Gradle manifests, wrappers, locks or verification metadata | Maven repository or Gradle caches | JAR, layered application, native image, or custom runtime; match supported JVM and diagnostics |
| .NET | solution/project files, lock files, SDK selection | NuGet packages and intermediate compiler output | framework-dependent or self-contained publish; match runtime, globalization, and diagnostics |
| Node/Bun/Deno | manifest, exact lockfile, package-manager version | content-addressed package store and build cache | source or bundled assets/server; native addons constrain OS/libc/CPU |
| Python | `pyproject.toml`, lock/requirements files, interpreter constraints | installer downloads and built wheels | source, wheel set, or environment; binary wheels and extensions constrain ABI |
| Ruby | Gemfile and lock, Ruby version, Bundler config | downloaded gems and extension builds | application plus gems; native gems constrain ABI |
| PHP | Composer manifests/lock and extension declarations | Composer download cache | source/vendor tree plus required PHP extensions |
| Elixir/Erlang | Mix/Rebar manifests, locks, OTP/Elixir versions | Hex/Rebar downloads, dependencies, incremental build | release or BEAM application; OTP and native interface compatibility matter |
| Swift | package manifest/resolution and toolchain | package downloads and `.build` outputs | native binary and libraries; Linux toolchain/runtime compatibility matters |
| Dart/Flutter | pubspec and lock, SDK constraints | package cache and build outputs | AOT/native, JS, or assets according to target |
| R/Julia | environment/manifest lock and runtime version | package/artifact depot or project library | runtime plus native packages; system-library closure matters |
| Static frontend | frontend manifest/lock and build configuration | package store and framework build cache | generated immutable assets served by a separate minimal runtime |

For another language, apply the general method and add no invented conventions.

## Cache types and trust

- **Layer cache** reuses completed image instructions. Order stable inputs before volatile source, but do not distort correctness for cache hits.
- **Dependency cache** stores fetched immutable packages or verified archives. Use locked installs; do not let mutable cache contents replace lockfile verification.
- **Compiler cache** stores target-specific intermediate work. Scope it for ABI, architecture, compiler, flags, and features that affect correctness.
- **Framework cache** may mix dependency and source-derived outputs. Confirm whether it is portable across workspaces, branches, or machines.
- **Remote CI cache** crosses a trust boundary. Prevent untrusted branches from poisoning protected release caches; separate read and write permissions when supported.

Secret values do not reliably invalidate cached steps. When a secret controls fetched content, add a non-secret version or checksum input that deliberately invalidates the step.

## Cache validation

Measure at least these paths when cache performance matters:

1. a cold build with no reusable project cache;
2. an identical warm build;
3. a source-only change;
4. a dependency-lock change;
5. a toolchain, target platform, or feature change.

Record which steps rerun and why. A fast but contaminated cache is a correctness defect; a reproducible but needlessly cold build is an optimization defect.
