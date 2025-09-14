-- Extensions utiles
CREATE EXTENSION IF NOT EXISTS citext;

-- Customer
CREATE TABLE IF NOT EXISTS customer (
  id BIGSERIAL PRIMARY KEY,
  full_name VARCHAR(100) UNIQUE NOT NULL,
  email CITEXT UNIQUE NOT NULL
);

-- Bank
CREATE TABLE IF NOT EXISTS bank (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  account_number_validity_pattern VARCHAR(100) NOT NULL UNIQUE,
  cashier_check_validity_pattern VARCHAR(100) NOT NULL UNIQUE
);

-- Account
CREATE TABLE IF NOT EXISTS account (
  id BIGSERIAL PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES customer(id) ON DELETE CASCADE,
  bank_id BIGINT NOT NULL REFERENCES bank(id) ON DELETE CASCADE,
  account_number VARCHAR(20) UNIQUE NOT NULL,
  balance NUMERIC(15, 2) NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Banking transaction
CREATE TABLE IF NOT EXISTS banking_transaction (
  id BIGSERIAL PRIMARY KEY,
  account_id BIGINT NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  transaction_type VARCHAR(20) NOT NULL,
  amount NUMERIC(15, 2) NOT NULL,
  transaction_date TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT transaction_type_chk CHECK (transaction_type IN ('deposit','withdrawal','transfer'))
);

-- Loan application
CREATE TABLE IF NOT EXISTS loan_application (
  id BIGSERIAL PRIMARY KEY,
  account_id BIGINT NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  loan_type VARCHAR(20) NOT NULL,
  loan_amount NUMERIC(15, 2) NOT NULL,
  loan_description TEXT,
  status VARCHAR(20) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT loan_status_chk CHECK (status IN ('pending','approved','rejected','cancelled'))
);

-- Cashier check
CREATE TABLE IF NOT EXISTS cashier_check (
  id BIGSERIAL PRIMARY KEY,
  account_id BIGINT NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  check_number VARCHAR(50) NOT NULL,
  issue_date TIMESTAMPTZ NOT NULL,
  amount NUMERIC(15, 2) NOT NULL,
  is_valid BOOLEAN NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (account_id, check_number)
);

-- Loan monitoring
CREATE TABLE IF NOT EXISTS loan_monitoring (
  id BIGSERIAL PRIMARY KEY,
  loan_application_id BIGINT NOT NULL REFERENCES loan_application(id) ON DELETE CASCADE,
  monitoring_date TIMESTAMPTZ NOT NULL DEFAULT now(),
  risk_status VARCHAR(100),
  check_validation_status VARCHAR(100),
  loan_provider_status VARCHAR(100),
  notification_status VARCHAR(100),
  customer_status VARCHAR(100)
);

-- Indexes sur FKs
CREATE INDEX IF NOT EXISTS idx_account_customer ON account(customer_id);
CREATE INDEX IF NOT EXISTS idx_account_bank     ON account(bank_id);
CREATE INDEX IF NOT EXISTS idx_tx_account       ON banking_transaction(account_id);
CREATE INDEX IF NOT EXISTS idx_loan_account     ON loan_application(account_id);
CREATE INDEX IF NOT EXISTS idx_check_account    ON cashier_check(account_id);
CREATE INDEX IF NOT EXISTS idx_monit_loan       ON loan_monitoring(loan_application_id);

-- Trigger pour updated_at
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

-- (Optionnel) Validation des numéros selon les patterns de la banque
CREATE OR REPLACE FUNCTION validate_account_number()
RETURNS TRIGGER AS $$
DECLARE pat text;
BEGIN
  SELECT account_number_validity_pattern INTO pat FROM bank WHERE id = NEW.bank_id;
  IF pat IS NOT NULL AND NEW.account_number !~ pat THEN
    RAISE EXCEPTION 'account_number % does not match bank pattern %', NEW.account_number, pat;
  END IF;
  RETURN NEW;
END; $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_account_validate ON account;
CREATE TRIGGER trg_account_validate
BEFORE INSERT OR UPDATE ON account
FOR EACH ROW EXECUTE FUNCTION validate_account_number();
