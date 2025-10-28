CREATE OR REPLACE VIEW sleeplab.vw_hypnogram_demo AS
SELECT s.session_id,
       ssr.ts,
       ssr.stage_label,
       ssr.confidence
FROM sleeplab.session_psg s
JOIN sleeplab.sleep_staging_result ssr USING (session_id)
ORDER BY s.session_id, ssr.ts;
