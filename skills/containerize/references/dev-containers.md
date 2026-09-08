# Dev Containers

Use the Development Container Specification for reproducible development environments that build on the same application and service contracts as the rest of the stack. Keep development ergonomics separate from production image and deployment requirements.

A Dev Container is the environment in which the developer, editor extensions, and development commands run. It is not inherently the production container or the entire production stack reproduced locally. Choose the relationship deliberately:

- **Standalone environment**: build or pull one development image and mount or clone the workspace into it.
- **Compose-integrated environment**: attach the editor to one development service while Compose starts the databases, queues, and other dependencies it needs.
- **Production-derived environment**: share base or build stages and service definitions, then add a development stage or override. This improves parity without putting development tools into the production target.
- **Attached environment**: connect tooling to an already running container for inspection or ad hoc work; do not present this as a reproducible repository setup.
- **Prebuilt environment**: publish the Dev Container image to reduce setup time for local, remote, or cloud development while keeping its source configuration and update policy versioned.

## Stack integration

- Identify the consuming tool, Dev Container CLI version, container engine, and Compose implementation. Verify their supported properties and commands; Docker API compatibility does not guarantee identical Podman behavior.
- Reuse an existing Containerfile stage, image, or Compose service when its runtime contract fits development. Prefer a dedicated development stage or a small Compose override for compilers, debuggers, editor agents, bind mounts, and development-only commands.
- Preserve one authoritative definition of shared dependencies, networks, ports, and build arguments. Extend the existing Compose stack instead of copying it when an override expresses the difference cleanly.
- Keep production targets free of editor extensions, source bind mounts, host sockets, broad capabilities, and development credentials. Do not infer that a working Dev Container is a tested production image.

## Configuration

- Choose exactly one primary source in `devcontainer.json`: an image, a Containerfile build, or a Compose service. Set the workspace folder and mount deliberately, accounting for volumes that mask files supplied by the image.
- Match the container user and host UID/GID behavior so the mounted workspace and caches remain writable without defaulting to root. Distinguish `remoteUser`, which controls tool and lifecycle processes, from the service's runtime user.
- Put stable OS packages and tools in the image or a versioned Feature. Use lifecycle commands only for work that depends on the mounted repository, and ensure creation and start commands terminate.
- Pin Features through the generated `.devcontainer-lock.json`, define an update policy, and use frozen lockfile validation when reproducibility is required.
- Treat forwarded ports as developer access and published ports as host exposure. Expose only what the workflow needs.
- Keep secrets out of images, Features, lifecycle commands, and committed environment files. Treat a mounted engine socket as privileged control of that engine; choose socket access, Docker-outside-of-Docker, or Docker-in-Docker only from the required isolation and workflow.
- Add only tool-specific editor settings under the appropriate `customizations` key so the portable Dev Container contract remains usable by other supporting tools.

## Interactive development

- Enable hot reload by combining a source bind mount or synchronized workspace with the framework's own watcher and development command. Dev Containers provide the environment and connectivity; they do not implement application reload semantics.
- Verify file-change delivery on the actual host, engine, remote filesystem, and framework. Use polling only when native events are demonstrably unreliable because it increases CPU and filesystem load.
- Forward the development server or debugger port through `devcontainer.json`; publish it through Compose only when non-editor host clients need direct access.
- Keep long-running application and watcher processes under the development service command, a task, or an explicit terminal command. Lifecycle hooks are for bounded setup or update work and must terminate.
- Decide whether the Dev Container tool may override the image or service command. Preserve the application command when parity matters; use a development command or keep-alive only when the editor-attached service intentionally has a different lifecycle.
- Support debugging with only the capabilities the debugger actually needs. Treat `SYS_PTRACE`, relaxed seccomp, device access, and engine socket mounts as development privileges that require explicit justification.
- Persist expensive dependency and compiler caches separately from the source workspace. Key or isolate them when toolchain, architecture, trust boundary, or lockfiles make sharing unsafe.

## Validation

1. Read the effective configuration with the pinned Dev Container CLI and inspect the selected image or build, Compose files, service, workspace, user, mounts, Features, ports, and lifecycle commands.
2. Build and start the Dev Container with its real engine. Rebuild after configuration, Containerfile, Compose, or Feature changes.
3. Execute the repository's setup, build, test, debugger, and hot-reload paths as the configured development user. Verify source and cache ownership from both host and container.
4. Start required sibling services and test their documented names, networks, health, and persistence without depending on production-only ingress.
5. Test a clean first creation as well as a rebuild with existing volumes and caches; detect stale or masked image content.
6. If CI uses the Dev Container, run its build and tests through the same pinned CLI and lockfile. Test the final production image separately.
