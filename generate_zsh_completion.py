def generate_zsh_completion(opts_map, cmd):
    """
    Generate a Zsh completion script for the given options and suboptions.
    """
    options = [f'--{opt}' for opt in opts_map]
    lines = [
        f"#compdef {cmd}\n",
        f"_{cmd}() {{",
        "  local cur\n  cur=${words[CURRENT]}\n"
    ]
    # If the argument doesn't start with - or --
    lines.append("  if [[ $cur != -* ]]; then")
    lines.append("    _files")
    lines.append("    return")
    lines.append("  fi")
    lines.append("  if [[ $cur == --*: ]]; then")
    lines.append("    local mainopt=\"${cur%%:*}\"")
    lines.append("    local subopts=()")
    for opt, subs in opts_map.items():
        if subs:
            sub_list = ' '.join(subs)
            lines.append(f"    [[ $mainopt == --{opt} ]] && subopts=({sub_list})")
    lines.append("    for s in $subopts; do")
    lines.append("      compadd -- \"$mainopt:$s\"")
    lines.append("    done")
    lines.append("    return\n  fi")
    lines.append("  local opts")
    lines.append(f"  opts=({' '.join(options)})")
    lines.append("  compadd -Q -a opts")
    lines.append("}\n")
    lines.append(f"compdef _{cmd} {cmd}")
    return '\n'.join(lines)

