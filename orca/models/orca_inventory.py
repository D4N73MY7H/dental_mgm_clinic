from odoo import api, models, fields


class Inventory(models.Model):
    _name = 'orca.inventory'
    _description = 'Medications'

    name = fields.Char(string='Name')
    quantity = fields.Integer(string='Quantity')
    image = fields.Image(string='Image')