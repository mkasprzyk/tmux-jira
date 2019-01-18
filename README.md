## Create new API token for account
```
https://id.atlassian.com/manage/api-tokens
```

## Export environment variables
```
export JIRA_URL=<url>
export JIRA_USERNAME=<username>
export JIRA_TOKEN=<token>
```

## Install plugin
Add to ~/.tmux.conf following line
```
set -g @plugin 'mkasprzyk/tmux-jira'
```

## Shortcuts
```
<prefix> j #Load sessions for assigned tickets
<prefix> J #Clear all loaded sessions
```
