Log Action
##########

Write logs on Tryton models.

How to use:

1.- Import **LogActionMixin** class and **write_log** function:

::

    from trytond.modules.log_action import LogActionMixin, write_log

2.- Create a model that derives from **LogActionMixin** and add the resouce field (Many2One)
to map the model you want to log, use *__name__* same as the model you want to log plus
*'.log_action'* appended to the end:

::

    class MyLog(LogActionMixin):
        "My Logs Model"
        __name__ = "my.model.log_action" 
        resource = fields.Many2One('my.model',
            'My Model', ondelete='CASCADE', select=True)

3.- Add the logs field (One2Many) to the model you want to log.

::

    logs = fields.One2Many ('my.model.log_action', 'resource', 'Logs')

4.- Use the **write_log** function wherever you want for any object which model has a logs
field defined.
If **write_log** finds *my.model.log_action* model then it writes messages using it,
otherwise an error is raised.

**write_log** has following parameters:

    - **action**: The message to log. It can be a model message id for gettext translation.
    - **obj**: Objects from which logs are written. Must be of same type.
    - ***args**: Optional key for searching porpuses.
    - ****variables**: Optional variables used by gettext for translation.

::

    write_log(action, objects, *key, **variables)

Example::

    # For this to work, tranlatable_message must be defined in ir.message
    # usually with message.xml for a module.

    write_log('test_module.tranlatable_message', [obj1, obj2], the_key, val1='one', val2='two')

5.- **Views:**: You can define your own views for the log model or use the views defined on *log_action* module:

::

    <field name="logs" colspan="4"
        view_ids="log_action.log_view_tree,log_action.log_view_form"/>


License
-------

See LICENSE

Copyright
---------

See COPYRIGHT


For more information please visit:

  * https://formateli.com/
  * http://www.tryton.org/
