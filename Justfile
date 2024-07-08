set shell := ["zsh", "-cu"]
LOCATION_PYTHON := `python -c "import sys;print(sys.executable)"`

# just manual: https://github.com/casey/just/#readme

# Ignore the .env file that is only used by the web service
set dotenv-load := false

CURRENT_DIR := "$(pwd)"

grep_cmd := if "{{os()}}" =~ "macos" { "ggrep" } else { "grep" }
en0_ip := `ifconfig en0 | grep inet | cut -d' ' -f2 | grep -v ":"`


_default:
		@just --list

info:
		print "Python location: {{LOCATION_PYTHON}}"
		print "OS: {{os()}}"

# verify python is running under pyenv
which-python:
		python -c "import sys;print(sys.executable)"

restart:
  docker compose down; docker-compose up -d --build; bash request-script.sh

logs:
  docker-compose logs -f | ccze -A
