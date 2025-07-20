def generate_fish_completion(opts_map, cmd):
    """
    Generate a Fish shell completion script for the given options and suboptions.

    - opts_map: dictionary of {option: [suboption, ...], ...}
    - cmd: name of the command (e.g., 'es2panda')
    """
    lines = []

    # Define a function to output all main options (for --option completions)
    lines.append(f"function __{cmd}_main_options")
    for o in opts_map:
        lines.append(f"    echo --{o}")
    lines.append("end\n")

    # Define a function to output suboptions for the current option (for --option:suboption completions)
    lines.append(f"function __{cmd}_suboptions")
    lines.append("    set -l cur (commandline -ct)")  # Get the current word being completed
    lines.append("    set -l mainopt (string split \":\" -- $cur)[1]")  # Extract main option before ':'
    lines.append("    set -l cleanopt (string replace -- -- \"\" $mainopt)")  # Remove leading '--'
    for opt, subs in opts_map.items():
        if subs:
            for sub in subs:
                # For each suboption, print --option:suboption if the current main option matches
                lines.append(f"    if test $cleanopt = '{opt}'; echo --{opt}:{sub}; end")
    lines.append("end\n")

    # Register the completion for main options (when ':' is not present in the current word)
    lines.append(
        f"complete -c {cmd} -f -n 'not string match -rq \"^--.*:.*\" -- (commandline -ct)' -a '(__{cmd}_main_options)'"
    )
    # Register the completion for suboptions (when ':' is present in the current word)
    lines.append(
        f"complete -c {cmd} -f -n 'string match -rq \"^--.*:.*\" -- (commandline -ct)' -a '(__{cmd}_suboptions)'"
    )

    return '\n'.join(lines)

