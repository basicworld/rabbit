# -*- coding:utf8 -*-
"""
Intro: config file for tool kit
Author: basicworld@163.com
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')

EMAIL_ACCOUNT = {
    'test@itprofessor.cn': {
        'usr': 'test@itprofessor.cn',  # change to your own account
        'pwd': 'Rabbit1234',  # change to your owen pwd
        'signature': u'Yours sincerely',
    },
    'usrname@example.com': {
        'usr': '',
        'pwd': '',
        'signature': u'',
    },
}

EMAIL_SUBJECT = "Hello world from rabbit"
EMAIL_BODY = """Hello my friend,
This is an illustrate email from <strong>rabbit</strong>--\
an easy to use tool kit for python coding. Click \
<a href="https://github.com/basicworld/rabbit">here</a>\
 for more information.
Thanks for your interest. Have a good day!
"""
EMAIL_HTML_MODEL = r"""<!DOCTYPE html>
<head><style type="text/css">
a:link {color: #065FB9}
a:visited {color: #065FB9}
a:hover {color: #065FB9}
a:active {color: #065FB9}
</style></head><body>
<!--body-->
<br><br><div style="margin:0;padding:0;width:20%;height:1px;
background-color:#CCCCCC;overflow:hidden;margin-top:15px;"></div>
<p style="line-height:80%;font-size:80%;"><!--signature--></p>
<p style="line-height:80%;font-size:80%;"><!--send_time--></p>
<p style="line-height:80%;font-size:80%;color:#065FB9">Powered by
<a href="https://github.com/basicworld/rabbit"> rabbit</a></p>
<p></p></body></html>
"""


# config for email server
# highly recommand you to set ssl=True if ssl port exit
# default POP3_SMTP_IMAP
EMAIL_SERVER = {
    'model': {
    'imap': {'host': '', 'port': [], },
    'smtp': {'host': '', 'port': [], },
    'pop3': {'host': '', 'port': [], },
    },

    '163.com': {
    'imap': {'host': 'imap.163.com', 'port': [993, ], },
    'smtp': {'host': 'smtp.163.com', 'port': [994, ], },
    'pop3': {'host': 'pop.163.com', 'port': [995, ], },
    },

    'itprofessor.cn': {
    'imap': {'host': 'imap.mxhichina.com', 'port': [993, ], },
    'smtp': {'host': 'smtp.mxhichina.com', 'port': [465, ], },
    'pop3': {'host': 'pop3.mxhichina.com', 'port': [995, ], },
    },

    'adyolo.com': {
    'imap': {'host': '', 'port': [], },
    'smtp': {'host': 'smtp.exmail.qq.com', 'port': [465], },
    'pop3': {'host': 'pop.exmail.qq.com', 'port': [995], },
    },

    '126.com': {
    'imap': {'host': 'imap.126.com', 'port': [993, ], },
    'smtp': {'host': 'smtp.126.com', 'port': [465, 994, ], },
    'pop3': {'host': 'pop.126.com', 'port': [995, ], },
    },

    'qq.com': {
    'imap': {'host': '', 'port': [], },
    'smtp': {'host': 'smtp.qq.com', 'port': [465, ], },
    'pop3': {'host': 'pop.qq.com', 'port': [995], },
    },
}
