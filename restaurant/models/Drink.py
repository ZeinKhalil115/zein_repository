from odoo import fields, api, models


class Drink(models.Model):
    _name = "drink"
    _description = "this database is for drink without alcohol"
    # the next line is for the chatter which include log and message section
    _inherit = ['mail.thread', 'mail.activity.mixin']
    drink_id = fields.Integer(string='Order Id', required=True, tracking=True)
    _sql_constraints = [
        # here we set a constraint for the employee ID to be unique, where the first parameter is constraint name and
        # the second one is SQL constraint expression and the third one for Constraint error message
        ('unique_drink_id', 'unique(drink_id)', 'Drink id must be unique.'),
    ]
    name = fields.Char(string='Drink name', required=True, tracking=True)
    ingredients = fields.Text(string='Ingredients drink', required=True, tracking=True)
    temp = fields.Selection([('cold', 'Cold'), ('hot', 'Hot')], string='Drink temp', required=True, tracking=True)
    price = fields.Float(string="Price", digits=(3, 2), required=True, tracking=True)
    extra = fields.Char(string="Extra", tracking=True)
    note = fields.Html(string='Note', tracking=True)
