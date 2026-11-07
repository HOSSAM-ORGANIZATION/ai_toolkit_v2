# Universal Adaptive Makefile Guide

The `Makefile.universal` template provides a zero-configuration, self-adapting build and automation workflow for any Flutter project.

---

## 1. Dynamic Archetype Detection

The Makefile reads `project_profile.yaml` at runtime:
- **Single App Mode (`flavors: []`):**
  - Commands run directly: `make run`, `make apk`, `make aab`, `make ipa`.
  - No flavor arguments required or prompted.
- **Multi-Flavor Mode (`flavors: [dev, staging, prod]` or `[user, provider, delivery]`):**
  - Commands require or default to a flavor:
    - `make dev run` or shorthand `make dev-run`
    - `make prod apk` or shorthand `make prod-apk`
  - Shorthand targets are generated automatically for all detected flavors.

---

## 2. Mandatory Gatekeeper Integration

Before executing any `run` or `build` target, the Makefile triggers `check-profile-gate`.
If `project_profile.yaml` is absent or incomplete:
- The build halts immediately with an informative banner.
- Prompts developer to run `make toolkit-init`.

---

## 3. Toolkit Submodule Management

Configure your custom repository remote:
```makefile
TOOLKIT_REPO ?= git@github.com:<your-org>/ai_toolkit_v2.git
```

Targets:
- `make toolkit-init`: Launches the interactive Profile Wizard.
- `make toolkit-add`: Adds the toolkit submodule to a new project and triggers `setup/install.sh`.
- `make toolkit-sync`: Checkouts the pinned commit recorded in the host project.
- `make toolkit-pull`: Pulls the latest commits from `origin/main` AND synchronizes updated Cursor rules/skills into `.cursor/`.
- `make toolkit-push MSG="..."`: Commits and pushes internal improvements back to the toolkit repo.
- `make toolkit-status`: Checks the git status of the toolkit submodule.

---

## 4. Asset, Icon & Splash Automation

- `make icons`: Loops through all detected flavors and runs `flutter_launcher_icons-<flavor>.yaml` if present, or standard single-app launcher icons.
- `make splash`: Generates native splash screens per flavor and synchronizes iOS LaunchScreen storyboards automatically.
