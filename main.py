#!/usr/bin/env python3

import argparse
import yaml
import re
from generate_bash_completion import generate_bash_completion
from generate_zsh_completion import generate_zsh_completion
from generate_fish_completion import generate_fish_completion

def load_yaml(path):
    """
    Load the YAML file from the given path and return the parsed structure as a Python object.
    """
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def collect_options(config):
    """
    Recursively traverse the YAML config to extract all options and their suboptions.

    Returns:
        A dictionary mapping option names to lists of suboption names, e.g.
        {
            "option1": ["suboptionA", "suboptionB"],
            "option2": [],
            ...
        }
    """
    opts = {}
    def rec(node):
        if isinstance(node, dict):
            name = node.get('name')
            subs = None
            # Look for a key that looks like 'sub_options', 'suboptions', etc.
            for k, v in node.items():
                if isinstance(v, list) and re.match(r'(?i)^sub[-_]?options?$', k):
                    # Extract suboption names from the list
                    subs = [item['name'] for item in v if isinstance(item, dict) and 'name' in item]
                    break
            # Register this option and any suboptions
            if name:
                opts.setdefault(name, [])
                if subs:
                    opts[name].extend(subs)
            # Recursively process all values (in case of nested options)
            for v in node.values():
                rec(v)
        elif isinstance(node, list):
            # If the node is a list, recurse into each item
            for item in node:
                rec(item)
    # Start recursion from the root of the YAML structure
    rec(config)
    # Remove duplicates and sort suboptions for each option
    for k in opts:
        opts[k] = sorted(set(opts[k]))
    return opts

def main():
    """
    Main entry point for the script. Parses arguments, loads config,
    extracts options, and prints the generated shell completion script(s).
    """
    parser = argparse.ArgumentParser(
        description='Shell completion script generator from a YAML config'
    )
    parser.add_argument(
        'config',
        help='YAML config file containing option and suboption definitions'
    )
    parser.add_argument(
        '-c', '--cmd',
        help='Name of the target command (e.g. es2panda)',
        default='completion'
    )
    parser.add_argument(
        '-s', '--shell',
        choices=['bash', 'zsh', 'fish'],
        nargs='+',
        default=['bash', 'zsh', 'fish'],
        help='Target shells to generate completions for (default: all)'
    )
    args = parser.parse_args()

    cfg = load_yaml(args.config)

    # Extract all options and suboptions from the config
    opts_map = collect_options(cfg)

    for sh in args.shell:
        if sh == 'bash':
            print(generate_bash_completion(opts_map, args.cmd))
        elif sh == 'zsh':
            print(generate_zsh_completion(opts_map, args.cmd))
        elif sh == 'fish':
            print(generate_fish_completion(opts_map, args.cmd))

if __name__ == '__main__':
    main()

