# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class ProductTemplateWithAttrDesc(models.Model):
#     _inherit = "product.template"

#     attribute_description = fields.Char(compute='_get_attribute_description')

#     def _get_attribute_description(self):
#         for template in self:
#             template.attribute_descripcion = "hola pirola"


# class pslabels(models.Model):
#     _name = 'pslabels.pslabels'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
