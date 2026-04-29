from odoo import models, fields, api

class ChamaMember(models.Model):
    _name = 'chamatech.member'
    _description = 'Chama Group Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Member Name", required=True, tracking=True)
    phone = fields.Char(string="Mpesa Number", required=True, tracking=True)
    role_id = fields.Many2one('chamatech.role', string="Role", required=True, tracking=True)

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
                    'date_assigned': fields.Date.context_today(member),
                })
        return members

    def write(self, vals):
        # 1. If the role is changing, 'close' the old history record first
        if 'role_id' in vals:
            for member in self:
                # Find the current active role history (no resignation date set)
                old_history = self.env['chamatech.role.history'].search([
                ('member_id', '=', member.id),
                ('role_id', '=', member.role_id.id),
                ('date_resigned', '=', False)
                ], limit=1)

                if old_history:
                    old_history.write({'date_resigned': fields.Date.context_today(member)})

        # 2. Standard save to update the actual member record
        res = super(ChamaMember, self).write(vals)

        # 3. Log the NEW history if the role changes
        if 'role_id' in vals:
            for member in self:
                if member.role_id:
                    self.env['chamatech.role.history'].create({
                        'role_id': member.role_id.id,
                        'member_id': member.id,
                        'date_assigned': fields.Date.context_today(member),
                    })
        return res