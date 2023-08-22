{
    # a set of the information that will be display when someone brows our model from the app list
    'name': 'Restaurant',
    'author': 'Zein Khalil',
    'website': 'www.starrestaurant.com',
    'category': 'food',
    'sequence': -99,
    'summary': 'this model is for the Star Restaurant',
    # the class that we used from outside our class
    'depends': ['mail'],
    'data': [
        # we should write all our xml and security files here, and we considered that the setting security file first,
        # because it can be loaded faster than xml files
        'security/ir.model.access.csv', 'views/main_menu.xml', 'views/food.xml',
        'views/drink.xml', 'views/orders.xml', 'views/employees.xml'
    ],
    'application': True
}
