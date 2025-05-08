def get_sudo_logs():
    """Get parsed logs of attempts to use sudo, successful and unsuccessful alike"""
    import datetime
    yr = str(datetime.datetime.now().year)
    date_parser = lambda dtstr: str(datetime.datetime.strptime(yr+' '+ dtstr,'%Y %b %d %H:%M:%S'))[:19]
    import os
    stream = os.popen('journalctl _COMM=sudo | grep COMMAND')
    output = list(stream.readlines())
    sudo_rows = list()
    for row in output:
        row_text = row.replace(" : user NOT in sudoers ; ","_user_NOT_in_sudoers : ")
        row_command = row_text.split(' ; COMMAND=')[1].strip('\n')
        row_rest = row_text.split(' ; COMMAND=')[0]
        row_user = row_rest.split(' ; USER=')[1]
        row_rest = row_rest.split(' ; USER=')[0]
        row_pwd = row_rest.split(' ; PWD=')[1]
        row_rest = row_rest.split(' ; PWD=')[0]
        try:
            row_tty = row_rest.split(' : TTY=')[1]
            row_rest = row_rest.split(' : TTY=')[0]
        except:
            print(row_rest)
        row_terminal_user = row_rest.split(':')[-1].strip()
        row_rest = ':'.join( row_rest.split(':')[:-1] )
        row_process = row_rest.split(' ')[-1]
        row_machine = row_rest.split(' ')[-2]
        row_date = date_parser( ' '.join(row_rest.split(' ')[:-2]) )
        row_parsed = dict()    
        row_parsed['date'] = row_date
        row_parsed['invoked_user'] = row_user
        row_parsed['terminal_user'] = row_terminal_user
        row_parsed['device'] = row_machine
        row_parsed['process'] = row_process
        row_parsed['pwd'] = row_pwd
        row_parsed['tty'] = row_tty
        row_parsed['command'] = row_command
        sudo_rows += [ row_parsed ]
    return sudo_rows

def get_ssh_logs():
    """Get parsed logs of attempts to use ssh, successful and unsuccessful alike"""
    import datetime
    yr = str(datetime.datetime.now().year)
    date_parser = lambda dtstr: str(datetime.datetime.strptime(yr+' '+ dtstr,'%Y %b %d %H:%M:%S'))[:19]
    import os
    stream = os.popen('journalctl -u ssh -S -3000')
    output = list(stream.readlines())
    sudo_rows = list()
    for row in output:
        try:
            row_date_part = str(date_parser(' '.join(row.split(' ')[:3])))[:19]
            row_device = row.split(' ')[3]
            row_process = row.split(' ')[4]
            row_text = ' '.join(row.split(' ')[5:])
            row_json = \
                {
                    "date": row_date_part,
                    "device": row_device,
                    "process": row_process,
                    "text": row_text
                }
            sudo_rows += [row_json]
        except:
            pass
    return sudo_rows