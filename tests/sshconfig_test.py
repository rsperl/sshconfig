import os

from sshconfig.sshconfig import parse_ssh_config, SshConfigEntry


class TestSshConfig(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_entry(self):
        e = SshConfigEntry("myhost", dict(a=1,b=2))
        e.add_option("c", "hello")
        exp = """Host myhost
    a 1
    b 2
    c hello

"""
        got = "{}".format(e)
        assert(got == exp)

    def test_parseconfig(self):
        filedir = os.path.dirname(os.path.realpath(__file__))
        sampleconfig = os.path.join(filedir, "config")
        expected = [
            SshConfigEntry('*', dict(
                ServerAliveCountMax="3",
                StrictHostKeyChecking="no",
                UserKnownHostsFile="/dev/null",
                LogLevel="ERROR",
                ServerAliveInterval="60",
                IdentityFile="~/.ssh/id_rsa"
            )),
            SshConfigEntry('*.domain.local', dict(
                ProxyCommand="ProxyCommand ssh myproxy nc %h %p"
            )),
            SshConfigEntry('*/*', dict(
                ProxyCommand="ProxyCommand ssh %r@$(dirname %h) -W $(basename %h):%p"
            )),
            SshConfigEntry('myhost1.domain.local', dict(User="root")),
            SshConfigEntry('myhost2.domain.local'),
            SshConfigEntry('myhost3', dict(HostName="myhost3.domain.local"))
        ]
        got = parse_ssh_config(sampleconfig)
        assert(len(got) == len(expected), "check length")
        for i in range(0, len(got)):
            assert(got[i] == expected[i], "compare entry")
