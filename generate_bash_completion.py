def generate_bash_completion(opts_map, cmd):
    """
    Generate a Bash completion script for the given options and suboptions.
    - opts_map: dictionary of {option: [suboption, ...], ...}
    - cmd: name of the command (e.g., 'es2panda')
    """
    func = f"_{cmd}_completions"

    # Build a space-separated string of all main options (e.g., '--foo --bar')
    opt_list = ' '.join(f'--{o}' for o in opts_map)

    # Prepare the case body for suboption completions
    case_entries = []
    for opt, subs in opts_map.items():
        # Build a space-separated string of suboptions for each option
        sub_opts = ' '.join(f'--{opt}:{s}' for s in subs)
        # Each case branch sets the 'suggestions' variable if the main option matches
        case_entries.append(f'        --{opt}) suggestions="{sub_opts}";;')
    case_body = '\n'.join(case_entries)

    # Return the formatted Bash completion script as a string
    return f'''
{func}() {{
    # Remove ':' from COMP_WORDBREAKS so Bash treats --option:suboption as one word
    COMP_WORDBREAKS=${{COMP_WORDBREAKS//:/}}

    local cur            # The current word being completed
    COMPREPLY=()         # Initialize the array for possible completions
    cur="${{COMP_WORDS[COMP_CWORD]}}"   # Get the current word

    # Completion for suboptions, e.g., --option:<TAB>
    if [[ "$cur" == --*:* ]]; then
        local opt="${{cur%%:*}}"     # Extract the main option, e.g., --foo from --foo:bar
        local suggestions=""         # To store matching suboptions

        # For each option, fill 'suggestions' if opt matches
        case "$opt" in
{case_body}
            *) suggestions="";;
        esac
        # Use compgen to generate possible suboption completions
        COMPREPLY=($(compgen -W "$suggestions" -- "$cur"))
        return 0
    fi

    # Completion for main options (when ':' is not present)
    COMPREPLY=($(compgen -W "{opt_list}" -- "$cur"))
    return 0
}}
# Register the completion function with Bash for the given command
complete -F {func} {cmd}
'''.strip()

