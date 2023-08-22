from odoo import fields, api, models, http
from odoo.exceptions import ValidationError


class Orders(models.Model):
    _name = 'orders'
    _description = 'this page is for orders '
    # the next line is for the chatter which include log and message section
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # (record name) here we do not have name field so when we add new record the name will be like the field order_id
    # but after adding this field, the name of the record will be the same name as it
    _rec_name = 'order_id'
    order_id = fields.Integer(string='Order Id', index=True, readonly=True)
    cacher_id = fields.Integer(string='Cacher id ', related='cacher_name.employee_id')
    # in the next line we connect this field with the employee class(from the first parameter) and select that the
    # job_title field in the employee class should be casher or Cashier
    cacher_name = fields.Many2one('employees', string='Cashier name', required=True,
                                  domain=[('job_title', '=', ['Cashier', 'cashier'])], tracking=True)
    order_date = fields.Datetime(string='Order Date', default=fields.Datetime.now, readonly=True)
    customer_name = fields.Char(string="Customer name", required=True, tracking=True)
    # to store the details of the many2many in postgres we add
    # the second(table name),third(column) and fourth(column) parameter
    order_food_item = fields.Many2many(
        'food',
        'order_food_tag_rel',
        'order_id',
        'food_id',
        string="Food Order",
        tracking=True
    )
    order_drink_item = fields.Many2many(
        'drink',
        'order_drink_tag_rel',
        'order_id',
        'drink_id',
        string="Drink order", tracking=True)
    table_number = fields.Integer(string='Table number', tracking=True)
    special_instructions = fields.Html(string="Special instructions", default='no', tracking=True)
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_order', 'In Order'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string="Status", default='draft', required=True)
    cacher_name_for_avatar = fields.Many2one('res.users', string='Cashier name', related='cacher_name.user_id')

    @api.constrains('order_food_item', 'order_drink_item')
    def _check_food_or_drink_items(self):
        for order in self:
            if not order.order_food_item and not order.order_drink_item:
                raise ValidationError("Please select at least one food or drink item.")

    # here we define a method in order to calculate the total price of the order and put it in the total_price field

    @api.depends('order_food_item', 'order_drink_item')
    def _compute_total_price(self):
        for order in self:
            food_price = sum(order.order_food_item.mapped('price'))
            drink_price = sum(order.order_drink_item.mapped('price'))
            order.total_price = food_price + drink_price

    # a method to check if all records are deleted, then restart the order_id from
    @api.model
    def check_empty_records(self):
        if not self.search_count([]):
            sequence = self.env['ir.sequence'].search([('code', '=', 'orders')])
            if sequence:
                sequence.number_next_actual = 1

    # the unlink method is used to delete records from a model. It is automatically called when you delete a record,
    # and here we override it to call the previous method every time a delete action happen to ensure that when the
    # all records are deleted, the order_id will start again from zero
    def unlink(self):
        super().unlink()
        self.check_empty_records()

    # Define the method that will be triggered when cancel button is clicked, and mark the order as cancel.
    def cancel_button(self):
        self.state = 'cancel'
        self.total_price = self.total_price * 0.4

    # Define the method that will be triggered when save button is clicked. P.S: odoo will automatically save all the
    # changes, but here I write the necessary changes because I do not want the user to do it.
    def save_button(self):
        self.order_id = self.env['ir.sequence'].next_by_code('orders')
        self.state = 'in_order'
        