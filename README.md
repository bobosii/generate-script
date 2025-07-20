# Shell Completion Script Generator

This repository provides a modular Python tool to generate **Bash**, **Zsh**, and **Fish** shell completion scripts from a YAML configuration file.

## Usage

```bash
python3 main.py <config.yaml> [options]
```

### Required Argument

* `<config.yaml>`: Path to your YAML configuration file that defines all command options and suboptions.

### Flags / Options

* `-c, --cmd <command_name>`
  The CLI command name for which you are generating completions.
  **Default:** `completion`
  **Example:** `-c es2panda`

* `-s, --shell <shells ...>`
  Target shells for completion script generation.
  You can specify one or more of: `bash`, `zsh`, `fish`
  **Default:** All shells (`bash`, `zsh`, `fish`)
  **Example:** `-s bash zsh`

## Examples

Generate Bash, Zsh, and Fish completions for `es2panda`:

```bash
python3 main.py options.yaml -c es2panda
```

Generate only Zsh completion for `ark`:

```bash
python3 main.py runtime_options_gen.yaml -c ark -s zsh
```

Generate Bash and Fish completions for `mycli`:

```bash
python3 main.py my_options.yaml -c mycli -s bash fish
```

## How It Works

The tool reads your YAML config and extracts all options (and their suboptions) recursively.

It generates the appropriate static completion script(s) for each requested shell.

No dependencies or parsing is required at shell runtime; the scripts are ready to copy into the system.

## Output

By default, the generated completion script is printed to `stdout`.
You can redirect the output into the right location for your shell, for example:

**Bash (for testing):**

```bash
python3 main.py options.yaml -c es2panda -s bash > _es2panda
sudo cp _es2panda /usr/share/bash-completion/completions/es2panda
```

**Zsh:**

```bash
python3 main.py options.yaml -c es2panda -s zsh > _es2panda
sudo cp _es2panda /usr/share/zsh/functions/Completion/Unix/_es2panda
```

**Fish:**

```bash
python3 main.py options.yaml -c es2panda -s fish > es2panda.fish
cp es2panda.fish ~/.config/fish/completions/es2panda.fish
```

## YAML Structure Example

```yaml
options:
  - name: foo
    sub_options:
      - name: error
      - name: enable
      - name: disable
  - name: bar
    sub_options:
      - name: line
      - name: source
      - name: files
  # ... more options ...
```

## Requirements

* Python 3
* PyYAML (`pip install pyyaml`)

