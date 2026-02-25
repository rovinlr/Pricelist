{
    "name": "Product Pricelist Cost Method",
    "summary": "Adds a Cost-based computation method for pricelist rules.",
    "version": "19.0.1.0.0",
    "category": "Sales/Sales",
    "author": "Custom",
    "license": "LGPL-3",
    "depends": ["product"],
    "data": [
        "views/product_pricelist_item_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "product_pricelist_costo/static/src/scss/pricelist_item_dialog.scss",
        ],
    },
    "installable": True,
    "application": False,
}
