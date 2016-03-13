# -*- coding:utf8 -*-
"""
Intro: config file for tool kit
Author: basicworld@163.com
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class EmailConfig(object):
    """
    account 'test@itprofessor.cn' is a test account for everyone using rabbit,
    so please do not change its pwd.
    just delete it and write your own account here
    """
    # input your config message here
    account = [
        {'usr': 'test@itprofessor.cn',  # change to your own account
         'pwd': 'Rabbit1234',  # change to your owen pwd
         'signature': u'Yours sincerely'
         },
        {'usr': '', 'pwd': '', 'signature': u''},
    ]
    subject = "Hello world from rabbit"
    body = """Hello my friend,
    You are seeing this content beacuse the message sender did not write \
    anything in email body. Please contact him/her to confirm this email if \
    you have any concern.

    Have a good day!
    """
    html_model = r"""<!DOCTYPE html>
    <head>
    <style type="text/css">
    a:link {color: #065FB9}
    a:visited {color: #065FB9}
    a:hover {color: #065FB9}
    a:active {color: #065FB9}
    </style>
    </head>
    <body>
    <!--body-->
    <br>
    <br>
    <div style="margin:0;
                padding:0;
                width:20%;
                height:1px;
                background-color:#CCCCCC;
                overflow:hidden;
                margin-top:15px;">
    </div>
    <p style="line-height:80%;font-size:80%;"><!--signature--></p>
    <p style="line-height:80%;font-size:80%;"><!--send_time--></p>
    <p style="line-height:80%;font-size:80%;color:#065FB9">Powered by
    <a href="https://github.com/basicworld/rabbit"> rabbit</a></p>
    <p></p>
    </body>
    </html>
    """


class Pop3SmtpImap(object):
    """
    config for email server
    highly recommand you to set ssl=True if ssl port exit
    """
    # default POP3_SMTP_IMAP
    server = {
        'model': {
        'imap': {'host': '', 'port': [], 'ssl': False},
        'smtp': {'host': '', 'port': [], 'ssl': False},
        'pop3': {'host': '', 'port': [], 'ssl': False},
        },

        '163': {
        'imap': {'host': 'imap.163.com', 'port': [993, 143], 'ssl': True},
        'smtp': {'host': 'smtp.163.com', 'port': [994, 25], 'ssl': True},
        'pop3': {'host': 'pop.163.com', 'port': [995, 110], 'ssl': True},
        },

        'itprofessor': {
        'imap': {'host': 'imap.mxhichina.com', 'port': [993, ], 'ssl': True},
        'smtp': {'host': 'smtp.mxhichina.com', 'port': [465, 25], 'ssl': True},
        'pop3': {'host': 'pop3.mxhichina.com', 'port': [995, ], 'ssl': True},
        },

        'adyolo': {
        'imap': {'host': '', 'port': [], 'ssl': True},
        'smtp': {'host': 'smtp.exmail.qq.com', 'port': [465], 'ssl': True},
        'pop3': {'host': 'pop.exmail.qq.com', 'port': [995], 'ssl': True},
        },

        '126': {
        'imap': {'host': 'imap.126.com', 'port': [993, 143], 'ssl': True},
        'smtp': {'host': 'smtp.126.com', 'port': [465, 994, 25], 'ssl': True},
        'pop3': {'host': 'pop.126.com', 'port': [995, 110], 'ssl': True},
        },

        'qq': {
        'imap': {'host': '', 'port': [], 'ssl': True},
        'smtp': {'host': 'smtp.qq.com', 'port': [465, 587], 'ssl': True},
        'pop3': {'host': 'pop.qq.com', 'port': [995], 'ssl': True},
        },
    }
