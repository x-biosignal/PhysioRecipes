test_that("the case database lists cases and enforces invariants", {
  cases <- list_cases()
  expect_gt(nrow(cases), 0)
  expect_true(all(c("id", "title", "status", "n_grounded") %in% names(cases)))

  # every shipped case must satisfy the invariants
  v <- validate_cases()
  expect_true(all(v$ok), info = paste(v$id[!v$ok], v$reason[!v$ok], collapse = " | "))
})

test_that("get_case resolves a known case", {
  id <- list_cases()$id[1]
  cj <- get_case(id)
  expect_true(isTRUE(cj$dataset$public))
})

test_that("verified-tier cases ship a replay bundle with a verification report", {
  cases <- list_cases()
  vid <- cases$id[cases$status == "verified"]
  # the strict (verified) tier is the one that carries a byte-identical replay
  # bundle; validated-tier cases carry a validation block + audit instead.
  skip_if(length(vid) == 0L, "no verified-tier cases in the database")
  for (id in vid) {
    expect_true(dir.exists(case_bundle(id)), info = id)
    expect_true(file.exists(file.path(case_bundle(id), "verification_report.json")),
                info = id)
  }
})

test_that("escalations() returns a well-formed research queue", {
  e <- escalations()
  expect_true(all(c("id", "target", "question") %in% names(e)))
})
