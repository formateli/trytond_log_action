#This file is part of Tryton log_action module. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from . import log_action
from .log_action import LogActionMixin, write_log


def register():
    Pool.register(
        log_action.LogAction,
        module='log_action', type_='model')
