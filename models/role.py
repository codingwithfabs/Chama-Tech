from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ChamaRole(models.Model):
    _name = 'chamatech.role'
    _description = 'Chama Member Roles'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Role Name", required=True, tracking=True)
    availability = fields.Selection([('available', 'Available'),
                                     ('filled', 'Filled')], string="Availability", default="available")
    

    @api.constrains('name')
    def _check_role_limit(self):
        #Count existing roles
        role_count = self.env['chamatech.role'].search_count([])

        # If we are trying to create a record that exceeds 11
        if role_count > 11:
            raise ValidationError("Limit Reached: This platform supports a maximum of 11 roles/users including the Admin.")