#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -z "${JIRA_USERNAME}" ] || [ -z "${JIRA_TOKEN}" ]; then
  echo "JIRA_USERNAME and JIRA_TOKEN evironment variables must be set!"
  exit 1
fi

if [[ ! -e ${CURRENT_DIR}/.venv ]]; then
  virtualenv ${CURRENT_DIR}/.venv
  source ${CURRENT_DIR}/.venv/bin/activate
  pip install -r ${CURRENT_DIR}/requirements.txt
fi

tmux setenv JIRA_URL "${JIRA_URL}"
tmux setenv JIRA_USERNAME "${JIRA_USERNAME}"
tmux setenv JIRA_TOKEN "${JIRA_TOKEN}"
tmux setenv PATH "${CURRENT_DIR}/.venv/bin:${PATH}"

tmux bind-key j run-shell "python ${CURRENT_DIR}/app.py"
tmux bind-key J run-shell "python ${CURRENT_DIR}/app.py --clear=true"
