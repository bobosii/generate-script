def generate_zsh_completion(opts_map, cmd):
    """
    Generate a Zsh completion script for the given options and suboptions.

    - opts_map: dictionary of {option: [suboption, ...], ...}
    - cmd: name of the command (e.g., 'es2panda')
    """
    # Prepare a list of all main options as strings with '--' prefix
    options = [f'--{opt}' for opt in opts_map]

    # Begin Zsh completion script lines
    lines = [
        f"#compdef {cmd}\n",
        f"_{cmd}() {{",
        "  local cur\n  cur=${words[CURRENT]}\n"
    ]

    # Check if the current word is in the form --option:
    lines.append("  if [[ $cur == --*: ]]; then")
    # Extract the main option, e.g. --foo from --foo:bar
    lines.append("    local mainopt=\"${cur%%:*}\"")
    # Array to store suboptions
    lines.append("    local subopts=()")
    # For each option with suboptions, assign subopts if the current option matches
    for opt, subs in opts_map.items():
        if subs:
            sub_list = ' '.join(subs)
            lines.append(f"    [[ $mainopt == --{opt} ]] && subopts=({sub_list})")
    # For each suboption, suggest --option:suboption
    lines.append("    for s in $subopts; do")
    lines.append("      compadd -- \"$mainopt:$s\"")
    lines.append("    done")
    lines.append("    return\n  fi")

    # If ':' is not present, suggest main options
    lines.append("  local opts")
    lines.append(f"  opts=({' '.join(options)})")
    lines.append("  compadd -Q -a opts")

    # End the function and register with compdef
    lines.append("}\n")
    lines.append(f"compdef _{cmd} {cmd}")

    return '\n'.join(lines)

