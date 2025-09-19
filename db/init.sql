-- Useful extensions
CREATE EXTENSION IF NOT EXISTS citext;

-- =========================
-- Customer
-- =========================
CREATE TABLE IF NOT EXISTS customer (
  id BIGSERIAL PRIMARY KEY,
  full_name VARCHAR(100) NOT NULL,
  email CITEXT UNIQUE NOT NULL
);

-- =========================
-- Bank
-- =========================
CREATE TABLE IF NOT EXISTS bank (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  account_number_validity_pattern VARCHAR(200) NOT NULL,
  check_validity_pattern VARCHAR(200) NOT NULL
);

-- =========================
-- Account
-- =========================
CREATE TABLE IF NOT EXISTS account (
  account_number VARCHAR(32) PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES customer(id) ON DELETE CASCADE,
  bank_id BIGINT NOT NULL REFERENCES bank(id) ON DELETE CASCADE,
  balance NUMERIC(15, 2) NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT balance_chk CHECK (balance >= 0) -- No negative value allowed
);

-- =========================
-- BankingTransaction
-- =========================
CREATE TABLE IF NOT EXISTS banking_transaction (
  id BIGSERIAL PRIMARY KEY,
  account_number VARCHAR(32) NOT NULL REFERENCES account(account_number) ON DELETE CASCADE,
  transaction_type VARCHAR(20) NOT NULL,
  amount NUMERIC(15, 2) NOT NULL,
  transaction_date TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT transaction_type_chk CHECK (transaction_type IN ('deposit','withdrawal','transfer')),
  CONSTRAINT amount_pos_chk CHECK (amount > 0)
);

-- =========================
-- LoanApplication
-- =========================
CREATE TABLE IF NOT EXISTS loan_application (
  id BIGSERIAL PRIMARY KEY,
  account_number VARCHAR(32) NOT NULL REFERENCES account(account_number) ON DELETE CASCADE,
  loan_type VARCHAR(20) NOT NULL,
  loan_amount NUMERIC(15, 2) NOT NULL,
  loan_description TEXT,
  status VARCHAR(20) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT loan_status_chk CHECK (status IN ('pending','approved','rejected','cancelled')),
  CONSTRAINT loan_amount_pos_chk CHECK (loan_amount > 0)
);

-- =========================
-- BankCheck
-- =========================
CREATE TABLE IF NOT EXISTS bank_check (
  id BIGSERIAL PRIMARY KEY,
  account_number VARCHAR(32) NOT NULL REFERENCES account(account_number) ON DELETE CASCADE,
  check_number VARCHAR(64) NOT NULL,
  check_amount NUMERIC(15, 2) NOT NULL,
  check_status VARCHAR(20) NOT NULL, -- enum via CHECK below
  CONSTRAINT check_amount_pos_chk CHECK (check_amount > 0),
  CONSTRAINT check_status_chk CHECK (check_status IN ('issued','cleared','bounced','rejected')),
  UNIQUE (account_number, check_number)
);

-- =========================
-- LoanMonitoring
-- =========================
CREATE TABLE IF NOT EXISTS loan_monitoring (
  loan_application_id BIGINT PRIMARY KEY REFERENCES loan_application(id) ON DELETE CASCADE,
  monitoring_date TIMESTAMPTZ NOT NULL DEFAULT now(),
  risk_status VARCHAR(100),
  check_validation_status VARCHAR(100),
  loan_provider_status VARCHAR(100),
  notification_status VARCHAR(100),
  customer_status VARCHAR(100)
);

-- =========================
-- Indexes
-- =========================
CREATE INDEX IF NOT EXISTS idx_account_customer ON account(customer_id);
CREATE INDEX IF NOT EXISTS idx_account_bank     ON account(bank_id);
CREATE INDEX IF NOT EXISTS idx_tx_account       ON banking_transaction(account_number);
CREATE INDEX IF NOT EXISTS idx_tx_date          ON banking_transaction(transaction_date);
CREATE INDEX IF NOT EXISTS idx_loan_account     ON loan_application(account_number);
CREATE INDEX IF NOT EXISTS idx_check_account    ON bank_check(account_number);

-- =========================
-- Trigger updated_at on account
-- =========================
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at := now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_account_updated_at ON account;
CREATE TRIGGER trg_account_updated_at
BEFORE UPDATE ON account
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- =========================
-- Validation of account_number vs bank pattern
-- =========================
CREATE OR REPLACE FUNCTION validate_account_number()
RETURNS TRIGGER AS $$
DECLARE pat text;
BEGIN
  SELECT account_number_validity_pattern INTO pat
  FROM bank WHERE id = NEW.bank_id;

  IF pat IS NOT NULL AND NEW.account_number !~ pat THEN
    RAISE EXCEPTION 'account_number % does not match bank pattern %', NEW.account_number, pat;
  END IF;

  RETURN NEW;
END; $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_account_validate ON account;
CREATE TRIGGER trg_account_validate
BEFORE INSERT OR UPDATE ON account
FOR EACH ROW EXECUTE FUNCTION validate_account_number();

-- =========================
-- Validation of check_number vs bank pattern
-- (gets bank_id via account -> bank)
-- =========================
CREATE OR REPLACE FUNCTION validate_check_number()
RETURNS TRIGGER AS $$
DECLARE pat text;
DECLARE b_id BIGINT;
BEGIN
  SELECT bank_id INTO b_id FROM account WHERE account_number = NEW.account_number;
  IF b_id IS NULL THEN
    RAISE EXCEPTION 'Unknown account_number %', NEW.account_number;
  END IF;

  SELECT check_validity_pattern INTO pat FROM bank WHERE id = b_id;

  IF pat IS NOT NULL AND NEW.check_number !~ pat THEN
    RAISE EXCEPTION 'check_number % does not match bank check pattern %', NEW.check_number, pat;
  END IF;

  RETURN NEW;
END; $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_check_validate ON bank_check;
CREATE TRIGGER trg_check_validate
BEFORE INSERT OR UPDATE ON bank_check
FOR EACH ROW EXECUTE FUNCTION validate_check_number();
