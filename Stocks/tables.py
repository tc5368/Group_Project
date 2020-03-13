from flask_table import Table, Col

class Results(Table):
    Stock_ID         = Col('Stock ID')
    Stock_Name       = Col('Stock Name')
    Current_Price    = Col('Current Price')
    Stock_Table      = Col('Stock Table', show='False')
