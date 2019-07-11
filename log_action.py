#This file is part of log_action Tryton module. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.pool import Pool
from trytond.model import fields
from trytond.transaction import Transaction
from trytond.ir.resource import ResourceMixin
from datetime import datetime

__all__ = [
        'LogAction',
        'write_log'
    ]


class LogAction(ResourceMixin):
    "Log Action"
    __name__ = "log_action" 

    action = fields.Char('Action', readonly=True)
    date = fields.DateTime('Date', readonly=True)
    user = fields.Many2One('res.user', 'User', readonly=True)

    @staticmethod
    def default_date():
        return datetime.now()

    @staticmethod
    def default_user():
        return Transaction().user

    @classmethod
    def log(cls, action, objs):
        user = Transaction().user
        with Transaction().set_user(0):
            for obj in objs:
                cls.create([{
                    'resource': obj.__class__.__name__ + ',' + str(obj.id),
                    'action': action,
                    'user': user
                }])


def write_log(action, objs):
    Log = Pool().get('log_action')
    Log.log(action, objs)
