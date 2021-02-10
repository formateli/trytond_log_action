# This file is part of log_action module.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from trytond.model import ModelSQL, ModelView, fields
from trytond.transaction import Transaction
from datetime import datetime
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = [
        'LogActionMixin',
        'LogAction',
        'write_log'
    ]


class LogActionMixin(ModelSQL, ModelView):
    key = fields.Char('Key', readonly=True, select=True)
    action = fields.Char('Action', readonly=True)
    date = fields.DateTime('Date', readonly=True)
    user = fields.Many2One('res.user', 'User', readonly=True)
    variables = fields.Char('Variables', readonly=True)
    message = fields.Function(fields.Char('Message'), 'get_message')

    @classmethod
    def __setup__(cls):
        super(LogActionMixin, cls).__setup__()
        cls._order = [
                ('date', 'DESC'),
                ('id', 'DESC')
            ]

    @staticmethod
    def default_date():
        return datetime.now().replace(microsecond=0)

    @staticmethod
    def default_user():
        return Transaction().user

    @staticmethod
    def _get_variables(data):
        result = {}
        if not data:
            return result
        pairs = data.split(':||:')
        for pair in pairs:
            vals = pair.split(':|:')
            result[vals[0]] = vals[1]
        return result

    @staticmethod
    def _get_variables_str(variables):
        result = ''
        for key, value in variables.items():
            if result != '':
                result += ':||:'
            result += key + ':|:'
            result += str(value)
        if result == '':
            result = None
        return result

    def get_message(self, name=None):
        variables = self._get_variables(self.variables)
        return gettext(self.action, **variables)

    @staticmethod
    def _get_resource(obj):
        return obj.id

    @classmethod
    def log(cls, action, objs, key, model_name, **variables):
        user = Transaction().user
        variables_str = LogActionMixin._get_variables_str(variables)
        logs = []
        with Transaction().set_user(0):
            for obj in objs:
                # Ensure all objects are of same type
                if model_name != obj.__class__.__name__:
                    raise UserError(
                        gettext('log_action.objet_not_same_type',
                            model_1=model_name,
                            model_2=obj.__class__.__name__,
                        ))
                logs.append({
                    'key': key,
                    'resource': cls._get_resource(obj),
                    'action': action,
                    'variables': variables_str,
                    'user': user,
                })

            if logs:
                cls.create(logs)


class LogAction(LogActionMixin):
    "Log Action"
    __name__ = "log_action"


def write_log(action, objs, *args, **variables):
    if not objs or not action:
        return
    if not args:
        key = None
    else:
        key, = args

    model_name = objs[0].__class__.__name__
    pool = Pool()
    model = model_name + '.log_action'
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
    Log.log(action, objs, key, model_name, **variables)
