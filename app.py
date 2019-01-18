import commands
import logging
import click
import os

from jira import JIRA
import tabulate


logger = logging.getLogger(__name__)

DEFAULT_JIRA_URL="https://jira.atlassian.com"

jira = JIRA(os.environ.get('JIRA_URL', DEFAULT_JIRA_URL),
    basic_auth=(
        os.environ.get('JIRA_USERNAME'),
        os.environ.get('JIRA_TOKEN')
    )
)


def tmux(command):
    status, output = commands.getstatusoutput('tmux {}'.format(command))
    logger.debug('tmux command status: {}'.format(status))
    return output

def current_session():
    return tmux('display-message -p "#S"')

def get_sessions():
    return [session.split(':')[0] for session in tmux('ls').split('\n')]

def new_session(name):
    logger.debug('Creating new session: {}'.format(name))
    return tmux('new-session -d -s {}'.format(name))

def kill_session(name):
    logger.debug('Killing session: {}'.format(name))
    return tmux('kill-session -t {}'.format(name))

def add_unresolved_sessions(unresolved):
    current_sessions = get_sessions()
    for session in unresolved:
        logger.debug('Adding new session: {}'.format(session))
        if str(session) not in current_sessions:
            new_session(str(session))
        else:
            logger.debug('Session: exists!'.format(session))
    return unresolved

@click.command()
@click.option('--clear', default=False, help='Clean current sessions')
def main(clear):
    if clear:
        sessions_to_clear = get_sessions()
        sessions_to_clear.remove(current_session())
        for session in sessions_to_clear:
            kill_session(session)
        print('Sessions: {} killed'.format(', '.join(sessions_to_clear)))
    else:
        sessions = []
        assigned_issues = jira.search_issues('assignee = currentUser() AND resolution = Unresolved')
        for session in add_unresolved_sessions(assigned_issues):
            sessions.append([
                str(session),
                session.fields.assignee,
                session.fields.summary
            ])
        print(tabulate.tabulate(sessions,
            headers=['ID', 'Assignee', 'Summary']
            )
        )


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
