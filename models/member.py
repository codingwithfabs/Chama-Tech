from odoo import models, fields, api

class ChamaMember(models.Model):
    _name = 'chamatech.member'
    _description = 'Chama Group Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Member Name", required=True, tracking=True)
    phone = fields.Char(string="Mpesa Number", required=True, tracking=True)
    role_id = fields.Many2one('chamatech.role', string="Role", required=True, tracking=True)

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