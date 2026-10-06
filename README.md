# myls

A simple command-line tool that lists the files in a folder, with options for filtering, sorting, and colored or icon output.

## Installation

```bash
git clone https://github.com/S1aken/ls.git
cd ls
pip install -e .
```

After installing, the `myls` command is available in your terminal.

## Quick start

```bash
myls                      # list the current folder
myls /path/to/folder      # list a specific folder
```

With no options, hidden files are not shown, the list is sorted by name, and the output is plain text.

## Options

| Option | Values | Default | What it does |
|---|---|---|---|
| `--filter` | `visible`, `all`, `files`, `dirs` | `visible` | Chooses what gets listed |
| `--sort` | `name`, `size`, `date` | `name` | Chooses the sort criterion |
| `--style` | `plain`, `color`, `icons` | `plain` | Chooses how the output looks |
| `--color` | `blue`, `red`, `green`, `yellow` | `blue` | Chooses the color used by `--style color` |

### `--filter` values

| Value | Result |
|---|---|
| `visible` | Everything that is not hidden (files and folders) |
| `all` | Everything, including hidden items such as `.git` |
| `files` | Files only |
| `dirs` | Folders only |

### `--sort` values

| Value | Result |
|---|---|
| `name` | By name, A to Z |
| `size` | By size, smallest to largest |
| `date` | By last modified time, oldest to newest |

### `--style` values

| Value | Result |
|---|---|
| `plain` | Plain text |
| `color` | Folders are colored, files stay in the default color |
| `icons` | 📁 before folders, 📄 before files |

## Examples

Show everything, including hidden items:

```bash
myls --filter all
```

Show folders only:

```bash
myls --filter dirs
```

Show files only, sorted by size:

```bash
myls --filter files --sort size
```

Put the most recently modified file last:

```bash
myls --filter files --sort date
```

Show folders in red:

```bash
myls --style color --color red
```

Show a list with icons:

```bash
myls --style icons
```

Combine everything: files only, sorted by size, with icons:

```bash
myls --filter files --sort size --style icons
```

List another folder, including hidden items, sorted by date:

```bash
myls /path/to/folder --filter all --sort date
```

## Good to know

- The order of the options does not matter. `myls --sort size --filter files` gives the same result as `myls --filter files --sort size`.
- `--color` only has an effect together with `--style color`. With `--style icons` it is ignored.
- `--style color` only colors folders. Files stay in the default color.
- A folder's size is not the total size of its contents. It is the size of the folder entry itself (often shown as 0 on Windows). `--sort size` gives the most meaningful result together with `--filter files`.
- If you pass a folder that does not exist, you get this error: `No such directory: '...'`.
- If you pass an invalid value (for example `--sort weight`), the tool prints an error that lists the valid choices.

## Help

```bash
myls --help
```

## Running the tests

```bash
pip install pytest
pytest -q
```
