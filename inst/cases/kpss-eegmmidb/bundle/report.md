# kpss-eegmmidb

- KPSS level-stationarity statistic (lag 10) of the POz signal (0.20)
- |KPSS statistic - statsmodels kpss| (bit-exact) (7e-16)
- statsmodels 5% KPSS critical value (reference table) (0.463)
- KPSS fails to reject the stationarity null (statistic < critical; 1 = stationary) (yes)
- ADF rejects the unit-root null (the complementary test also says stationary) (yes)
- ADF and KPSS concur the segment is stationary (the confirmatory pair agrees) (yes)
