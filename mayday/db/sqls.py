MATCHING_TICKETS_KEYS = ['id', 'category_id', 'status_id', 'date', 'price_id', 'quantity',
                         'section', 'row', 'remarks', 'user_id', 'username', 'updated_at']
MATCHING_TICKETS = '''
SELECT src.id, src.category_id, src.status_id, src.`date`, src.price_id, src.quantity, src.section, src.row, src.remarks, src.user_id, src.username, src.updated_at FROM 
(SELECT id, category_id, status_id, `date`, price_id, quantity, section, row, remarks, updated_at, user_id, username, wish_date, wish_price_id, wish_quantity FROM tickets 
  WHERE status_id = 1 and category_id = 2 and is_banned = 0 and user_id != {user_id} and year = {year}) as src,
(SELECT id, `date`, price_id, quantity, wish_date, wish_price_id, wish_quantity FROM tickets 
  WHERE user_id = {user_id} and status_id = 1 and category_id = 2 and year = {year}) wish 
 WHERE find_in_set(src.date, wish.wish_date) 
 and find_in_set(src.price_id, wish.wish_price_id)
 and find_in_set(src.quantity, wish.wish_quantity)
 and find_in_set(wish.date, src.wish_date) 
 and find_in_set(wish.price_id, src.wish_price_id)
 and find_in_set(wish.quantity, src.wish_quantity)
 ORDER BY updated_at ASC
'''

SEARCH_BY_CONDITIONS_KEYS = ['id', 'category_id', 'status_id', 'date', 'price_id',
                             'quantity', 'section', 'row', 'wish_date', 'wish_price_id',
                             'wish_quantity', 'remarks', 'user_id', 'username',  'updated_at']

SEARCH_BY_CONDITIONS = '''SELECT id, category_id, status_id, `date`, price_id, quantity, section, row, wish_date, wish_price_id, wish_quantity, remarks, updated_at, user_id, username
FROM tickets WHERE is_banned = 0 AND {} ORDER BY id ASC;
'''
INSERT_TICKET = '''INSERT tickets (category_id, date, price_id, quantity, section, row, wish_date, wish_price_id, wish_quantity, user_id, username, updated_at)
VALUES ({category_id},{date},{price_id},{quantity},\'{section}\',\'{row}\', \'{wish_date}\', \'{wish_price_id}\', \'{wish_quantity}\', {user_id},\'{username}\', {updated_at});         
'''
UPDATE_TICKET = '''UPDATE tickets SET {} WHERE id = {};'''

TICKET_DISTRIBUTION_KEYS = ['category_id', 'date', 'price_id', 'amount']

TICKET_DISTRIBUTION = '''SELECT category_id, `date`, price_id, count(1) as amount FROM tickets
WHERE status_id = 1 GROUP BY category_id, `date`, price_id ORDER BY category_id, `date`, price_id ASC;
'''

STATUS_DISRIBUTION_KEYS = ['status_id', 'amount']

STATUS_DISRIBUTION = 'SELECT status_id, count(1) as amount from tickets GROUP BY status_id ORDER BY status_id ASC;'
