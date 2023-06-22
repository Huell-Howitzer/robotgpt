# Makefile

# Define the name of the virtual environment
VENV_NAME = venv

# Determine the BASE_DIR based on the location of the venv folder
BASE_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

# Set the BASE_DIR environment variable
export BASE_DIR

# Define color codes
COLOR_DEFAULT = "\033[0m"
COLOR_INFO = "\033[1;32m"
COLOR_WARNING = "\033[1;33m"
COLOR_ERROR = "\033[1;31m"

# Define messages
MSG_INFO = $(COLOR_INFO)[INFO]$(COLOR_DEFAULT)
MSG_WARNING = $(COLOR_WARNING)[WARNING]$(COLOR_DEFAULT)
MSG_ERROR = $(COLOR_ERROR)[ERROR]$(COLOR_DEFAULT)

.PHONY: all docs venv requirements

venv:
	@echo $(MSG_INFO) Activating the virtual environment and setting BASE_DIR
	@. $(VENV_NAME)/bin/activate && export BASE_DIR=$(BASE_DIR)

docs: venv
	@echo $(MSG_INFO) Building the Sphinx documentation
	@cd docs && make html && cd ..

requirements: venv
	@echo $(MSG_INFO) Installing dependencies from requirements.txt
	@pip install -r requirements.txt

all: requirements docs



