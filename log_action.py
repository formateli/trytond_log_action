#This file is part of log_action Tryton module. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from trytond.model import fields
from trytond.transaction import Transaction
from trytond.ir.resource import ResourceMixin
from datetime import datetime

__all__ = [
        'LogAction',
    ]


class LogAction(ResourceMixin):
    "Log Action"
    __name__ = "log_action" 

    action = fields.Char('Action')
    date = fields.DateTime('Date')
    user = fields.Many2One('res.user', 'User', readonly=True)

    @staticmethod
    def default_date():
        return datetime.now()

    @staticmethod
    def default_user():
        return Transaction().user
