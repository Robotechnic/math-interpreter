from .functions import functions
from .variables import variables

buildtin_symbol_table = functions
buildtin_symbol_table.update(variables)