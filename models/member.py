from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ChamaMember(models.Model):
    _name = 'chamatech.member'
    _description = 'Chama Group Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Member Name", required=True, tracking=True)
    phone = fields.Char(string="Mpesa Number", required=True, tracking=True)
    role_id = fields.Many2one('chamatech.role', string="Role", required=True, tracking=True)

    @api.constrains('role_id')
    def _check_unique_role_assignment(self):
        for member in self:
            #Search for other members with the same role
            duplicate = self.search([
                ('role_id', '=', member.role_id.id),
                ('id', '!=', member.id)
            ])
            if duplicate:
                raise ValidationError(f"The role '{member.role_id.name}' is already assigned to {duplicate[0].name}.")