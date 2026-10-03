# mutual-info-cardioresp-bidmc

- mutual information of RESP and PLETH (histogram estimator, nats) -- the undirected shared information (0.077)
- sklearn.metrics.mutual_info_score on the identical binning -- matches the op (0.07713332)
- max |mutualInformation - sklearn.metrics.mutual_info_score| on the identical binning (bit-exact) (5e-16)
- mutual information of RESP vs a SHUFFLED PLETH -- the histogram estimator's finite-sample bias floor (0.024)
- real / shuffled MI ratio -- the coupling detected above the finite-sample floor (3.2x)
- samples per signal (200 s at 25 Hz) (5001)
