-- sample_data.sql
-- =========================
-- Banks
-- =========================
INSERT INTO bank (name, account_number_validity_pattern, check_validity_pattern)
VALUES
  ('Bank A', 'BNKA[0-9]{4}', 'BNKA[0-9]{8}'),
  ('Bank B', 'BNKB[0-9]{4}', 'BNKB[0-9]{8}')
ON CONFLICT (name) DO NOTHING;

-- =========================
-- Customers
-- =========================
INSERT INTO customer (full_name, email) VALUES
  ('Louis Charollais', 'louis.charollais@email.com'),
  ('John Doe',         'john.doe@email.com'),
  ('Jane Doe',         'jane.doe@email.com')
ON CONFLICT (email) DO NOTHING;

-- =========================
-- Accounts
-- =========================
WITH b AS (SELECT id, name FROM bank),
     c AS (SELECT id, email FROM customer)
INSERT INTO account (account_number, customer_id, bank_id, balance)
VALUES
  ('BNKA0123',
   (SELECT id FROM c WHERE email='louis.charollais@email.com'),
   (SELECT id FROM b WHERE name='Bank A'),
   12500.00),

  ('BNKB5874',
   (SELECT id FROM c WHERE email='john.doe@email.com'),
   (SELECT id FROM b WHERE name='Bank B'),
   9800.75),

  ('BNKA5726',
   (SELECT id FROM c WHERE email='jane.doe@email.com'),
   (SELECT id FROM b WHERE name='Bank A'),
   1500.00),

  ('BNKB5720',
   (SELECT id FROM c WHERE email='jane.doe@email.com'),
   (SELECT id FROM b WHERE name='Bank B'),
   2500.00)
ON CONFLICT (account_number) DO NOTHING;

-- =========================
-- Banking Transactions
-- =========================
INSERT INTO banking_transaction (account_number, transaction_type, amount)
VALUES
  ('BNKA0123', 'deposit',     1000.00),
  ('BNKA0123', 'withdrawal',   200.00),
  ('BNKA0123', 'deposit',      500.00),
  ('BNKB5874', 'deposit',     2000.00),
  ('BNKB5874', 'withdrawal',   300.25),
  ('BNKB5874', 'withdrawal',   250.00),
  ('BNKA5726', 'deposit',     1500.00),
  ('BNKA5726', 'withdrawal',   100.00),
  ('BNKA5726', 'deposit',      200.00),
  ('BNKB5720', 'withdrawal',   500.00),
  ('BNKB5720', 'deposit',     1000.00),
  ('BNKB5720', 'withdrawal',   300.00),
  ('BNKB5720', 'deposit',      500.00),
  ('BNKB5720', 'withdrawal',   200.00);

-- =========================
-- Bank Check
-- =========================
INSERT INTO bank_check (account_number, check_number, check_amount, check_status)
VALUES
  ('BNKB5874', 'BNKB12345678', 10000.00, 'cleared')
ON CONFLICT (account_number, check_number) DO NOTHING;
