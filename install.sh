#!/usr/bin/env bash
# Installs goboscript, which build.py needs, at the commit the GitHub Action uses.
#
#   ./install.sh                 from a clone of this repo
#   ./install.sh --from-source   compile it instead of downloading
#
# On Linux (x86_64) it downloads a ready-made copy from this repo's Releases into
# ~/.local/bin: no sudo needed. Anywhere else, or with --from-source, it compiles goboscript
# with Rust, which needs (Ubuntu): sudo apt install build-essential pkg-config libssl-dev
set -euo pipefail

github_repo="wwrinkle/sla-scratch-projects"
repo="$(cd "$(dirname "$0")" && pwd)"
bin_dir="$HOME/.local/bin"

# The goboscript commit is pinned in one place: the workflow.
rev="$(sed -n 's/^ *GOBOSCRIPT_REV: *//p' "$repo/.github/workflows/build.yml")"
if [ -z "$rev" ]; then
  echo "Couldn't find GOBOSCRIPT_REV in .github/workflows/build.yml" >&2
  exit 1
fi

download() {
  local name="goboscript-linux-x86_64"
  local url="https://github.com/$github_repo/releases/download/goboscript-${rev:0:7}"
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' EXIT

  echo "Downloading goboscript ${rev:0:7}..."
  curl -fsSL -o "$tmp/$name" "$url/$name" || return 1
  curl -fsSL -o "$tmp/$name.sha256" "$url/$name.sha256" || return 1
  if ! (cd "$tmp" && sha256sum --quiet -c "$name.sha256"); then
    echo "The download doesn't match its checksum." >&2
    return 1
  fi

  mkdir -p "$bin_dir"
  install -m 755 "$tmp/$name" "$bin_dir/goboscript"
  echo "Installed $bin_dir/goboscript"
  case ":$PATH:" in
    *":$bin_dir:"*) ;;
    *) echo "Open a new terminal so $bin_dir is on your PATH." ;;
  esac
}

from_source() {
  # System packages the build needs: a C compiler, and OpenSSL (found through pkg-config).
  if ! command -v cc >/dev/null || ! command -v pkg-config >/dev/null \
     || ! pkg-config --exists openssl; then
    echo "Missing system packages. Run:" >&2
    echo "  sudo apt install build-essential pkg-config libssl-dev" >&2
    exit 1
  fi

  if ! command -v cargo >/dev/null && [ ! -x "$HOME/.cargo/bin/cargo" ]; then
    echo "Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
  fi
  # shellcheck source=/dev/null
  . "$HOME/.cargo/env"

  echo "Compiling goboscript at $rev (takes a few minutes)..."
  cargo install --locked --git https://github.com/aspizu/goboscript --rev "$rev"
  echo "Installed ~/.cargo/bin/goboscript. Open a new terminal (or run: . ~/.cargo/env)."
}

if [ "${1:-}" = "--from-source" ]; then
  from_source
elif [ "$(uname -s)-$(uname -m)" = "Linux-x86_64" ]; then
  if ! download; then
    echo "Couldn't download goboscript ${rev:0:7}; compiling it instead." >&2
    from_source
  fi
else
  from_source
fi

echo "Then build with: python3 build.py"
