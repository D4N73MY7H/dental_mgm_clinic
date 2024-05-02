from odoo import api, fields, models, _
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Patient(models.Model):
    _name = 'orca.patient'
    _description = 'Patient Details'

    id_num = fields.Char(string='Patient ID', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    name = fields.Char(string='Name')
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=False)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')])
    age_group = fields.Selection([
        ('kids', 'Kids (0-15)'),
        ('young_adults', 'Young Adults (15-18)'),
        ('adults', 'Adults (18-50)'),
        ('mid_age', 'Mid Age (50-70)'),
        ('old', 'Old (70+)')
    ], string='Age Group', compute='_compute_age_group', store=True)
    phone_number = fields.Char(string='Phone Number')
    image = fields.Image(string='Image')
    email = fields.Char(string='E-mail')
    address = fields.Char(string='Address')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('uniq_patient_phone-number', 'unique(phone_number)', 'Patient Phone Number must be unique!'),
        ('uniq_patient_email', 'unique(email)', 'Email must be unique!')
    ]

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = datetime.today().date()
        for patient in self:
            if patient.date_of_birth:
                dob = fields.Date.from_string(patient.date_of_birth)
                age = relativedelta(today, dob).years
                patient.age = age
            else:
                patient.age = 0

    @api.depends('age')
    def _compute_age_group(self):
        for record in self:
            if record.age <= 15:
                record.age_group = 'kids'
            elif 15 < record.age <= 18:
                record.age_group = 'young_adults'
            elif 18 < record.age <= 50:
                record.age_group = 'adults'
            elif 50 < record.age <= 70:
                record.age_group = 'mid_age'
            else:
                record.age_group = 'old'

    @api.model
    def create(self, vals):
        vals['id_num'] = self.env['ir.sequence'].next_by_code('orca.patient')
        return super(Patient, self).create(vals)

