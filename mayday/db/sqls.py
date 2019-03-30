MATCHING_TICKETS_KEYS = ['id', 'category', 'status', 'date', 'price_id', 'quantity',
                         'section', 'row', 'remarks', 'user_id', 'username', 'updated_at']
MATCHING_TICKETS = '''
SELECT src.id, src.category, src.status, src.`date`, src.price_id, src.quantity, src.section, src.row, src.remarks, src.user_id, src.username, src.updated_at FROM 
(SELECT id, category, status, `date`, price_id, quantity, section, row, remarks, updated_at, user_id, username, wish_dates, wish_price_ids, wish_quantities FROM tickets 
  WHERE status = 1 and category = 2 and is_banned = 0 and user_id != {user_id} ) as src,
(SELECT id, `date`, price_id, quantity, wish_dates, wish_price_ids, wish_quantities FROM tickets 
  WHERE user_id = {user_id} and status = 1 and category = 2 ) wish 
 WHERE find_in_set(src.date, wish.wish_dates) 
 and find_in_set(src.price_id, wish.wish_price_ids)
 and find_in_set(src.quantity, wish.wish_quantities)
 and find_in_set(wish.date, src.wish_dates) 
 and find_in_set(wish.price_id, src.wish_price_ids)
 and find_in_set(wish.quantity, src.wish_quantities)
 ORDER BY updated_at ASC
'''

SEARCH_BY_CONDITIONS_KEYS = ['id', 'category', 'status', 'date', 'price_id',
                             'quantity', 'section', 'row', 'wish_dates', 'wish_price_ids',
                             'wish_quantities', 'remarks', 'user_id', 'username',  'updated_at']

SEARCH_BY_CONDITIONS = '''SELECT id, category, status, `date`, price_id, quantity, section, row, wish_dates, wish_price_ids, wish_quantities, remarks, updated_at, user_id, username
FROM tickets WHERE is_banned = 0 AND {} ORDER BY id ASC;
'''
INSERT_TICKET = '''INSERT tickets (category, date, price_id, quantity, section, row, wish_dates, wish_price_ids, wish_quantities, user_id, username, updated_at)
VALUES ({category},{date},{price_id},{quantity},\'{section}\',\'{row}\', \'{wish_dates}\', \'{wish_price_ids}\', \'{wish_quantities}\', {user_id},\'{username}\', {updated_at});         
'''
UPDATE_TICKET = '''UPDATE tickets SET {} WHERE id = {};'''

TICKET_DISTRIBUTION_KEYS = ['category', 'date', 'price_id', 'amount']

TICKET_DISTRIBUTION = '''SELECT category, `date`, price_id, count(1) as amount FROM tickets
WHERE status = 1 GROUP BY category, `date`, price_id ORDER BY category, `date`, price_id ASC;
'''

STATUS_DISRIBUTION_KEYS = ['status', 'amount']

STATUS_DISRIBUTION = 'SELECT status, count(1) as amount from tickets GROUP BY status ORDER BY status ASC;'
