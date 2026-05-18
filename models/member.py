from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ChamaMember(models.Model):
    _name = 'chamatech.member'
    _description = 'Chama Group Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.users', string="Contact", required=True, tracking=True, ondelete='restrict')

    name = fields.Char(related='partner_id.name', required=True, tracking=True, store=True, readonly=True)
    phone = fields.Char(string="Mpesa Number", required=True, tracking=True)
    role_id = fields.Many2one('chamatech.role', string="Role", required=True, tracking=True)
    date_joined = fields.Date(string="Date Joined", default=fields.Date.context_today, required=True, tracking=True)
    date_left = fields.Date(string="Date Left", tracking=True, help="The date this member officially left the Chama.")

    # Link to the list of contributions
    contribution_ids = fields.One2many('chamatech.mycontribution', 'member_id', string="Contributions")

    # Total sum field
    total_contributions = fields.Float(string="Total Contributions", compute='_compute_total_contributions', store=True, tracking=True)

    history_ids = fields.One2many('chamatech.role.history', 'member_id', string="Role History")

    # Logic to prevent contributions after they leave
    active = fields.Boolean(default=True)

    @api.constrains('role_id', 'active')
    def _check_unique_role_assignment(self):
        for member in self:
            if not member.active:
                continue

            # Search for OTHER active members with this same role
            duplicate = self.search([
                ('role_id', '=', member.role_id.id),
                ('active', '=', True),
                ('id', '!=', member.id) # Critical: Don't count yourself!
            ])

            # Check against the dynamic limit we set in the Role model
            if duplicate and len(duplicate) >= member.role_id.max_slots:
                raise ValidationError(f"The role '{member.role_id.name}' is full.")

    @api.depends('contribution_ids.amount', 'contribution_ids.state')
    def _compute_total_contributions(self):
        for member in self:
            # We explicity loop to avoid any recordset caching issues
            total = 0.0
            for line in member.contribution_ids:
                if line.state == 'validated':
                    total += line.amount
            member.total_contributions = total

    @api.model_create_multi
    def create(self, vals_list):
        # 1. Create the members first
        members = super(ChamaMember, self).create(vals_list)
        
        # 2. Log the initial role assignment in history
        for member in members:
            if member.role_id:
                self.env['chamatech.role.history'].create({
                    'role_id': member.role_id.id,
                    'member_id': member.id,
                    'date_assigned': fields.Date.context_today(member),
                })
        return members

    def write(self, vals):
        # 1. Standard save to update the member record first
        res = super(ChamaMember, self).write(vals)

        # 2. If the role was changed, create the new history record
        # The history model's 'create' will now automatically handle closing the old one
        if 'role_id' in vals:
            for member in self:
                self.env['chamatech.role.history'].create({
                    'role_id': member.role_id.id,
                    'member_id': member.id,
                    'date_assigned': fields.Date.context_today(self),
                })
        return res
    
    @api.onchange('active')
    def _onchange_active(self):
        if not self.active:
            # If they are being deactivated, set the date to today
            self.date_left = fields.Date.context_today(self)
        else:
            # If they are being reactivated, clear the date
            self.date_left = False
