def generate_iptables_rules():
    def block_snippet(ip):
        res = f"""-A INPUT -s {ip} -j DROP
-A OUTPUT -s {ip} -j DROP"""
        return res
    import os
    script_dir = os.path.abspath( os.path.dirname( __file__ ) )+"/"
    with open(script_dir+'local_files/block.ips','r') as fi:
        ip_list = fi.readlines()
    ip_list = list(map(lambda z: str(z).strip('\n'),ip_list))
    p0 = """*filter
:INPUT DROP [1332:62688]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [8601:2465080]"""
    plast = """
-A INPUT -i lo -j ACCEPT
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
-A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT
COMMIT
"""
    block_lines = '\n'.join(list(map(block_snippet,ip_list)))
    return p0+block_lines+plast

if __name__=="__main__":
    print(generate_iptables_rules())