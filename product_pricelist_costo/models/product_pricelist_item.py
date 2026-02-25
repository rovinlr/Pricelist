from odoo import api, fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    compute_price = fields.Selection(
        selection_add=[("costo", "Costo")],
        ondelete={"costo": "set default"},
    )

    kg_per_unit = fields.Float(string="Kg por unidad", digits="Product Unit of Measure")
    purchase_price_per_kg = fields.Float(string="Precio compra por kg", digits=(16, 3))

    labor_cost = fields.Float(string="Mano de obra", digits=(16, 3))
    carton_cost = fields.Float(string="Cartón", digits=(16, 3))
    materials_cost = fields.Float(string="Materiales", digits=(16, 3))
    overhead_cost = fields.Float(string="Costos indirectos", digits=(16, 3))
    packaging_cost_total_per_kg = fields.Float(
        string="Total costo embalaje por kg",
        digits=(16, 3),
        compute="_compute_cost_totals",
        store=True,
    )

    incoterms_cost = fields.Float(string="Incoterms", digits=(16, 3))
    total_cost_per_sale_unit = fields.Float(
        string="Total coste por unidad de venta",
        digits=(16, 3),
        compute="_compute_cost_totals",
        store=True,
    )
    margin_cost = fields.Float(string="Margen", digits=(16, 3))

    @api.depends(
        "purchase_price_per_kg",
        "labor_cost",
        "carton_cost",
        "materials_cost",
        "overhead_cost",
        "incoterms_cost",
        "kg_per_unit",
    )
    def _compute_cost_totals(self):
        for item in self:
            item.packaging_cost_total_per_kg = (
                item.labor_cost
                + item.carton_cost
                + item.materials_cost
                + item.overhead_cost
            )
            item.total_cost_per_sale_unit = (
                item.purchase_price_per_kg
                + item.packaging_cost_total_per_kg
                + item.incoterms_cost
            ) * item.kg_per_unit

    def _compute_costo_price(self):
        self.ensure_one()
        return self.total_cost_per_sale_unit + self.margin_cost
