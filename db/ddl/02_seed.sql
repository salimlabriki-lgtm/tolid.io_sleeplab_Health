--TEST
INSERT INTO sleeplab.patient (anon_id, birth_year, sex) VALUES ('P-0001', 1990, 'U')
ON CONFLICT (anon_id) DO NOTHING;

INSERT INTO sleeplab.session_psg (patient_id, started_at, ended_at, notes)
SELECT patient_id, now() - interval '90 min', now(), 'demo session'
FROM sleeplab.patient WHERE anon_id='P-0001';

INSERT INTO sleeplab.algo_run (algo_name, algo_version, params_hash)
VALUES ('yasa', '0.6.3', 'demo');

-- 5 points fictifs d’hypnogramme
INSERT INTO sleeplab.sleep_staging_result(session_id, run_id, ts, stage_label, confidence)
SELECT s.session_id, r.run_id, now() - x*interval '15 min',
       (ARRAY['W','N1','N2','N3','REM'])[x], 0.90
FROM generate_series(1,5) AS x
CROSS JOIN LATERAL (SELECT session_id FROM sleeplab.session_psg ORDER BY session_id DESC LIMIT 1) s
CROSS JOIN LATERAL (SELECT run_id FROM sleeplab.algo_run ORDER BY run_id DESC LIMIT 1) r;
--FIN DU TEST