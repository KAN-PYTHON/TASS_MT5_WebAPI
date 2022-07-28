'''
import mt5_webapi_lib as mt5
account = '111511'
session = mt5.connect('webapi.educationvector.com', '1003', 'hf7jrf83er')

print('mod_account_right:', mt5.mod_account_rights('webapi.educationvector.com', account, session, 0))
print('close_position:', mt5.close_position('webapi.educationvector.com', '1003', 'hf7jrf83er', account, session))
print('pcount:', mt5.pcount('webapi.educationvector.com', account, session))
print('del_order', mt5.del_order('webapi.educationvector.com', account, session))
'''