def before_auth(oh3c_info):
    print 'Called before auth'

def after_auth_succ(oh3c_info):
    print 'Called after auth successfully'

def after_auth_fail(oh3c_info):
    print 'Called after auth failed'

def after_logoff(oh3c_info):
    print 'Called after logoff'
