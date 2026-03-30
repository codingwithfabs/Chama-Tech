from odoo import models, fields, api


class ChamaTech(models.Model):
    _name = 'chamatech.chamatech'
    _description = 'chamatech'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one('res.partner', string="Member Name", required=True, tracking=True)
    amount = fields.Integer(string="Amount", required=True, tracking=True)
    # value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text(string="Decription", required=True, tracking=True)
    status = fields.Selection(selection=[("in_progress", "In Progress"),
                            ("goal_reached", "Goal Reached")],
                            string="Status", required=True, tracking=True)
    frequency = fields.Selection(selection=[("daily", "Daily"),
                                            ("weekly", "Weekly"),
                                            ("monthly", "Monthly")], string="Frequency", required=True, tracking=True)
    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100

