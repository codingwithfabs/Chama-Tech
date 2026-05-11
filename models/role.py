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

    def _get_role_limits(self):
        """Centralized definition of Chama structure"""
        return {
            'Chairperson': 1,
            'Secretary': 1,
            'Treasurer': 1,
            'Vice Chairperson': 1,
            'Welfare Officer': 2,
            'Member': 4,
            'System Admin': 1,
        }

    @api.constrains('max_slots', 'name')
    def _check_role_structure(self):
        for role in self:
            current_usage = self.env['chamatech.member'].search_count([('role_id', '=', role.id)])
            if current_usage > role.max_slots:
                raise ValidationError(
                    f"Limit Reached: {role.name} only allows {role.max_slots} members."
                )

        # Dynamic Total System Check
        # We fetch the limit from Odoo's System Parameters (defaulting to 11)
        total_limit_str = self.env['ir.config_parameter'].sudo().get_param('chamatech.total_member_limit', '11')
        total_limit = int(total_limit_str)
        
        all_members_count = self.env['chamatech.member'].search_count([])
        if all_members_count > total_limit:
            raise ValidationError(
                f"The system is currently configured for a maximum of {total_limit} members."
            )