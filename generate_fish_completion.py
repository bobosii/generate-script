def generate_fish_completion(opts_map, cmd):
    """
    Generate a Fish shell completion script for the given options and suboptions.
    Falls back to file/dir completion if argument does not start with '-'.
    """
    lines = []

    lines.append(f"function __{cmd}_main_options")
    for o in opts_map:
        lines.append(f"    echo --{o}")
    lines.append("end\n")

    lines.append(f"function __{cmd}_suboptions")
    lines.append("    set -l cur (commandline -ct)")
    lines.append("    set -l mainopt (string split \":\" -- $cur)[1]")
    lines.append("    set -l cleanopt (string replace -- -- \"\" $mainopt)")
    for opt, subs in opts_map.items():
        if subs:
            for sub in subs:
                lines.append(f"    if test $cleanopt = '{opt}'; echo --{opt}:{sub}; end")
    lines.append("end\n")

    # Only offer options if argument starts with '-' (files are still shown)
    lines.append(
        f"complete -c {cmd} -n 'string match -rq \"^-\" -- (commandline -ct) && not string match -rq \"^--.*:.*\" -- (commandline -ct)' -a '(__{cmd}_main_options)'"
    )
    # Suboption completion: *** -f disables file completion ***
    lines.append(
        f"complete -c {cmd} -f -n 'string match -rq \"^--.*:.*\" -- (commandline -ct)' -a '(__{cmd}_suboptions)'"
    )

    return '\n'.join(lines)

