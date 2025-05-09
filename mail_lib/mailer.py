import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
dt = lambda : str(datetime.datetime.now())[5:16]
import json
import platform
import socket
import os
import os_lib.generate_firewall as fwl
import os_lib.sudo_log as sudo_log

def get_server_identity():
    """Get information about the server"""
    server_info = {
        'hostname': socket.gethostname(),
        'ip_address': socket.gethostbyname(socket.gethostname()),
        'os': platform.system(),
        'os_version': platform.release(),
        'architecture': platform.machine(),
        'python_version': platform.python_version()
    }
    return server_info

def load_json_file(fname):
    with open(fname,'r') as fi:
        s = ''.join(fi.readlines())
    return json.loads(s)

def get_local_mail_creds():
    from pathlib import Path
    p = Path(__file__).absolute().parent.parent
    p = p / "local_files" / "mail_creds.json"
    return load_json_file(p)

def get_receivers():
    from pathlib import Path
    p = Path(__file__).absolute().parent.parent
    p = p / "local_files" / "receivers.json"
    return load_json_file(p)['receivers']

def format_server_info(server_info):
    """Format server information for email"""
    return f"""
    Server Information:
    -------------------
    Hostname: {server_info['hostname']}
    IP Address: {server_info['ip_address']}
    OS: {server_info['os']} {server_info['os_version']}
    Architecture: {server_info['architecture']}
    Python Version: {server_info['python_version']}
    """

def send_email():
    # Get server information
    server_info = get_server_identity()
    receivers = get_receivers()
    
    subject = f"{dt()} -- {server_info['hostname']} -- Heartbeat (sys info, sudo logs) "

    # Add server information to the email
    server_info_text = format_server_info(server_info)
    server_info_html = f"<pre>{server_info_text}</pre>"

    sudo_logs = sudo_log.get_sudo_logs()
    sudo_logs = sudo_logs[::-1][:32]

    ssh_logs = sudo_log.get_ssh_logs()
    ssh_logs = ssh_logs[::-1][:32]
    
    # Combine original content with server information
    full_text = f"\n{server_info_text}\n\n"
    full_text += "Last 32 sudo logs\n"

    for row in sudo_logs:
        full_text += f"{row['date']} {row['terminal_user']} {row['command']}\n"
    full_text += "\n\n"

    full_text += "Last 32 SSH logs\n"

    for row in ssh_logs:
        text_snippet = row['text'][:50].strip('\n')
        process = row['process'].split('[')[0]
        while len(process) < 8:
            process += ' '
        full_text += f"{row['date'][5:16]} {process} -- {text_snippet}\n"
    full_text += "\n\n"

    full_html = f"<h2>Reporting Server</h2><br><br>{server_info_html}<br><br>"
    table_html = ""
    for row in sudo_logs:
        table_html += f"<tr><td>{row['date']}</td><td>{row['terminal_user']}</td><td>{row['command']}</td></tr>"
    table_html = f"<h3>Last 32 sudo events on {server_info['hostname']}</h3><table><tr><th>Datetime</th><th>User Account</th><th>Command</th>{table_html}</table>"
    full_html += table_html

    table_html = ""
    for row in ssh_logs:
        table_html += f"<tr><td>{row['date']}</td><td>{row['process']}</td><td>{row['text']}</td></tr>"
    table_html = f"<h3>Last 32 ssh events on {server_info['hostname']}</h3><table><tr><th>Datetime</th><th>Process</th><th>Text</th>{table_html}</table>"
    full_html += table_html

    full_html = f"""
    <html>
      <body>
        {full_html}
      </body>
    </html>
    """

    mail_creds = get_local_mail_creds()

    # Email configuration
    smtp_server = mail_creds['smtp_server']
    smtp_port = mail_creds['smtp_port']
    from_email = mail_creds['from_email']
    password = mail_creds['password']

    to_email = ', '.join(receivers)

    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"📡 {subject} - From {server_info['hostname']}"
    msg['From'] = from_email
    msg['To'] = to_email

    # Create the body of the message
    part1 = MIMEText(full_text, 'plain')
    part2 = MIMEText(full_html, 'html')

    # Attach parts into message container
    msg.attach(part1)
    msg.attach(part2)

    try:
        # Connect to the server and send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email.split(', '), msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

    # print(fwl.generate_iptables_rules())