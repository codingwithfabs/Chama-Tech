from odoo import models, fields, api

class ChamaRole(models.Model):
    _name = 'chamatech.role'
    _description = 'Chama Member Roles'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Role Name", required=True, tracking=True)
    availability = fields.Selection([('available', 'Available'),
                                     ('filled', 'Filled')], string="Availability", default="available")