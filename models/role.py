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
            if role.member_ids:
                role.availability = 'filled'
            else:
                role.availability = 'available'

    @api.constrains('name')
    def _check_role_limit(self):
        """Strictly limits the number of roles/users to 11"""
        # We count all records in this model
        role_count = self.env['chamatech.role'].search_count([])
        
        # If the count exceeds 11, prevent saving
        if role_count > 11:
            raise ValidationError(
                "System Limit: This platform is configured for a maximum of 11 roles/users "
                "including the Administrator. Please delete an existing role before adding a new one."
            )