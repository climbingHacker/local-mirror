# Package Mirroring Tool

This is a simple tool for creating various partial package mirrors.

## Setup

Copy `example.mirror.toml` to `mirror.toml` and adjust the options to your needs.

## Architecture

### apt mirror

The Metadata is Parsed from the upstream Mirror and stored in a MySQL database. Packages are added to a tracking list once they're retrieved at least once. Tracked packages are cached locally.

### MySql Scheme: debian

#### distros

| id                              | distro       | amd64    | i368     | arm64   | armhf     | riscv64  | armel    | loong64  | ppc64el  | s390x    |
|---------------------------------|--------------|----------|----------|----------|----------|----------|----------|----------|----------|----------|
| INT                             | VARCHAR(255) | BOOLEAN  | BOOLEAN  | BOOLEAN  | BOOLEAN  | BOOLEAN  | BOOLEAN  | BOOLEAN  | BOOLEAN  | BOOLEAN  |
| AUTO_INCREMENT <br> PRIMARY KEY |              | NOT NULL | NOT NULL | NOT NULL | NOT NULL | NOT NULL | NOT NULL | NOT NULL | NOT NULL | NOT NULL |

## Project Structure

```
├── apt.py      # functions and classes for debian style mirrors
├── main.py     # Flask app
├── setup-db.py # DB setup script
└──             # 
```

## AI Declaration

Very bad AI inline suggestions(qwen2.5-coder-0.5b) were used in this Project, also AI(deepseek-v4.1-flash) was used for researching and understanding concepts.
