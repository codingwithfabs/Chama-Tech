from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ChamaRole(models.Model):
    _name = 'chamatech.role'
    _description = 'Chama Member Roles'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Role Name", required=True, tracking=True)

    max_slots = fields.Integer(string="Max Slots", default=1, required=True)
    
    # Selection field for availability status
    availability = fields.Selection([
        ('available', 'Available'),
        ('filled', 'Filled')
    ], string="Availability", compute='_compute_availability', store=True, tracking=True)

    # Relationships
    history_ids = fields.One2many('chamatech.role.history', 'role_id', string="History")

    @api.depends('max_slots')
    def _compute_availability(self):
        """Sets role to 'filled' if any member is assigned, otherwise 'available'"""
        for role in self:
            current_usage = self.env['chamatech.member'].search_count([('role_id', '=', role.id)])

            if current_usage >= role.max_slots:
                role.availability = 'filled'
            else:
                role.availability = 'available'


    @api.constrains('max_slots', 'name')
    def _check_role_structure(self):
        for role in self:
            current_usage = self.env['chamatech.member'].search_count([('role_id', '=', role.id)])
            if current_usage > role.max_slots:
                raise ValidationError(
                    f"Limit Reached: {role.name} only allows {role.max_slots} members."
                )