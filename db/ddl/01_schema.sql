--TEST--
CREATE SCHEMA IF NOT EXISTS sleeplab;

CREATE TABLE IF NOT EXISTS sleeplab.patient (
  patient_id      BIGSERIAL PRIMARY KEY,
  anon_id         TEXT UNIQUE NOT NULL,
  birth_year      INT,
  sex             TEXT CHECK (sex IN ('F','M','U')),
  created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS sleeplab.session_psg (
  session_id      BIGSERIAL PRIMARY KEY,
  patient_id      BIGINT NOT NULL REFERENCES sleeplab.patient(patient_id),
  started_at      TIMESTAMPTZ NOT NULL,
  ended_at        TIMESTAMPTZ,
  notes           TEXT
);

CREATE TABLE IF NOT EXISTS sleeplab.algo_run (
  run_id          BIGSERIAL PRIMARY KEY,
  algo_name       TEXT NOT NULL,
  algo_version    TEXT NOT NULL,
  run_ts          TIMESTAMPTZ DEFAULT now(),
  params_hash     TEXT
);

CREATE TABLE IF NOT EXISTS sleeplab.sleep_staging_result (
  id              BIGSERIAL PRIMARY KEY,
  session_id      BIGINT NOT NULL REFERENCES sleeplab.session_psg(session_id),
  run_id          BIGINT NOT NULL REFERENCES sleeplab.algo_run(run_id),
  ts              TIMESTAMPTZ NOT NULL,
  stage_label     TEXT NOT NULL,   -- e.g. W,N1,N2,N3,REM
  confidence      NUMERIC(5,4)     -- 0..1
);
COMMENT ON SCHEMA sleeplab IS 'L2 logical model (demo)';
COMMENT ON TABLE sleeplab.sleep_staging_result IS 'Unified output for staging across algos';
--FIN DU TEST--