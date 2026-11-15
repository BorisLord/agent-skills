# Docker AI product skill routing

Docker Sandboxes and Docker Agent are separate products from OCI application image and deployment engineering. Use the owning [official Docker skill](https://github.com/docker/skills#skills) when it is installed. If it is unavailable, identify the relevant skill and link its source rather than claiming to have loaded it or installing it without a request. For mixed tasks, use `containerize` only for the image or container-engineering contract.

## Docker Sandboxes

| Task | Official skill |
| --- | --- |
| Create, reattach to, stop, or remove a standalone `sbx` sandbox; choose workspace isolation | [`docker-sandboxes-lifecycle`](https://github.com/docker/skills/blob/main/skills/docker-sandboxes-lifecycle/SKILL.md) |
| Configure `sbx` network policy, credentials, or registry access | [`docker-sandboxes-network-credentials`](https://github.com/docker/skills/blob/main/skills/docker-sandboxes-network-credentials/SKILL.md) |
| Author or run a declarative `sbxenv.yaml` environment | Current [official Docker Sandboxes documentation](https://docs.docker.com/ai/sandboxes/); discover the current catalog before naming an owning skill |
| Author, verify, or distribute a v3 `sbx kit` descriptor | [`docker-sandboxes-kits`](https://github.com/docker/skills/blob/main/skills/docker-sandboxes-kits/SKILL.md) (experimental) |

Legacy v2 `spec.yaml` kits are outside the current `docker-sandboxes-kits` skill. Check the installed version and its matching official documentation; do not claim that the v3 skill authors or debugs v2 kits, or silently migrate them.

## Docker Agent

| Task | Official skill |
| --- | --- |
| Configure Docker Agent's `agent.yaml`, models, tools, or teams | [`docker-agent-config`](https://github.com/docker/skills/blob/main/skills/docker-agent-config/SKILL.md) |
| Run Docker Agent, choose approvals, sandbox isolation, or worktrees | [`docker-agent-run`](https://github.com/docker/skills/blob/main/skills/docker-agent-run/SKILL.md) |
| Serve, share, or evaluate Docker Agent | [`docker-agent-deploy`](https://github.com/docker/skills/blob/main/skills/docker-agent-deploy/SKILL.md) |

`docker agent run --sandbox` belongs to `docker-agent-run`; standalone `sbx run` belongs to `docker-sandboxes-lifecycle`. Load both owning skills when a task crosses their boundaries. Podman AI Lab and third-party agent sandbox launchers are separate workflows; this skill covers their OCI image and container-runtime aspects, not their agent-specific lifecycle or credential brokerage.
