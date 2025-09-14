-- Banks
INSERT INTO bank (name, account_number_validity_pattern, cashier_check_validity_pattern)
VALUES
  ('Bank A', 'BNKAA[0-9]{4}', 'BNKAA[0-9]{8}'),
  ('Bank B', 'BNKB[0-9]{4}', 'BNKB[0-9]{8}')
ON CONFLICT (name) DO NOTHING;

-- Customers
INSERT INTO customer (full_name, email) VALUES
  ('Louis Charollais',  'louis.charollais@email.com'),
  ('John Doe',   'john.doe@email.com'),
  ('Jane Doe', 'jane.doe@email.com')
ON CONFLICT (email) DO NOTHING;

-- Accounts
WITH b AS (SELECT id, name FROM bank),
     c AS (SELECT id, email FROM customer)
INSERT INTO account (customer_id, bank_id, account_number, balance)
VALUES
  ((SELECT id FROM c WHERE email='louis.charollais@email.com'),
   (SELECT id FROM b WHERE name='Bank A'),
   'BNKA0123', 12500.00),

  ((SELECT id FROM c WHERE email='john.doe@email.com'),
   (SELECT id FROM b WHERE name='Bank B'),
   'BNKB5874',  9800.75),

  ((SELECT id FROM c WHERE email='jane.doe@email.com'),
   (SELECT id FROM b WHERE name='Bank A'),
   'BNKA5726', 1500.00),

  ((SELECT id FROM c WHERE email='jane.doe@email.com'),
   (SELECT id FROM b WHERE name='Bank B'),
   'BNKB5720',  2500.00)
ON CONFLICT (account_number) DO NOTHING;

-- Transactions
INSERT INTO banking_transaction (account_id, transaction_type, amount)
SELECT a.id, x.transaction_type, x.amount
FROM (VALUES
  ('BNKA0123', 'deposit',    1000.00),
  ('BNKA0123', 'withdrawal',  200.00),
  ('BNKA0123', 'deposit',     500.00),
  ('BNKB5874', 'deposit',    2000.00),
  ('BNKB5874', 'withdrawal',  300.25),
  ('BNKB5874', 'withdrawal',  250.00),
  ('BNKA5726', 'deposit',    1500.00),
  ('BNKA5726', 'withdrawal',  100.00),
  ('BNKA5726', 'deposit',     200.00),
  ('BNKB5720', 'withdrawal',  500.00),
  ('BNKB5720', 'deposit',    1000.00),
  ('BNKB5720', 'withdrawal',  300.00),
  ('BNKB5720', 'deposit',     500.00),
  ('BNKB5720', 'withdrawal',  200.00)
) AS x(account_number, transaction_type, amount)
JOIN account a ON a.account_number = x.account_number;

-- Cashier check
INSERT INTO cashier_check (account_id, check_number, issue_date, amount, is_valid)
SELECT a.id, 'BNKB12345678', TIMESTAMPTZ '2024-03-01 10:00:00', 10000.00, TRUE
FROM account a WHERE a.account_number = 'BNKB5874'
ON CONFLICT (account_id, check_number) DO NOTHING;
