Log Action
##########

Write logs on models.

This module can be used in two different ways:

1.- Creating global logs:

    - Import **write_log** function:
      ::
          from trytond.modules.log_action import write_log

    - Add the logs field to the model.
      ::
          logs = fields.One2Many ('log_action', 'resource', 'Logs')

    - Use the **write_log** function wherever you want,
      passing as arguments the message and objects affected:
      ::
          write_log ('Some insteresting log', sales)

    - **write_log** writes the message using *write_log* module.


2.- Using your own log model:

    - Import **LogActionMixin** class and **write_log** function:
      ::
          from trytond.modules.log_action import LogActionMixin, write_log

    - Create a model that derives from **LogActionMixin** and add the resouce field
      to map the model you want to log, use *__name__* same as the model to log plus
      *'.log_action'* appended to the end:
      ::
          class YourLog(LogActionMixin):
              "Your Logs"
              __name__ = "my.model.log_action" 
              resource = fields.Many2One('my.model',
                  'My Model', ondelete='CASCADE', select=True)

    - Add the logs field to the model using your log model.
      ::
          logs = fields.One2Many ('my.model.log_action', 'resource', 'Logs')

    - Use the **write_log** function wherever you want.
      If **write_log** finds *my.model.log_action* model then it writes messages using it,
      otherwise it writes messages using *log_action* model.

    - **Views:**: You can define your own views for the log model or use the views defined
      on *log_action* module:
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

  * http://www.formateli.com/
  * http://www.tryton.org/
