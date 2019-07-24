#This file is part of log_action Tryton module. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.pool import Pool
from trytond.model import ModelSQL, ModelView, fields
from trytond.transaction import Transaction
from datetime import datetime

__all__ = [
        'LogActionMixin',
        'LogAction',
        'write_log'
    ]


class LogActionMixin(ModelSQL, ModelView):
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
    def log(cls, action, objs):
        user = Transaction().user
        logs = []
        with Transaction().set_user(0):
            for obj in objs:
                logs.append({
                    'resource': cls._get_resource(obj),
                    'action': action,
                    'user': user
                })
        if logs:
            cls.create(logs)


class LogAction(LogActionMixin):
    "Log Action"
    __name__ = "log_action" 

    resource = fields.Reference('Resource', selection='get_models',
        required=True, select=True)

    @staticmethod
    def get_models():
        pool = Pool()
        Model = pool.get('ir.model')
        ModelAccess = pool.get('ir.model.access')
        models = Model.search([])
        access = ModelAccess.get_access([m.model for m in models])
        return [(m.model, m.name) for m in models if access[m.model]['read']]

    @classmethod
    def check_access(cls, ids, mode='read'):
        pool = Pool()
        ModelAccess = pool.get('ir.model.access')
        if ((Transaction().user == 0)
                or not Transaction().context.get('_check_access')):
            return
        model_names = set()
        with Transaction().set_context(_check_access=False):
            for record in cls.browse(ids):
                if record.resource:
                    model_names.add(str(record.resource).split(',')[0])
        for model_name in model_names:
            checks = cls._convert_check_access(model_name, mode)
            for model, check_mode in checks:
                ModelAccess.check(model, mode=check_mode)

    @classmethod
    def _convert_check_access(cls, model, mode):
        return [
            (model, {'create': 'write', 'delete': 'write'}.get(mode, mode))]

    @classmethod
    def read(cls, ids, fields_names):
        cls.check_access(ids, mode='read')
        return super(LogAction, cls).read(ids, fields_names)

    @classmethod
    def delete(cls, records):
        cls.check_access([a.id for a in records], mode='delete')
        super(LogAction, cls).delete(records)

    @classmethod
    def write(cls, records, values, *args):
        all_records = []
        actions = iter((records, values) + args)
        for other_records, _ in zip(actions, actions):
            all_records += other_records
        cls.check_access([a.id for a in all_records], mode='write')
        super(LogAction, cls).write(records, values, *args)
        cls.check_access(all_records, mode='write')

    @classmethod
    def create(cls, vlist):
        records = super(LogAction, cls).create(vlist)
        cls.check_access([r.id for r in records], mode='create')
        return records

    @staticmethod
    def _get_resource(obj):
        return obj.__class__.__name__ + ',' + str(obj.id)


def write_log(action, objs):
    if not objs:
        return
    pool = Pool()
    model = objs[0].__class__.__name__
    try:
        # Try to use model own logs
        Log = pool.get(model + '.log_action')
    except KeyError:
        # Use global logs
        Log = pool.get('log_action')
    Log.log(action, objs)
