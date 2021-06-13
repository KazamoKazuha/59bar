def b(s):
    return ('[b]%s[/b]' % (s))


def i(s):
    return ('[i]%s[/i]' % (s))


def u(s):
    return ('[u]%s[/u]' % (s))


def d(s):
    return ('[del]%s[/del]' % (s))

def size(s,siz):
    return ('[size=%s]%s[/size]' %(siz,s))

def collapse(s, t: ''):
    if t != '':
        t = '='+t
    return ('[collapse%s]%s[/collapse]\n' % (t, s))
