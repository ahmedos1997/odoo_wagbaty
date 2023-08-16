# -*- coding: utf-8 -*-

from odoo import models, fields, api


class test_field_module(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'
    _description = 'test module'
    name_amount = fields.Char('اسم العنصر')
    product_weight = fields.Integer('وزن الوجبة بالجرام')
    calories = fields.Integer('عدد السعرات الحرارية', compute='_calcamount', store=True)
    calories_calc = fields.Integer('عدد السعرات الحرارية لكل 100 جرام')
    expiry_date = fields.Date('تاريخ إنتهاء الصلاحية')
    @api.depends('calories_calc','product_weight')
    def _calcamount(self):
        for record in self:
            record.calories = record.product_weight * record.calories_calc



class partners_meal(models.Model):
    _name ='partners.meal'
    _description = 'meal for all group'
    meal_name = fields.Selection([
        ('breakfast','وجبات الفطور'),
        ('lunch','وجبات الغداء'),
        ('dinner','وجبات العشاء')
    ], string='اسم الوجبة')

    partners_id = fields.Many2one('res.partner',string='اسم العميل')

    meal_datetime = fields.Datetime('وقت الوجبة')
    meal_note = fields.Text('الملاحظات')
    item_id = fields.One2many('partners.meal.item','meal_id') # هذا الحقل لربط هذا الكلاس بي الكلاس التالي

    total_price= fields.Float(string='اجمالي سعر الوجبة',compute='_calctotalprice',store=True)
    @api.depends('item_id.meal_item_price')
    def _calctotalprice(self):
        for record in self:
            currentprice = 0
            for i in record.item_id:
                currentprice = currentprice + i.meal_item_price
            record.total_price = currentprice

class partners_meal_item(models.Model):
    _name = 'partners.meal.item'
    _description = 'partners meal item'

    product_id = fields.Many2one('product.template','عنصر الوجبة')
    meal_id = fields.Many2one('partners.meal') # قمنا بربط الكلاس السابق بهذا الحقل
    meal_num = fields.Integer('عدد عناصر الوجبة')
    meal_price = fields.Float(related='product_id.list_price',string='سعر الوجبة',readonly=False,store=False)
    calories = fields.Integer(related='product_id.calories', string='عدد السعرات الحرارية')
    weight = fields.Integer(related='product_id.product_weight', string='وزن الوجبة')
    meal_item_price = fields.Float(string='سعر عناصر الوجبة',compute='_calcprice', store=True)
    @api.depends('meal_num','meal_price')
    def _calcprice(self):
        for record in self:
            record.meal_item_price = record.meal_num * record.meal_price

