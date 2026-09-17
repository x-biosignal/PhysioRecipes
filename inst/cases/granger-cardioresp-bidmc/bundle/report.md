# granger-cardioresp-bidmc

- time-domain Granger causality respiration -> PPG pulse (Geweke log-variance-ratio) (0.103)
- time-domain Granger causality PPG pulse -> respiration (0.102)
- net Granger causality (respiration->pulse minus pulse->respiration) -- the directional asymmetry (+0.0015)
- max |grangerCausality - statsmodels grangercausalitytests| over both directions (agreement) (3.5e-07)
- max |grangerCausality - independent numpy OLS| over both directions (op arithmetic, machine precision up to ridge) (1.8e-09)
- BIDMC subjects (of 20) where respiration -> pulse is the net-dominant Granger direction (15)
