# PhysioRecipes 0.6.51

* New validated case `pacf-eegmmidb` — a **new-method authoring** case completing the ACF/PACF pair:
  introduces and certifies a newly-authored op, `PhysioAnalysis::partialAutocorrelation` (PACF via
  Durbin-Levinson on the biased ACF, building on the just-added `autocorrelation`). On a real eyes-closed
  EEG channel it reproduces the field-standard `statsmodels.tsa.pacf(method = "ldb")` **bit-for-bit**
  (max |diff| ~**6e-15**) across lags 0..20. Finding: the lag-1 PACF exactly equals the lag-1 ACF (0.856,
  the definitional identity), and the lag-2 PACF is strongly negative (-0.627) — the signature of an
  oscillatory AR(2)-like process, exactly what eyes-closed posterior alpha (a resonant ~10 Hz rhythm)
  looks like. Honest scope: newly-authored op (biased ldb convention; unbiased yw/ld/ols differ by
  construction); machine-precision (identical Levinson-Durbin recursion).

# PhysioRecipes 0.6.50

* New validated case `autocorrelation-eegmmidb` — a **new-method authoring** case adding the
  foundational time-series primitive the ecosystem lacked: introduces and certifies a newly-authored
  op, `PhysioAnalysis::autocorrelation` (single-series ACF, biased/demeaned estimator). On a real
  eyes-closed EEG channel it reproduces the field-standard `statsmodels.tsa.acf` (adjusted = FALSE)
  **bit-for-bit** (max |diff| ~**2e-16**) across lags 0..30. Finding: the lag-0 value is exactly 1 (the
  ACF identity), and the ACF decays below 1/e by lag 3 — a short decorrelation time (~19 ms at 160 Hz).
  Honest scope: newly-authored op filling the single-series gap (crossCorrelation is between-two-series);
  machine-precision (identical estimator); a foundational primitive certified against statsmodels.

# PhysioRecipes 0.6.49

* New validated case `enmoa-freeliving-pamap2` — a **new-method authoring** case completing the
  accelerometer movement triad: introduces and certifies a newly-authored op,
  `PhysioWearable::computeENMOa` (ENMO-abs, `|r - 1|`), the always-positive companion of ENMO that
  retains the sub-1 g dips ENMO's truncation discards. On a real ~62-minute PAMAP2 free-living
  hand-accelerometer recording it reproduces `GGIR::g.applymetrics` ENMOa to **machine precision**
  (max |diff| ~**2e-14 g**, correlation 1.0) across all **749** 5 s epochs. Finding: ENMOa ≥ ENMO at
  every epoch and exceeds it by **~63 mg** on average (mean 224 vs 162 mg) — the movement below 1 g
  that ENMO discards. Honest scope: newly-authored op; machine-precision (identical computation); ENMOa
  a physical quantity completing the ENMO+MAD+ENMOa triad.

# PhysioRecipes 0.6.48

* New validated case `hti-tinn-fantasia` — a **cross-tool reproducibility-audit** case (not new-method
  authoring): certifies the shipped `PhysioECG::ecgHRVgeometric` against the field-standard
  `NeuroKit2.hrv_time` geometric HRV indices on a real 5-minute Fantasia RR series. The **HRV triangular
  index (HTI)** reproduces NeuroKit2 HRV_HTI **bit-for-bit** (|diff| 0) — an integer-ratio index (391
  intervals / a modal histogram height of 35 = 11.17) at the shared 1/128 s standard bin. **TINN**, by
  contrast, **differs** (164 vs 297 ms) — a documented triangular-interpolation convention (least-squares
  triangle base width vs NeuroKit2's fit), not a bug in either tool. Takeaway: HTI is portable and
  convention-free; report which TINN you use. Honest scope: cross-tool re-certification (op extended only
  to accept an RR data frame); HTI portable integer ratio; TINN convention-dependent.

# PhysioRecipes 0.6.47

* New validated case `phase-entropy-eegmmidb` — a **new-method authoring** case adding a phase-plane
  complexity mechanism: introduces and certifies a newly-authored op, `PhysioEEG::phaseEntropy` (phase
  entropy, Rohila & Sharma 2019), which builds the Second-Order Difference Plot (first vs second
  differences) and takes the normalized Shannon entropy of the polar-angle distribution over k sectors.
  On a real eyes-closed EEG channel it reproduces `NeuroKit2.entropy_phase` **bit-for-bit** (max |diff|
  ~**4e-16**) across the sector count k. Finding: PhasEn increases with k (1.238 → 1.287 → 1.299) and
  sits below the 1/ln(2) = 1.443 normalization ceiling. Honest scope: newly-authored op;
  machine-precision (identical pipeline); NeuroKit2 normalization reproduced; value depends on (delay, k).

# PhysioRecipes 0.6.46

* New validated case `slope-entropy-eegmmidb` — a **new-method authoring** case completing the
  discrete-symbolic complexity trio: introduces and certifies a newly-authored op,
  `PhysioEEG::slopeEntropy` (slope entropy, Cuesta-Frau 2019), which symbolizes the slope angle
  `atan(dx)` between successive samples into five classes (steep/gentle/flat, up/down) and takes the
  Shannon entropy of the slope patterns — capturing local-trend shape (vs the amplitude-pattern and
  increment-magnitude mechanisms). It is the ecosystem's **100th registered analysis tool**. On a real
  eyes-closed EEG channel it reproduces `NeuroKit2.entropy_slope` **bit-for-bit** (max |diff| ~**9e-16**)
  across the embedding dimension. Finding: unlike the normalized entropies it **increases** with
  dimension (1.26 → 2.43 → 3.57, an unnormalized Shannon over longer patterns), and the signal realizes
  18 of the 25 = 5^(m-1) possible slope patterns at m=3. Honest scope: newly-authored op;
  machine-precision (identical pipeline); value depends on (dimension, thresholds).

# PhysioRecipes 0.6.45

* New validated case `mad-freeliving-pamap2` — a **new-method authoring** case completing the
  accelerometer ENMO+MAD metric pair: introduces and certifies a newly-authored op,
  `PhysioWearable::computeMAD` (mean amplitude deviation, Vähä-Ypyä et al. 2015), the gravity-robust
  movement metric complementary to the (GGIR-certified) ENMO. On a real ~62-minute PAMAP2 free-living
  hand-accelerometer recording it reproduces `GGIR::g.applymetrics` MAD to **machine precision**
  (max |diff| ~**5e-14 g**, correlation 1.0) across all **749** 5 s epochs. Finding: MAD measures the
  *variation* of the acceleration magnitude within an epoch (vs ENMO's *elevation* above 1 g), and on
  this recording ranges 5–1222 mg (mean 232 mg) — a physical movement profile. Honest scope:
  newly-authored op; machine-precision (identical computation); MAD is a physical quantity, so the
  mean/max/min are meaningful movement descriptors.

# PhysioRecipes 0.6.44

* New validated case `increment-entropy-eegmmidb` — a **new-method authoring** case adding the
  increment-domain complexity the ecosystem lacked: introduces and certifies a newly-authored op,
  `PhysioEEG::incrementEntropy` (increment entropy, Liu et al. 2016), which symbolizes each successive
  increment by its sign and a magnitude class and takes the normalized Shannon entropy of the
  increment-words — a mechanism distinct from the amplitude-histogram, NCDF-pattern and
  template-matching entropies. On a real eyes-closed EEG channel it reproduces
  `NeuroKit2.entropy_increment` **bit-for-bit** (max |diff| ~**9e-16**) across (dimension, q). Finding:
  it is non-increasing in the embedding dimension (4.27 → 3.51 → 3.01 at q=4), and the signal realizes
  only **33 of the 81** = (2q+1)^m possible increment-words (structured). Honest scope: newly-authored
  op; machine-precision (identical pipeline); value depends on (dimension, q).

# PhysioRecipes 0.6.43

* New validated case `fuzzy-entropy-eegmmidb` — a **new-method authoring** case completing the
  sample-entropy family: introduces and certifies a newly-authored op, `PhysioEEG::fuzzyEntropy`
  (fuzzy entropy, Chen et al. 2007), the **fuzzy generalization of sample entropy** — a smooth
  exponential membership `exp(-(d^n)/r)` replaces the crisp Heaviside match threshold, so near-matches
  count partially (far more robust on short/noisy segments). On a real eyes-closed EEG channel it
  reproduces `NeuroKit2.entropy_fuzzy` **bit-for-bit** (max |diff| ~**4e-15**) across (dimension, r).
  Finding: at m=2, r=0.2 FuzzyEn (**0.948**) is lower than the crisp sample entropy (**1.327**) — the
  soft membership counts near-matches the step rejects — and FuzzyEn is non-increasing in the embedding
  dimension. Honest scope: newly-authored op; machine-precision (identical pipeline); value depends on
  (dimension, r, fuzzy power n).

# PhysioRecipes 0.6.42

* New validated case `hrv-time-neurokit-fantasia` — a **cross-tool reproducibility-audit** case (not
  new-method authoring): certifies the shipped `PhysioECG::ecgHRVtime` against the field-standard
  Python reference `NeuroKit2.hrv_time` on a real 5-minute Fantasia RR series. The three core
  Task-Force metrics — **MeanNN, SDNN and RMSSD** (the two most-reported HRV indices in physiology) —
  reproduce NeuroKit2 **bit-for-bit** (max |diff| 0). The sole divergence is **pNN50** (37.18% vs
  37.08%), a documented **denominator convention** — `ecgHRVtime` divides the nn50 count by the number
  of successive differences (N−1 = 390), NeuroKit2 by the number of intervals (N = 391) — with the
  nn50 count itself **identical at 145**, proving the gap is denominator-only, not a beat-detection or
  threshold difference. Honest scope: cross-tool re-certification; MeanHR (60000/mean(RR)) estimand not
  cross-validated (NeuroKit2 hrv_time returns no MeanHR column).

# PhysioRecipes 0.6.41

* New validated case `dispersion-entropy-eegmmidb` — a **new-method authoring** case introducing a
  newly-authored op, `PhysioEEG::dispersionEntropy` (dispersion entropy, Rostaghi & Azami 2016), a
  fast outlier-robust symbolic-dynamics complexity measure with a mechanism distinct from every
  entropy folded so far (NCDF amplitude-class ranking + embedding "dispersion patterns", rather than
  amplitude binning or ordinal ranking). On a real eyes-closed EEG channel it reproduces
  `NeuroKit2.entropy_dispersion` **bit-for-bit** for both the dispersion entropy DispEn (max |diff| 0)
  and the reverse dispersion entropy RDEn (max |diff| ~7e-18) across (c, dimension, delay) settings.
  Finding: the signal realizes only **108 of the 216** = c^m possible dispersion patterns (structured,
  not pattern-saturating), and DispEn (1.117) sits below the base-2/ln normalization ceiling
  1/ln(2) = 1.443. Honest scope: newly-authored op; machine-precision (identical pipeline); NCDF
  classes near-equiprobable so complexity lives in the patterns; NeuroKit2 normalization reproduced,
  not corrected.

# PhysioRecipes 0.6.40

* New validated case `tsallis-entropy-eegmmidb` — a **new-method authoring** case that completes the
  generalized-entropy pair: introduces and certifies a newly-authored op, `PhysioEEG::tsallisEntropy`
  (Tsallis entropy, 1988), the **non-additive** counterpart of the (additive) `renyiEntropy` added in
  the previous case. On a real eyes-closed EEG channel it reproduces `NeuroKit2.entropy_tsallis`
  **bit-for-bit** (max |diff| ~**9e-16**) across `q = {0.5, 1, 2, 3}`. Finding: at `q = 1` the Tsallis
  entropy exactly recovers the Shannon entropy (2.325 nats) **and coincides with the Renyi entropy**,
  but at `q = 2` it diverges sharply (Tsallis 0.885 vs Renyi 2.167) — the two generalizations meet
  **only at `q = 1`** because Tsallis is non-additive; `S_q` is non-increasing in `q`. Honest scope:
  newly-authored op; machine-precision (identical formula, not a convention agreement); histogram
  bin-count-dependent (structure, not an absolute physiological quantity).

# PhysioRecipes 0.6.39

* New validated case `renyi-entropy-eegmmidb` — a **new-method authoring** case: introduces and
  certifies a newly-authored op, `PhysioEEG::renyiEntropy` (Renyi entropy, 1961), the generalized
  (order-`alpha`) entropy family, filling the gap the ecosystem's Shannon-based entropies
  (permutation, sample, spectral) left open. On a real eyes-closed EEG channel it reproduces
  `NeuroKit2.entropy_renyi` **bit-for-bit** (max |diff| ~**4e-16**) across `alpha = {0.5, 1, 2, 3}`.
  Finding: the `alpha = 1` value exactly recovers the Shannon entropy (2.325 nats), `alpha = 2` the
  collision entropy (2.167), and the family is monotonically decreasing in `alpha` — the defining
  structure. Honest scope: histogram/bin-dependent, so the structure (not the absolute value) is the
  content. Requires PhysioEEG >= 0.7.7. Coverage map regenerated (68 cases).

# PhysioRecipes 0.6.38

* New validated case `petrosian-fd-eegmmidb` — a **new-method authoring** case: introduces and
  certifies a newly-authored op, `PhysioEEG::petrosianFD` (Petrosian fractal dimension, 1995), a fast
  waveform-complexity index filling the gap the complexity suite (permutation entropy, Lempel-Ziv,
  Hjorth, sample/approximate entropy, DFA, RQA, SVD entropy) left open. On a real eyes-closed
  posterior EEG channel it reproduces `antropy.petrosian_fd` **bit-for-bit** (max |diff| **0**;
  unlike Higuchi/Katz, Petrosian has one unambiguous closed form). Finding: Petrosian FD is lower over
  the posterior alpha region (all 9 parieto-occipital channels below the frontal mean; 1.020 vs
  1.027) — the eyes-closed alpha rhythm is a smoother oscillation, the sixth complementary view of
  posterior alpha (with Welch/spectrogram/Hjorth/coherence/SVD). Requires PhysioEEG >= 0.7.6.
  Coverage map regenerated (67 cases).

# PhysioRecipes 0.6.37

* New validated case `mutual-info-cardioresp-bidmc` — a **new-method authoring** case: introduces and
  certifies a newly-authored op, `PhysioCrossModal::mutualInformation` (histogram mutual information),
  the undirected information-theoretic complement of transfer entropy, filling a gap (the ecosystem
  had directed TE, coherence, cross-correlation, distance correlation — but no general MI). On real
  cardiorespiratory signals (BIDMC-01 RESP + PLETH) it reproduces `sklearn.metrics.mutual_info_score`
  **bit-for-bit** (max |diff| ~**5e-16**) on the identical binning. Finding: the real RESP-PLETH MI
  (0.077 nats) is ~3.2x the histogram estimator's shuffled finite-sample floor (0.024) — a genuine
  undirected dependence (the shared respiratory modulation). Honest scope: histogram estimator is
  positively biased (ratio-to-shuffled, not absolute, is the signal); in nats. Requires PhysioCrossModal
  >= 0.7.1. Coverage map regenerated (66 cases).

# PhysioRecipes 0.6.36

* New validated case `svd-entropy-eegmmidb` — a **new-method authoring** case: introduces and
  certifies a newly-authored op, `PhysioEEG::svdEntropy` (SVD entropy, Roberts 1999), filling the
  dimensionality gap the complexity suite (permutation entropy, Lempel-Ziv, Hjorth, sample/approximate
  entropy, DFA, RQA) left open. On a real eyes-closed posterior EEG channel it reproduces
  `antropy.svd_entropy` **bit-for-bit** (max |diff| ~**2e-16**; both via LAPACK SVD). Finding: SVD
  entropy is lower over the posterior alpha region (all 9 parieto-occipital channels below the frontal
  mean; posterior 1.24 vs frontal 1.29) — the eyes-closed alpha rhythm is a low-dimensional
  oscillation, consistent with the Welch/spectrogram/Hjorth/coherence cases on the same data. Requires
  PhysioEEG >= 0.7.5. Coverage map regenerated (65 cases).

# PhysioRecipes 0.6.35

* New validated case `csi-cvi-fantasia` — a **new-method authoring** case: introduces and certifies
  a newly-authored op, `PhysioECG::ecgHRVautonomic` (the Toichi cardiac autonomic indices CSI/CVI/
  CSI_Modified from the Poincare 4-SD box), filling the gap the ecosystem's raw SD1/SD2 left open. On
  a real 5-minute RR window (Fantasia f1y01) it reproduces NeuroKit2's `hrv_nonlinear` indices
  **bit-for-bit** (max |diff| **0**). Finding: the Cardiac Vagal Index is higher in the young (4.90)
  than the old (4.55), robust across the cohort (5/5 young above the old mean) — the parasympathetic
  decline of autonomic aging, complementing the DFA and Poincare aging cases. Requires PhysioECG >=
  0.4.1. Coverage map regenerated (64 cases).

# PhysioRecipes 0.6.34

* New validated case `hra-fantasia` — a **new-method authoring** case: introduces and certifies a
  newly-authored op, `PhysioECG::ecgHRVasymmetry` (heart-rate asymmetry), filling the gap the
  ecosystem's symmetric SD1/SD2 left open. On a real 5-minute RR window (Fantasia f1y01), the op
  reproduces NeuroKit2's `hrv_nonlinear` HRA indices (GI/SI/AI/PI + the C1d/C1a/C2d/C2a
  deceleration/acceleration contributions) **bit-for-bit** (max |diff| ~**1e-14**). Finding:
  decelerations dominate short-term variability (C1d 0.63 > C1a 0.37), the established HRA signature,
  robust across the cohort (8/10 subjects); accelerations dominate long-term (C2a 0.64 > C2d 0.36).
  Honest scope: the op is newly authored (identical Piskorski-Guzik formulas → bit-exact); the
  long-term asymmetry is mixed across the small cohort and no age direction is claimed. Requires
  PhysioECG >= 0.4.0. Coverage map regenerated (63 cases).

# PhysioRecipes 0.6.33

* New validated case `eeg-detrend-scipy-eegmmidb` — a **preprocessing-primitive fidelity** case: the
  first external-reference (scipy) certification of `PhysioPreprocess::detrendSignal` (the detrend
  step that precedes the Welch/spectrogram estimates). On a real drifting frontopolar EEG channel
  (Fpz), it reproduces `scipy.signal.detrend` **bit-for-bit** (max |diff| ~**1e-12** linear, **0**
  constant — identical least-squares-line/mean formulas). Finding (methodological): the **linear**
  detrend removes a low-frequency trend that **constant** (mean) removal leaves in — sub-1-Hz Welch
  power falls from 1284 (raw) to 59 (linear) vs 112 (constant), so the detrend *type* removes ~47%
  more low-frequency leakage. Honest scope: detrendSignal is not a new op; linear detrend removes only
  the linear part (oscillatory wander needs a high-pass). Coverage map regenerated (62 cases).

# PhysioRecipes 0.6.32

* New validated case `eeg-coherence-scipy-eegmmidb` — a **connectivity fidelity** case (the spatial
  view completing the eyes-closed EEG arc after Welch power and spectrogram dynamics): the first
  external-reference (scipy) certification of `PhysioEEG::eegCoherence`. On the eight
  parieto-occipital channels of real eyes-closed EEG, its magnitude-squared coherence reproduces
  `scipy.signal.coherence` **bit-for-bit** (max |diff| ~**2e-16** across all 28 pairs) once
  conventions match — symmetric Hann, matched window length + overlap, detrend=False; the coherence
  ratio cancels the window normalization. Finding: posterior alpha coherence is high (mean 0.63,
  peaking 0.90 between adjacent occipital channels PO3–O1) — the eyes-closed alpha rhythm is
  spatially synchronized. Honest scope: eegCoherence is not a new op; magnitude-squared coherence is
  inflated by volume conduction (imaginary coherence, also available, addresses it). Coverage map
  regenerated (61 cases).

# PhysioRecipes 0.6.31

* New validated case `eeg-spectrogram-scipy-eegmmidb` — a **time-frequency fidelity** case (the
  time-resolved sibling of the Welch case): the first external-reference (scipy) certification of
  the `PhysioAnalysis::spectrogram` (STFT). On real eyes-closed posterior EEG (POz), it reproduces
  `scipy.signal.spectrogram` **bit-for-bit** (max |diff| ~**7e-13** over the full 129 × 11
  frequency × time matrix) once conventions are matched — symmetric Hann, no detrend, density
  scaling, one-sided doubling, nperseg=256, 50% overlap, mode='psd'. Finding: the alpha rhythm
  dominates every one of the 11 windows (peak in 8–13 Hz, median 11.25 Hz) yet its power waxes and
  wanes across time (CV ~58%) — the amplitude modulation the time-averaged Welch PSD hides. Honest
  scope: spectrogram is not a new op; the match requires the matched conventions (scipy's defaults
  differ). Coverage map regenerated (60 cases).

# PhysioRecipes 0.6.30

* New validated case `eeg-bandpower-welch-eegmmidb` — a **spectral-estimation fidelity** case: the
  first external-reference (scipy) certification of the `PhysioAnalysis::bandPower` **Welch**
  estimator (used across the EEG cases for findings, never checked against the reference). On real
  eyes-closed 64-channel EEG, its band powers reproduce `scipy.signal.welch` **bit-for-bit**
  (max |diff| ~**7e-13** over 64 channels × 5 bands) once conventions are matched — symmetric Hann
  window, no per-segment detrend, density scaling, one-sided doubling, nperseg=256, 50% overlap.
  Finding: relative alpha power is highest over the parieto-occipital region (peak POz 0.73;
  posterior mean 0.69 vs frontal 0.28) — the eyes-closed posterior alpha rhythm, cross-consistent
  with the Hjorth case's low posterior mobility on the same data. Honest scope: bandPower is not a
  new op; the match requires the symmetric-Hann + no-detrend conventions (scipy's defaults differ).
  Coverage map regenerated (59 cases).

# PhysioRecipes 0.6.29

* New validated case `poincare-hrv-fantasia` — a **nonlinear-HRV geometry** case (the geometric
  complement of the DFA fractal-scaling case on the same Fantasia cohort). On a real 5-minute RR
  window, `PhysioECG::ecgHRVpoincare` computes the Poincare descriptors **SD1** (short-term/vagal,
  **54.3 ms**) and **SD2** (long-term, **81.5 ms**). It reproduces an independent from-scratch
  numpy analytical closed-form **bit-for-bit** (max |diff| **0**) and NeuroKit2 `hrv_nonlinear`:
  SD1 bit-for-bit (the universal SDSD/√2), SD2 up to a documented ~0.2 ms convention (op =
  analytical closed-form; NeuroKit2 = geometric paired-projection, reproduced bit-for-bit by an
  independent numpy paired projection). Finding: short-term HRV (SD1) is markedly higher in the
  young (53.1 ms) than the old (35.3 ms) — an age-related cardiac-vagal decline. Honest scope:
  the SD2 gap is a resolved convention (neither wrong); aging is descriptive (n=5+5). Coverage
  map regenerated (58 cases).

# PhysioRecipes 0.6.28

* New validated case `te-cardioresp-bidmc` — a **model-free directed-coupling** case
  (the information-theoretic complement of the linear Granger case on the same pair). On real
  cardiorespiratory signals (BIDMC-01), `PhysioCrossModal::transferEntropy` (histogram estimator)
  measures the **respiration → pulse** transfer entropy (**0.036 bits**) exceeding **pulse →
  respiration** (**0.024**), net **+0.012** — the same directed asymmetry Granger found, with no
  linearity assumed. It reproduces an independent from-scratch numpy transfer entropy
  **bit-for-bit** (max |diff| ~6e-17 in both directions) and recovers a constructed x → y coupling
  (TE **0.67** driving vs **0.06** reverse). Honest scope: the histogram estimator is
  estimator-dependent with a positive finite-sample bias (raw values are point estimates, not
  significance tests). Coverage map regenerated (57 cases).

# PhysioRecipes 0.6.27

* New validated case `ecg-ppg-crosscorr-bidmc` — a **time-domain cross-correlation** coupling
  case (complementing the frequency-domain coherence). On real simultaneous ECG + PPG
  (BIDMC-01), `PhysioCrossModal::crossCorrelation` measures the **pulse arrival time**: the
  ECG-PPG cross-correlation peaks at **0.39 s** (heart → fingertip). It reproduces an independent
  from-scratch numpy normalized cross-correlation **bit-for-bit** (max |diff| ~3e-14 across all
  lags) and its peak lag matches `scipy.signal.correlate`. Coverage map regenerated (56 cases).

# PhysioRecipes 0.6.26

* New validated case `eeg-wpli-alpha-eegmmidb` — a **debiased weighted phase-lag index**
  (wPLI) case, completing the canonical phase-connectivity trio (PLV → PLI → wPLI). On the
  same real occipital O1-Oz pair, `PhysioCrossModal::weightedPLI` gives a debiased wPLI of
  **0.011** — confirming (like PLI) the strong alpha PLV of 0.92 is mostly volume conduction.
  Validated by reproducing an independent scipy imaginary-cross-spectrum wPLI (**~7e-3**) and
  demonstrating the debiasing: for independent signals the biased wPLI is a spurious 0.038 but
  the debiased wPLI collapses to **0.0006**, while genuine lagged coupling stays **1.0**.
  Coverage map regenerated (55 cases).

# PhysioRecipes 0.6.25

* New validated case `eeg-pli-alpha-eegmmidb` — a **phase-lag index** (PLI)
  volume-conduction-robust connectivity case. On the same real occipital O1-Oz pair whose
  alpha PLV is 0.92 (sibling case), `PhysioCrossModal::phaseLagIndex` gives **PLI = 0.016** —
  the strong PLV is almost entirely near-zero-lag (volume conduction / common reference),
  which PLI discounts. Validated three ways: recovers the volume-conduction contrast
  (constructed zero-lag → PLV 0.99 / **PLI 0.01**; lagged → **PLI 1.0**), reproduces an
  independent scipy Hilbert-band PLI (**~4e-3**), and its sign formula is exact. Coverage map
  regenerated (54 cases).

# PhysioRecipes 0.6.24

* New validated case `eeg-plv-alpha-eegmmidb` — a **phase-locking value** (PLV) phase-
  connectivity case. On real eyes-closed occipital EEG (eegmmidb S002R02, O1 & Oz),
  `PhysioCrossModal::phaseLockingValue` measures alpha-band phase synchronization
  (**PLV 0.92**, nearly in phase). Validated three ways: it recovers ground truth
  (phase-locked → **0.995**, independent → **0.009**), reproduces an independent scipy
  Hilbert-band PLV to **~8e-5** (phase-robust, up to the filtfilt convention), and its
  summation formula is exact. Coverage map regenerated (53 cases).

# PhysioRecipes 0.6.23

* New validated case `eeg-hjorth-eegmmidb` — a **Hjorth-parameters** time-domain-complexity
  case across a full 64-channel montage. On real eyes-closed EEG (eegmmidb S002R02),
  `PhysioEEG::eegComplexity` computes Hjorth mobility + complexity per channel; they reproduce
  an independent numpy implementation **bit-for-bit** (~9e-16 across all 64 channels) and
  `antropy.hjorth_params` to **~3e-7** (up to the variance ddof convention). Mobility maps the
  eyes-closed alpha topography — lowest over parieto-occipital (POz, 0.53), highest over
  temporal (T7, 1.45). Coverage map regenerated (52 cases).

# PhysioRecipes 0.6.22

* New validated case `eeg-multitaper-alpha-eegmmidb` — a **multitaper** robust-spectral-
  estimation case. On real eyes-closed occipital EEG (eegmmidb S001R02, O1),
  `PhysioEEG::eegMultitaper` computes the non-adaptive multitaper PSD (average of DPSS-tapered
  periodograms); its DPSS tapers reproduce `scipy.signal.windows.dpss` to **~6e-14** and its
  full PSD an independent scipy+numpy reconstruction to **~1e-10** (both machine precision),
  and it agrees with MNE `psd_array_multitaper` in structure (correlation **0.99**, up to a
  one-sided factor-of-2). The spectrum is alpha-dominated (peak **10.5 Hz**, 46% of 0–45 Hz
  power in the alpha band). Coverage map regenerated (51 cases).

# PhysioRecipes 0.6.21

* New validated case `hrv-lomb-fantasia` — a **Lomb-Scargle** spectral-estimation case for
  the unevenly-sampled RR tachogram. On real Fantasia RR (young subject f1y01, 8708 beats),
  `PhysioECG::ecgHRVfreq(method="lomb")` computes the Lomb-Scargle periodogram (the correct
  estimate for irregular sampling — no interpolation) and reproduces the canonical
  `scipy.signal.lombscargle` to **machine precision**: the periodogram to a relative ~1e-10
  and the integrated VLF/LF/HF band powers to ~7e-11. The resting autonomic balance is
  **HF-dominant** (LF/HF ≈ 0.48, HF 67% of LF+HF). Coverage map regenerated (50 cases).

# PhysioRecipes 0.6.20

* New validated case `granger-cardioresp-bidmc` — the corpus's first **directed/causal
  connectivity** case. On real simultaneous respiration + PPG (BIDMC subject 01),
  `PhysioCrossModal::grangerCausality` measures time-domain Granger causality in both
  directions; cardiorespiratory coupling is strong and **bidirectional**, with
  respiration → pulse the net-dominant direction in **15/20** subjects. It reproduces the
  field-standard `statsmodels.tsa.stattools.grangercausalitytests` to **~3.5e-7** (an
  agreement, limited by statsmodels' intercept convention) and an independent from-scratch
  numpy OLS to **~1.8e-9** (the op's ridge floor), both directions; statsmodels' F-test
  confirms both directions overwhelmingly significant (F ≈ 54, p < 1e-100). Coverage map
  regenerated (49 cases).

# PhysioRecipes 0.6.19

* New **Coverage map** page (`coverage.qmd`) — a cross-cutting view of the whole corpus:
  every validated method, the field-standard reference it was checked against (MNE-Python,
  SciPy, GGIR, lme4, `energy`, NeuroKit2, …), and the public data used. Generated from each
  case's `case.json` by `tools/build_coverage.py` (re-run after adding a case) and linked
  from the gallery. Summarises the corpus honestly by reference kind — third-party tool,
  dataset ground truth, or established published finding: 48 cases across 21 packages, 29
  reproducing a named reference across 22 distinct references.

# PhysioRecipes 0.6.18

* New validated case `eeg-wavelet-alpha-eegmmidb` — a **Morlet-wavelet time-frequency**
  case. On real eyes-closed occipital EEG (eegmmidb S001R02, O1),
  `PhysioAnalysis::waveletTransform` computes the Morlet scalogram, which is dominated by
  the alpha rhythm (peak at 10 Hz, 66% of power in the 8–13 Hz band) — the classic Berger
  alpha resolved in time-frequency. It reproduces MNE-Python's `tfr_array_morlet` in
  time-frequency structure to correlation **0.9998** (full TFR) / **0.9999** (marginal
  spectrum), up to a normalization convention (~0.49×) — an agreement fold (independent
  Morlet implementations), not a machine-precision match.

# PhysioRecipes 0.6.17

* New validated case `hrv-dfa-aging-fantasia` — an **HRV detrended fluctuation
  analysis (DFA) / aging** case. On real Fantasia ECG, `PhysioECG::ecgDFA` recovers
  the fractal scaling of heart-rate dynamics: the short-term exponent α1 is **1.05 in
  young** (healthy 1/f fractal scaling ~1.0) and **1.41 in elderly** subjects — the
  age-related loss of fractal complexity (aging effect +0.36, every elderly subject
  above the young mean; Iyengar et al. 1996). ecgDFA reproduces an independent
  log-spaced standard-DFA (a different least-squares fitter) to machine precision (max
  |diff| = 1.3×10⁻¹⁴). This case exercises the ecgDFA log-spaced-scales bug fix
  (PhysioECG 0.3.2) — before it, ecgDFA returned NA on these long RR series.

# PhysioRecipes 0.6.16

* New validated case `eeg-lz-sleep-consciousness-sleepedf` — a **Lempel-Ziv complexity /
  consciousness-gradient** case. On a real overnight EEG (Sleep-EDF SC4001, Fpz-Cz),
  `PhysioEEG::eegComplexity(measures = "lempel_ziv")` shows cortical complexity is lowest
  in deep sleep (N3 = **0.364**) and highest in wake and REM (**0.464**), N2 intermediate
  (0.420) — the consciousness gradient (Lempel-Ziv is the basis of the Perturbational
  Complexity Index). Because LZ is an exactly-defined algorithm, it reproduces the
  canonical Python **antropy.lziv_complexity** to machine precision (max |diff| =
  5.6×10⁻¹⁷ across all stages), extending the permutation-entropy validation to a second
  exactly-defined complexity measure.

# PhysioRecipes 0.6.15

* New validated case `emg-hilbert-envelope-grabmyo` — an **EMG muscle-activation
  envelope** case. On a real 32-channel forearm-EMG gesture (GRABMyo),
  `PhysioEMG::emgEnvelope(method = "hilbert")` extracts the muscle-activation envelope
  (peak/mean modulation 6.5 — the gesture's burst activity). Because the analytic
  signal is an exactly-defined FFT operation, it reproduces the canonical
  **`scipy.signal.hilbert`** to **machine precision** (max |diff| = 5.6×10⁻¹⁶ over all
  32 channels). This upgrades emgEnvelope's validation from the RMS method (checked vs
  a naive moving-window reference) to the Hilbert method (checked vs scipy, grade A).

# PhysioRecipes 0.6.14

* New validated case `coherence-cardiac-bidmc` — a **spectral-connectivity
  (coherence)** case. On real simultaneous PPG + ECG (BIDMC subject 01),
  `PhysioCrossModal::coherence` shows the two different cardiac sensors — optical
  (PPG) and electrical (ECG) — cohere at the heart rate: magnitude-squared coherence
  peaks at **0.898 at 1.465 Hz (88 bpm)**, far above the 95% confidence limit. It
  reproduces the canonical **`scipy.signal.coherence`** to machine precision (max
  |diff| = 2.9×10⁻¹⁴ over the full spectrum, Welch settings matched exactly).
  Honest scope: the op does not detrend, so the finding is read in the cardiac band
  (0.5–5 Hz), excluding the DC component.

# PhysioRecipes 0.6.13

* New validated case `cca-gait-wbds` — a **canonical correlation analysis** case,
  completing a three-lens cross-modal trilogy on the same WBDS gait data. On real
  walking, `PhysioCrossModal::cca` finds the maximal LINEAR correlation between the
  kinematics (knee+ankle flexion) and kinetics (GRF): first canonical correlation
  **0.737** (5-subject 0.74–0.85), reproducing base R's **`stats::cancor`** to machine
  precision (max |diff| = 1.1×10⁻¹⁶). Notably r1 ≈ the distance correlation on the same
  data (0.72), indicating the coupling is largely linear. With the dCor case (any
  dependence, 0.72) and the RSA case (rank geometry, 0.34), the identical data is now
  read through three lenses, each validated against a different canonical reference
  (energy::dcor / vegan::mantel / stats::cancor).

# PhysioRecipes 0.6.12

* New validated case `circular-gait-coupling-wbds` — a **circular (directional)
  statistics** case. On real WBDS walking, `PhysioCore::circularSummary` analyses the
  knee-ankle vector-coding coupling angles — inter-joint coordination as directional
  data: mean coordination direction **254°**, mean resultant length **R̄ = 0.195**
  (Rayleigh p = 3×10⁻⁸), with the coordination consistency varying across subjects
  (R̄ 0.06–0.29). It reproduces the canonical R **`circular`** package to machine
  precision: R̄ matches **exactly** (|diff| = 0), the mean direction to 6×10⁻¹⁴. Honest
  scope: the Rayleigh-test p-value is an asymptotic approximation and the two libraries'
  higher-order series differ slightly (both p ~ 3×10⁻⁸) — reported, not claimed exact.

# PhysioRecipes 0.6.11

* New validated case `eeg-permutation-entropy-eegmmidb` — an **EEG signal-complexity**
  case. On all 64 channels of real eyes-closed resting EEG (eegmmidb S001R02),
  `PhysioEEG::eegComplexity` computes the **permutation entropy** (Bandt-Pompe) — a
  marker of cortical state, consciousness, and anaesthesia depth. Because permutation
  entropy is an exactly-defined algorithm, it reproduces the canonical Python
  **antropy** to **machine precision**: correlation 1.0, max |difference| = 2×10⁻¹⁶
  across the 64 channels, mean entropy 0.91. Honest scope: the tolerance-dependent
  sample entropy and PSD-dependent spectral entropy do NOT match antropy exactly
  (~0.01–0.02) and are deliberately not claimed — only the exactly-defined measure is.

# PhysioRecipes 0.6.10

* New validated case `eeg-pac-sleep-spindle-sleepedf` — a **phase-amplitude
  coupling** case on real NREM sleep EEG. On an overnight polysomnogram (Sleep-EDF
  SC4001, Fpz-Cz), `PhysioCrossModal::phaseAmplitudeCoupling` measures the
  slow-oscillation↔spindle coupling — the hallmark cross-frequency coupling of
  memory-consolidation sleep: Tort modulation index **0.00035**, **z = 9.6** above a
  circular-shift surrogate null (exceeds all 200 surrogates). It reproduces the
  canonical Python **tensorpac** to machine precision (|difference| = 5×10⁻¹⁷), fed
  the identical phase and amplitude. Honest scope: the surrogate null (not a non-zero
  MI) establishes the coupling is real; single subject, single channel.

# PhysioRecipes 0.6.9

* New validated case `rsa-mantel-gait-wbds` — a **representational similarity
  analysis (RSA) / Mantel test** case. On real WBDS treadmill walking (Fukuchi et
  al. 2018), `PhysioCrossModal::representationalSimilarity` correlates the
  dissimilarity matrices (RDMs) of the gait kinematics (knee+ankle flexion) and
  kinetics (GRF): Mantel **r = 0.34** (permutation p = 0.010) for one subject and
  **0.34–0.49** (mean 0.38) across all five — a moderate, significant
  representational correspondence. It reproduces the canonical **`vegan::mantel`
  exactly** (|difference| = 0). Notably weaker than the distance correlation on the
  same data (0.72): RSA is a rank correlation of distance matrices, a distinct and
  more conservative measure — both reported for an honest picture.

# PhysioRecipes 0.6.8

* New validated case `eeg-aperiodic-exponent-eegmmidb` — a **qEEG aperiodic
  (1/f) parameterization** case. On all 64 channels of real eyes-closed resting
  EEG (eegmmidb S001R02, PhysioNet), `PhysioEEG::eegAperiodic` (the specparam /
  FOOOF engine, Donoghue et al. 2020) recovers the aperiodic **exponent** — a
  widely-used marker of cortical excitation/inhibition balance. Fed the identical
  per-channel Welch PSD, it reproduces the canonical Python **fooof**: the
  per-channel exponents correlate **r = 0.98** across the 64 channels, mean
  \|difference\| **0.07**, both engines yielding physiologically plausible resting
  exponents (specparam 1.38, fooof 1.45; mean fit R² = 0.93). Honest boundary: an
  agreement benchmark (independent iterative implementations), with the largest
  divergence at the occipital electrodes where a strong alpha peak makes the two
  peak-removal heuristics differ.

# PhysioRecipes 0.6.7

* New validated case `crossmodal-dcor-gait-wbds` — a **cross-modal dependence**
  case. On real WBDS treadmill walking (Fukuchi et al. 2018), the distance
  correlation (Székely, Rizzo & Bakirov 2007) between the sagittal knee+ankle
  flexion angles (kinematics) and the antero-posterior+vertical GRF (kinetics) is
  **dCor = 0.72** (permutation p = 0.001) for one subject and **0.71–0.78** (mean
  0.74) across all five — a strong, significant, consistent coupling. The
  ecosystem's `PhysioCrossModal::distanceCorrelation` reproduces the canonical
  `energy::dcor` to machine precision (|diff| < 1e-13), so the measure is exact,
  not approximate. Distance correlation is zero iff the blocks are independent and,
  unlike Pearson or linear canonical correlation, detects dependence of any shape.

# PhysioRecipes 0.6.6

* New validated case `msknet-hypergraph-murphy` — the ecosystem's first
  **musculoskeletal-network** case. Building the whole-body muscle-bone hypergraph
  with `PhysioMSKNet` (`loadMSKData` -> `MSKHypergraph` -> `mskHomuncCorrelation`)
  reproduces Murphy et al. (2018, PLoS Biology): the paper-scale hypergraph (173
  bones, 270 muscles) and its central neuro-anatomical finding — a muscle's
  structural IMPACT corresponds to its cortical motor-HOMUNCULUS representation,
  R² = 0.517 (F = 20.4, p = 2.4e-4 over 21 regions), matching the paper's 0.52
  (F = 21.3). Honest scope: the impact-vs-recovery clinical model reproduces the
  significant positive direction but a lower R² (0.41 vs the paper's 0.76). 36 cases.

# PhysioRecipes 0.6.5

* New validated case `tms-eeg-tep-tesa` — the ecosystem's first **TMS
  neurophysiology** case. From the real TESA TMS-EEG recording (150 pulses,
  59-channel EEG; figshare 3188800), `PhysioNeurophys::setTMSpulses` +
  `tepAverage` recover the canonical **TMS-evoked potential (TEP)** component
  sequence: all six components (N15/P30/N45/P60/N100/P180) in the correct
  temporal ORDER (median latencies 16 < 31 < 45 < 66 < 115 < 188 ms,
  monotonically increasing) and with the correct POLARITIES (peak sign matches
  the expected N/P in 88–97 % of channels, mean 92 %), the N100 (~115 ms) and
  P180 (~188 ms) at their literature latencies. Honest scope: single
  participant, parietal (not motor) stimulation, and the case validates
  component EXTRACTION (the source data was already pulse-artifact-cut) — not
  TMS-artifact removal. (H-reflex was targeted too, but no public recruitment
  dataset was available; the TMS side is folded here.) 35 cases.

# PhysioRecipes 0.6.4

* New validated case `netphys-sleep-network-sleepedf` — the ecosystem's first
  **network-physiology** case (a new modality). A 6-node **time-delay-stability
  (TDS)** network (EEG delta/alpha/sigma + EOG/EMG/respiration) is built from one
  real overnight polysomnogram (Sleep-EDF Expanded) with the full PhysioNetPhysiology
  TDS stack (`physioNodeMatrix` → `timeDelayStability` → `tdsNetwork(surrogate)` →
  `tdsNetworkByState` → `tdsReconfiguration`) and split by sleep stage, reproducing
  the field's signature finding: the physiological network **reconfigures across
  sleep stages** — most integrated in REM (11 surrogate-significant links, density
  0.73) and least in wake/light sleep (9, 0.60); the EEG-delta rhythm is the
  persistent hub; and 6/15 couplings change between wake and REM. Links are kept
  only if they beat a phase-randomised surrogate threshold. Honest scope: single
  subject/night (the reconfiguration is the robust phenomenon; exact counts are
  subject-specific), deterministic given seed=1. 34 cases.

# PhysioRecipes 0.6.3

* New validated case `fnirs-activation-motor-mne` — the ecosystem's first **fNIRS**
  case, and a whole new modality. The full PhysioNIRS pipeline (`readSNIRF` →
  `intensityToOD` → `mbll` → `nirsActivationGLM` → `nirsActivationContrast`) is run
  on a real public finger-tapping recording (MNE-Python `fnirs_motor`) and validated
  at two points: (1) CROSS-TOOL — `mbll()` reproduces MNE-Python's
  `beer_lambert_law()` to **machine precision** (correlation 1.000 in all 28
  channels; only µM-vs-M units differ); (2) PHYSIOLOGY — the GLM recovers the
  canonical motor-activation signature, a task-evoked **HbO increase** (grand-average
  peak +0.21 µM at ~5 s, significant in 18/28 channels) with a concurrent **HbR
  decrease** (25/28). Honest scope: single subject; Tapping-vs-Control pools the two
  hands (contralateral localisation left as an open question). 33 cases.

# PhysioRecipes 0.6.2

* New validated case `gait-inverse-dynamics-fukuchi` — turning measured motion
  into joint kinetics and validating it against a real ground truth. Driving
  `PhysioMoCap::inverseDynamics2D()` (Newton-Euler, de Leva inertia) with the WBDS
  markers + ground reaction force, the recovered sagittal joint moments are
  validated against the dataset's OWN independently-computed moments (the `knt`
  files) and reproduce the expected **distal-to-proximal accuracy gradient**:
  ankle r = 0.97, knee r = 0.85, hip r = 0.77 (mean over 5 subjects), with a
  physiological ankle push-off peak (~1.66 N·m/kg reference). Honest scope: 2-D
  sagittal only, and the hip peak inflates because the greater-trochanter marker is
  a crude hip-centre proxy — reported, not hidden. 32 cases.

# PhysioRecipes 0.6.1

* New validated case `cohort-longitudinal-parkinsons-updrs` — the first
  genuinely-longitudinal real-patient cohort case: on the public UCI Parkinson's
  Telemonitoring data (42 patients, ~5,875 recordings over 6 months),
  `PhysioClinStats::fitMixedModel()` reproduces the reference engine `lme4::lmer()`
  byte-identically (max fixed-effect diff = 0, matching random-intercept SD), and
  `PhysioCore::PhysioCohort` carries the 42-subject container end-to-end. Fills the
  audit's real-patient-cohort maturity gap (honest scope: voice not gait; summary
  UPDRS; validated claim = reference-engine reproduction).

