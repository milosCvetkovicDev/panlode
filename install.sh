#!/usr/bin/env bash
# Install the idea workspace from template/ into a folder.
#
#   ./install.sh [--force] [--dry-run] <target-dir>
#
# Without --force no existing file is touched. --force refreshes engine files only (scripts/,
# .claude/agents/, .claude/rules/, .claude/skills/, templates/) in an existing workspace; your CLAUDE.md,
# founder/ files, .claude/settings.json and records are never overwritten. A symlink in the target, file
# or folder, is never written through. --dry-run prints the plan and writes nothing.
# Works with the bash 3.2 that ships with macOS.
set -euo pipefail

usage() {
  echo "usage: install.sh [--force] [--dry-run] <target-dir>" >&2
}

force=0
dry=0
target=""
set_target() {
  if [ -n "$target" ]; then
    echo "install.sh: only one target folder is allowed" >&2
    usage
    exit 2
  fi
  target="$1"
}
while [ $# -gt 0 ]; do
  case "$1" in
    --force) force=1 ;;
    --dry-run) dry=1 ;;
    -h | --help)
      usage
      exit 0
      ;;
    --)
      shift
      for arg in "$@"; do
        set_target "$arg"
      done
      break
      ;;
    -*)
      echo "install.sh: unknown option: $1" >&2
      usage
      exit 2
      ;;
    *) set_target "$1" ;;
  esac
  shift
done
if [ -z "$target" ]; then
  usage
  exit 2
fi
case "$target" in
  "~" | "~/"*)
    echo "install.sh: $target starts with a ~ the shell did not expand; pass an absolute path" >&2
    exit 2
    ;;
esac
# $(dirname) and $(basename) strip trailing newlines, so a name ending in one would change the path.
newline='
'
case "$target" in
  *"$newline"*)
    echo "install.sh: the target path contains a newline; pass a plain path" >&2
    exit 2
    ;;
esac

here="$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
src="$here/template"
if [ ! -d "$src" ]; then
  echo "install.sh: template/ not found next to install.sh ($here)" >&2
  exit 1
fi
if [ -e "$target" ] && [ ! -d "$target" ]; then
  echo "install.sh: $target exists and is not a folder" >&2
  exit 1
fi

# Absolute physical path of a folder that may not exist yet.
resolve() {
  local path="$1" rest=""
  while [ ! -d "$path" ]; do
    rest="/$(basename -- "$path")$rest"
    path="$(dirname -- "$path")"
  done
  # A .. below a missing folder can be neither resolved by cd nor compared by identity, so it would slip
  # past the guards below.
  case "$rest/" in
    */../*)
      echo "install.sh: $1 has a .. after a folder that does not exist yet; pass a plain path" >&2
      exit 2
      ;;
  esac
  printf '%s%s\n' "$(CDPATH='' cd -- "$path" && pwd -P)" "$rest"
}

refuse() {
  echo "install.sh: refusing to install into $abs: $1" >&2
  exit 1
}

# Compared by identity (-ef: same device and inode) as well as by spelling: macOS volumes are
# case-insensitive by default, so one folder has many spellings.
same_folder() {
  [ "$1" = "$2" ] || { [ -e "$1" ] && [ "$1" -ef "$2" ]; }
}

# True when the folder $2 is the absolute path $1 or one of the folders above it.
at_or_above() {
  local dir="$1"
  while :; do
    if same_folder "$dir" "$2"; then
      return 0
    fi
    if [ "$dir" = "/" ]; then
      return 1
    fi
    dir="$(dirname -- "$dir")"
  done
}

# The workspace's .claude/ and CLAUDE.md would apply to every project below the target.
abs="$(resolve "$target")"
if same_folder "$abs" "/"; then
  refuse "the root folder"
fi
if [ -n "${HOME:-}" ]; then
  home="$(resolve "$HOME")"
  if same_folder "$abs" "$home"; then
    refuse "your home folder; pick a new folder such as $home/ideas"
  fi
  if at_or_above "$home" "$abs"; then
    refuse "a parent of your home folder"
  fi
fi
if at_or_above "$abs" "$here"; then
  refuse "it is inside the release that holds install.sh"
fi
if [ "$force" -eq 1 ] && { [ ! -f "$abs/scripts/engine.py" ] || [ ! -d "$abs/scripts/ideaengine" ]; }; then
  echo "install.sh: --force updates an existing workspace, and $abs is not one" \
    "(no scripts/engine.py and scripts/ideaengine/); run without --force to install" >&2
  exit 1
fi

is_engine_file() {
  case "$1" in
    scripts/* | .claude/agents/* | .claude/rules/* | .claude/skills/* | templates/*) return 0 ;;
    *) return 1 ;;
  esac
}

# Files that may sit in a maintainer's template/ but never belong in a user's workspace.
is_local_state() {
  case "$1" in
    INDEX.md | .claude/settings.local.json | .claude/checkpoints/* | .DS_Store | */.DS_Store) return 0 ;;
    __pycache__/* | */__pycache__/* | .pytest_cache/* | */.pytest_cache/* | *.pyc | *.swp | *~) return 0 ;;
    *) return 1 ;;
  esac
}

# True when a folder between $abs and the file is a symlink (dangling or not); mkdir -p and cp would
# write into wherever it points.
parent_is_symlink() {
  local dir
  dir="$(dirname -- "$1")"
  while [ "$dir" != "." ]; do
    if [ -L "$abs/$dir" ]; then
      return 0
    fi
    dir="$(dirname -- "$dir")"
  done
  return 1
}

added=0
updated=0
kept=0
install_file() {
  local rel="$1" file="$src/$1" dest="$abs/$1"
  if [ -L "$dest" ]; then
    echo "skip $rel (symlink; never written through)"
    kept=$((kept + 1))
  elif parent_is_symlink "$rel"; then
    echo "skip $rel (symlinked folder; never written through)"
    kept=$((kept + 1))
  elif [ -e "$dest" ]; then
    if cmp -s "$file" "$dest"; then
      kept=$((kept + 1))
    elif [ "$force" -eq 1 ] && is_engine_file "$rel"; then
      echo "update $rel"
      updated=$((updated + 1))
      if [ "$dry" -eq 0 ]; then
        cp "$file" "$dest"
      fi
    else
      echo "skip $rel (yours differs; kept)"
      kept=$((kept + 1))
    fi
  else
    echo "add $rel"
    added=$((added + 1))
    if [ "$dry" -eq 0 ]; then
      mkdir -p "$(dirname -- "$dest")"
      cp "$file" "$dest"
    fi
  fi
}

# .claude/settings.json wires the hooks to scripts/engine.py, so it goes in last: an install cut short
# never leaves hooks pointing at an engine that is not there yet.
while IFS= read -r -d '' file; do
  rel="${file#"$src"/}"
  if is_local_state "$rel" || [ "$rel" = ".claude/settings.json" ]; then
    continue
  fi
  install_file "$rel"
done < <(find "$src" -type f -print0 | sort -z)
install_file ".claude/settings.json"

generate_index=0
if [ ! -e "$abs/INDEX.md" ] && [ ! -L "$abs/INDEX.md" ]; then
  generate_index=1
  echo "generate INDEX.md"
fi

mode=""
if [ "$dry" -eq 1 ]; then
  mode=" (dry run, nothing written)"
fi
echo "added $added, updated $updated, skipped $kept already present$mode"

if [ "$dry" -eq 1 ]; then
  exit 0
fi

# The index comes from the engine shipped here, never from code that was already in the target.
if command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; sys.exit(sys.version_info < (3, 10))'; then
  if [ "$generate_index" -eq 1 ]; then
    PYTHONDONTWRITEBYTECODE=1 python3 -B "$src/scripts/engine.py" --root "$abs" index >/dev/null
  fi
else
  echo "warning: Python 3.10 or newer was not found as python3; the engine and the hooks need it." >&2
fi

cat <<EOF

Next:
  1. cd "$abs" && git init
  2. Fill in founder/profile.md, founder/constraints.md and founder/channels.md.
  3. Start Claude Code there and run /scout-online.
EOF
