import logging

from django.contrib import messages
from django.core.management import call_command
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger("django")


def all_db_backup(request):
    try:
        feedback_db_backup(request)
        users_db_backup(request)
        core_db_backup(request)
        analytics_db_backup(request)
        messages.success(request, _('All DBes were successfully backed up.'))
        return redirect('users:backups_table')
    except Exception as e:
        logger.error('All databases backup, %s', str(e))
        messages.error(request, _('Error: ') + str(e))
        return redirect('users:backups_table')


def feedback_db_backup(request):
    """
    Unknown option(s) for dbbackup command: stdin.
    Valid options are: clean, compress, database,
    encrypt, force_color, help, interactive, no_color, noinput, output_filename, output_path,
    pythonpath, quiet, servername, settings, skip_checks, stderr, stdout, traceback, verbosity, version.

    :param request:
    :return:
    """
    try:
        call_command('dbbackup', '-d', 'feedback_db')
        messages.success(request, _('The Feedback DB was successfully backed up.'))
        return redirect('users:backups_table')
    except Exception as e:
        logger.error('The feedback databases backup, %s', str(e))
        print(str(e))
        messages.error(request, _('Error: ') + str(e))
        return redirect('users:backups_table')


def users_db_backup(request):
    try:
        call_command('dbbackup', '-d', 'users_db')
        messages.success(request, _('The Users DB was successfully backed up.'))
        return redirect('users:backups_table')
    except Exception as e:
        logger.error('The Users databases backup, %s', str(e))
        messages.error(request, _('Error: ') + str(e))
        return redirect('users:backups_table')


def core_db_backup(request):
    try:
        call_command('dbbackup', '-d', 'search_db')
        messages.success(request, _('The Core DB was successfully backed up.'))
        return redirect('users:backups_table')
    except Exception as e:
        logger.error('The Core databases backup, %s', str(e))
        messages.error(request, _('Error: ') + str(e))
        return redirect('users:backups_table')


def analytics_db_backup(request):
    try:
        call_command('dbbackup', '-d', 'analytics_db')
        messages.success(request, _('The Analytics DB was successfully backed up.'))
        return redirect('users:backups_table')
    except Exception as e:
        logger.error('The Analytics databases backup, %s', str(e))
        messages.error(request, _('Error: ') + str(e))
        return redirect('users:backups_table')


def crawler_db_backup(request):
    try:
        call_command('dbbackup', '-d', 'crawler_db')
        messages.success(request, _('The Crawler DB was successfully backed up.'))
        return redirect('users:backups_table')
    except Exception as e:
        logger.error('The Analytics databases backup, %s', str(e))
        messages.error(request, _('Error: ') + str(e))
        return redirect('users:backups_table')
