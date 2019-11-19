#This file is part of log_action Tryton module. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.pool import Pool
from trytond.model import ModelSQL, ModelView, fields
from trytond.transaction import Transaction
from datetime import datetime
from trytond.exceptions import UserError

__all__ = [
        'LogActionMixin',
        'LogAction',
        'write_log'
    ]


class LogActionMixin(ModelSQL, ModelView):
    key = fields.Char('Key', readonly=True)
    action = fields.Char('Action', readonly=True)
    date = fields.DateTime('Date', readonly=True)
    user = fields.Many2One('res.user', 'User', readonly=True)

    @classmethod
    def __setup__(cls):
        super(LogActionMixin, cls).__setup__()
        cls._order = [
                ('date', 'DESC'),
                ('id', 'DESC')
            ]

    @staticmethod
    def default_date():
        return datetime.now()

    @staticmethod
    def default_user():
        return Transaction().user

    @staticmethod
    def _get_resource(obj):
        return obj.id

    @classmethod
    def log(cls, action, objs, key):
        user = Transaction().user
        logs = []
        with Transaction().set_user(0):
            for obj in objs:
                logs.append({
                    'key': key,
                    'resource': cls._get_resource(obj),
                    'action': action,
                    'user': user
                })
        if logs:
            cls.create(logs)


class LogAction(LogActionMixin):
    "Log Action"
    __name__ = "log_action"


def write_log(action, objs, key=None):
    if not objs or not action:
        return
    pool = Pool()
    model = objs[0].__class__.__name__ + '.log_action'
    try:
        Log = pool.get(model)
    except KeyError:
        raise UserError(
            gettext('log_action.model_not_found',
                model=model,
            ))
    except Exception as e:
        raise UserError(
            gettext('log_action.log_action_error',
                error=str(e),
            ))
    Log.log(action, objs, key)
