from odoo import models, fields, api

class ChamaMember(models.Model):
    _name = 'chamatech.member'
    _description = 'Chama Group Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.partner', string="Contact", required=True, tracking=True, ondelete='restrict')

    name = fields.Char(related='partner_id.name', required=True, tracking=True, store=True, readonly=True)
    phone = fields.Char(string="Mpesa Number", required=True, tracking=True)
    role_id = fields.Many2one('chamatech.role', string="Role", required=True, tracking=True)
    date_joined = fields.Date(string="Date Joined", default=fields.Date.context_today, required=True, tracking=True)
    date_left = fields.Date(string="Date Left", tracking=True, help="The date this member officially left the Chama.")

    # Logic to prevent contributions after they leave
    active = fields.Boolean(default=True)

    # Link to the list of contributions
    contribution_ids = fields.One2many('chamatech.contribution', 'member_id', string="Contributions")

    # Total sum field
    total_contributions = fields.Float(string="Total Contributions", compute='_compute_total_contributions', store=True, tracking=True)

    @api.depends('contribution_ids.amount')
    def _compute_total_contributions(self):
        for member in self:
            confirmed = member.contribution_ids.filtered(lambda c: c.state == 'confirmed')
            #Sum up all the amounts in the contribution_ids list
            member.total_contributions = sum(member.contribution_ids.mapped('amount'))

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
                })
        return members

    def write(self, vals):
        # 1. Standard save
        res = super(ChamaMember, self).write(vals)
    
        # 2. Log history ONLY if the role actually changed
        if 'role_id' in vals:
            for member in self:
                if member.role_id:
                    self.env['chamatech.role.history'].create({
                        'role_id': member.role_id.id,
                        'member_id': member.id,
                        'date_assigned': fields.Date.context_today(member),
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
