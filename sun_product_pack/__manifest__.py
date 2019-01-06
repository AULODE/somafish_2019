{
  "name"                 :  "Product Pack",
  "summary"              :  "Combine two or more products together in order to create a bundle product.",
  "category"             :  "Sales Management",
  "version"              :  "11.0.1",
  "sequence"             :  1,
  "author"               :  "Kiran Kantesariya",
  "depends"              :  [
                             'sale_stock',
                            ],
  "data"                 :  [
                             'wizard/product_pack_wizard.xml',
                             'views/sun_product_pack.xml',
                             'security/ir.model.access.csv',
                            ],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
}