import os

root_privilege = False

try:
    import pynotify
except ImportError:
    print 'Please install package python-notify'

pynotify.init ("OH3C")

def before_auth(OH3C_info):
    pass

def after_auth_succ(OH3C_info):
    msg = pynotify.Notification('OH3C', "Authenticate Successfully!")
    msg.show()

def after_auth_fail(OH3C_info):
    msg = pynotify.Notification('OH3C', "Authenticate Failed!")
    msg.show()

def after_logoff(OH3C_info):
    msg = pynotify.Notification('OH3C', "Logoff Successfully!")
    msg.show()
