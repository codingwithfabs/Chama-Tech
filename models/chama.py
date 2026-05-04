from odoo import models, fields, api


class ChamaTech(models.Model):
    _name = 'chamatech.chamatech'
    _description = 'chamatech'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "amount desc"

    name = fields.Many2one('res.partner', string="Member Name", required=True, tracking=True)
    amount = fields.Integer(string="Amount", required=True, tracking=True)
    target_amount = fields.Integer(string="Goal Target", required=True, tracking=True, default=1000)
    description = fields.Text(string="Decription", required=True, tracking=True)
    status = fields.Selection(selection=[("in_progress", "In Progress"),
                            ("goal_reached", "Goal Reached")],
                            string="Status", required=True, tracking=True, compute="_compute_status", store=True)
    frequency = fields.Selection(selection=[("daily", "Daily"),
                                            ("weekly", "Weekly"),
                                            ("monthly", "Monthly")], string="Frequency", required=True, tracking=True)

    date = fields.Datetime(string="Date of Contribution", required=True, tracking=True, default=fields.Date.today)
    
    @api.depends('amount', 'target_amount')
    def _compute_status(self):
        for record in self:
            if record.amount >= record.target_amount:
                record.status = "goal_reached"
            else:
                record.status = "in_progress"