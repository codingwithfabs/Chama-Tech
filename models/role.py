from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ChamaRole(models.Model):
    _name = 'chamatech.role'
    _description = 'Chama Member Roles'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Role Name", required=True, tracking=True)
    
    # Selection field for availability status
    availability = fields.Selection([
        ('available', 'Available'),
        ('filled', 'Filled')
    ], string="Availability", compute='_compute_availability', store=True, tracking=True)

    # Relationships
    history_ids = fields.One2many('chamatech.role.history', 'role_id', string="History")
    member_ids = fields.One2many('chamatech.member', 'role_id', string="Current Members")

    @api.depends('member_ids')
    def _compute_availability(self):
        """Sets role to 'filled' if any member is assigned, otherwise 'available'"""
        for role in self:
            # For roles with more than 1 slot (Welfare/Standard), 
            # we check if it has reached its specific capacity
            limits = self._get_role_limits()
            max_slots = limits.get(role.name, 1)
            
            if len(role.member_ids) >= max_slots:
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

    @api.constrains('member_ids', 'name')
    def _check_role_structure(self):
        """Validates the specific quota for each role and the total limit of 11"""
        limits = self._get_role_limits()
        
        # 1. Check individual role quotas
        for role in self:
            if role.name in limits:
                current_usage = len(role.member_ids)
                if current_usage > limits[role.name]:
                    raise ValidationError(
                        f"Limit Reached: The role '{role.name}' only allows {limits[role.name]} member(s). "
                        f"You currently have {current_usage} assigned."
                    )

        # 2. Total System Check (Across all roles)
        all_members_count = self.env['chamatech.member'].search_count([])
        if all_members_count > 11:
            raise ValidationError(
                "Total System Limit: The Chama is limited to 11 total members across all roles."
            )