from odoo import fields, api, models


class Employees(models.Model):
    _name = "employees"
    _description = 'here you can found the employees in the restaurant'
    # the next line is for the chatter which include log and message section
    _inherit = ['mail.thread', 'mail.activity.mixin']
    user_id = fields.Many2one('res.users', string='Related User', tracking=True,required=True)
    employee_id = fields.Integer(string='ID', required=True)
    _sql_constraints = [
        # here we set a constraint for the employee ID to be unique, where the first parameter is constraint name and
        # the second one is SQL constraint expression and the third one for Constraint error message
        ('unique_employee_id', 'unique(employee_id)', 'Employee ID must be unique.'),
    ]
    name = fields.Char(string='name of the employee', required=True)
    job_title = fields.Char(string='job of employee', required=True)
    phone_number = fields.Char(string='phone number', required=True)
    _sql_constraints = [
        # here we set a constraint for the employee ID to be unique, where the first parameter is constraint name and
        # the second one is SQL constraint expression and the third one for Constraint error message
        ('unique_employee_phone', 'unique(phone_number)', 'Employee phone must be unique.'),
    ]
    salary = fields.Integer(string='salary of employee', required=True)
    email = fields.Text(string='employee email', help='click to send an E-mail')
    # to rat the employee
    rating = fields.Selection([
        ('0', 'low'),
        ('1', 'good'),
        ('2', 'very good'),
        ('3', 'excellent')], string="rating")
    notes = fields.Text(string='any notes on this employee !')

    # odoo will automatically save all the changes
    def save_button(self):
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'employee information has been saved successfully',
                'type': 'rainbow_man',
            }
        }
