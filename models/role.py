from odoo import models, fields, api

class ChamaRole(models.Model):
    _name = 'chamatech.role'
    _description = 'Chama Member Roles'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Role Name", required=True, tracking=True)
    availability = fields.Selection([
        ('available', 'Available'),
        ('filled', 'Filled')
    ], string="Availability", compute='_compute_availability', store=True, tracking=True)
    

    history_ids = fields.One2many('chamatech.role.history', 'role_id', string="History")
    member_ids = fields.One2many('chamatech.member', 'role_id', string="Current Members")

    @api.depends('member_ids')
    def _compute_availability(self):
        for role in self:
            if role.member_ids:
                role.availability = 'filled'
            else:
                role.availability = 'available'