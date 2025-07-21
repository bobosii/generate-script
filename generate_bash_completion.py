def generate_bash_completion(opts_map, cmd):
    """
    Generate a Bash completion script for the given options and suboptions.
    Falls back to file/dir completion (ls behavior) if argument does not start with '-'.
    """
    func = f"_{cmd}_completions"
    opt_list = ' '.join(f'--{o}' for o in opts_map)
    case_entries = []
    for opt, subs in opts_map.items():
        sub_opts = ' '.join(f'--{opt}:{s}' for s in subs)
        case_entries.append(f'        --{opt}) suggestions="{sub_opts}";;')
    case_body = '\n'.join(case_entries)
    return f'''
{func}() {{
    COMP_WORDBREAKS=${{COMP_WORDBREAKS//:/}}

    local cur
    cur="${{COMP_WORDS[COMP_CWORD]}}"

    # If not starting with '-', fallback to default file completion
    if [[ -z "$cur" || ! "$cur" =~ ^- ]]; then
        return 1
    fi

    # Suboption completion
    if [[ "$cur" == --*:* ]]; then
        local opt="${{cur%%:*}}"
        local suggestions=""
        case "$opt" in
{case_body}
            *) suggestions="";;
        esac
        COMPREPLY=($(compgen -W "$suggestions" -- "$cur"))
        return 0
    fi

    COMPREPLY=($(compgen -W "{opt_list}" -- "$cur"))
    return 0
}}
complete -o default -F {func} {cmd}
'''.strip()

