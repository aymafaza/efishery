# Copyright 2014 ACSONE SA/NV (http://acsone.eu).
# Copyright 2013 Akretion (http://www.akretion.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models, fields
from odoo.addons.base.models.ir_mail_server import MailDeliveryException

class BaseImportImport(models.TransientModel):
    _inherit = "base_import.import"

    def _import_one_chunk(self, model_name, attachment, options):
        result = super(BaseImportImport,self)._import_one_chunk(model_name, attachment, options)
        
        error_message = [
            message["message"]
            for message in result["messages"]
            if message["type"] == "error"
        ]
        
        # Send notification to user
        if not error_message:
            users = self.env.user
            if users:
                notification_ids = [(0, 0,
                                    {
                                        'res_partner_id': user.partner_id.id,
                                        'notification_type': 'inbox'
                                    }
                                    ) for user in users if users]

                # Send notification live chat
                self.env['mail.message'].create({
                    'message_type': "notification",
                    'body': "Import has been complete",
                    'subject': "Your Subject",
                    'partner_ids': [(4, user.partner_id.id) for user in users if users],
                    'model': self._name,
                    'res_id': self.id,
                    'notification_ids': notification_ids,
                    'author_id': self.env.user.partner_id and self.env.user.partner_id.id
                })

                # Send email notification
                template_id = self.env.ref('efishery_user.mail_template_complete_notification')
                template_id.sudo().send_mail(self.id,force_send=True)
                
        return result
