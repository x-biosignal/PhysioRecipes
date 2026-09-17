#' Root directory holding the case studies
#'
#' Resolves `inst/cases` whether the package is installed or loaded from source.
#' @return Absolute path to the directory that contains one sub-directory per case.
#' @keywords internal
cases_root <- function() {
  p <- system.file("cases", package = "PhysioRecipes")
  if (nzchar(p) && dir.exists(p)) return(p)
  stop("PhysioRecipes cases/ directory not found (looked in system.file('cases')).",
       call. = FALSE)
}

#' Read a single case record
#'
#' @param id Case id (the case sub-directory name, e.g. `"ecg-hrv-mitbih"`).
#' @return The parsed `case.json` as a list.
#' @export
#' @examples
#' if (length(list.files(system.file("cases", package = "PhysioRecipes"))))
#'   str(get_case(list_cases()$id[1]), max.level = 1)
get_case <- function(id) {
  f <- file.path(cases_root(), id, "case.json")
  if (!file.exists(f)) stop("No such case: ", id, call. = FALSE)
  jsonlite::read_json(f, simplifyVector = FALSE)
}

#' Path to a case directory or one of its files
#'
#' @param id Case id.
#' @param ... Optional path components under the case directory
#'   (e.g. `"bundle"`, `"bundle", "prereg.json"`).
#' @return An absolute path.
#' @export
case_path <- function(id, ...) {
  root <- file.path(cases_root(), id)
  if (!dir.exists(root)) stop("No such case: ", id, call. = FALSE)
  if (length(list(...))) file.path(root, ...) else root
}

#' Path to a case's verified run bundle
#'
#' The substrate bundle (frozen pre-registration, run manifest, op-DAG, terminal
#' artifact, claims and verification report) — the evidence a reader re-runs or
#' audits. The same shape [PhysioLake::physioPutBundle()] stores with lineage.
#'
#' @param id Case id.
#' @return Absolute path to the case's `bundle/` directory.
#' @export
case_bundle <- function(id) case_path(id, "bundle")

#' The case database as one row per case
#'
#' Browse the whole corpus: id, title, modality, ecosystem packages exercised,
#' dataset, reproducibility status and whether the case escalates an open question
#' to a paper.
#'
#' @return A `data.frame`, one row per case.
#' @export
#' @examples
#' if (length(list.files(system.file("cases", package = "PhysioRecipes"))))
#'   list_cases()
list_cases <- function() {
  ids <- list.dirs(cases_root(), full.names = FALSE, recursive = FALSE)
  ids <- ids[file.exists(file.path(cases_root(), ids, "case.json"))]
  if (!length(ids)) {
    return(data.frame(id = character(), title = character(), modality = character(),
                      packages = character(), dataset = character(), status = character(),
                      n_grounded = integer(), n_claims = integer(),
                      replay_byte_identical = logical(), escalated = logical(),
                      stringsAsFactors = FALSE))
  }
  rows <- lapply(ids, function(id) {
    c1 <- get_case(id)
    v <- c1$verification
    esc <- any(vapply(c1$open_questions %||% list(),
                      function(q) !is.null(q$escalate), logical(1)))
    data.frame(
      id = id,
      title = c1$title %||% NA_character_,
      modality = paste(unlist(c1$modality), collapse = ", "),
      packages = paste(unlist(c1$packages), collapse = ", "),
      dataset = c1$dataset$name %||% NA_character_,
      status = c1$status %||% NA_character_,
      n_grounded = as.integer(v$n_grounded %||% NA),
      n_claims = as.integer(v$n_claims %||% NA),
      replay_byte_identical = isTRUE(v$replay_byte_identical),
      escalated = esc,
      stringsAsFactors = FALSE)
  })
  do.call(rbind, rows)
}

#' Cases that escalate an open question to a paper
#'
#' The research queue: cases whose `open_questions` carry an `escalate` target.
#' @return A `data.frame` of id, title and escalation target(s).
#' @export
escalations <- function() {
  ids <- list_cases()$id
  out <- list()
  for (id in ids) {
    c1 <- get_case(id)
    for (q in c1$open_questions %||% list()) {
      if (!is.null(q$escalate)) {
        out[[length(out) + 1L]] <- data.frame(
          id = id, target = q$escalate,
          question = substr(q$q %||% "", 1, 160), stringsAsFactors = FALSE)
      }
    }
  }
  if (!length(out)) return(data.frame(id = character(), target = character(),
                                      question = character(), stringsAsFactors = FALSE))
  do.call(rbind, out)
}

#' Check the invariants every case must satisfy
#'
#' Structural gate (dataset is public; every claim is GROUNDED in the case's
#' `verification_report.json`; `n_grounded == n_claims`; a byte-identical replay is
#' recorded; a `verified`/`escalated` case has all claims grounded). The
#' pre-registration hash and per-case number tracing are checked by
#' `tools/validate_case.py` in CI.
#'
#' @param ids Cases to check (default: all).
#' @return A `data.frame` with one row per case and a logical `ok` column.
#' @export
validate_cases <- function(ids = list_cases()$id) {
  chk <- function(id) {
    c1 <- get_case(id)
    reasons <- character(0)
    if (!isTRUE(c1$dataset$public)) reasons <- c(reasons, "dataset not public")
    if (length(c1$claims) == 0L) reasons <- c(reasons, "no claims")
    # embargo: a public case must not escalate an unresolved question to a paper
    if (any(vapply(c1$open_questions %||% list(),
                   function(q) !is.null(q$escalate), logical(1))))
      reasons <- c(reasons, "escalated (embargo: keep unresolved->paper cases private)")
    if (identical(c1$status, "validated")) {
      v <- c1$validation
      if (is.null(v)) reasons <- c(reasons, "missing validation block")
      else {
        if (!grepl("REAL", toupper(v$data %||% ""))) reasons <- c(reasons, "validation not REAL data")
        if (!isTRUE(v$all_pass)) reasons <- c(reasons, "validation.all_pass not TRUE")
        if (is.null(v$reference)) reasons <- c(reasons, "validation names no reference")
      }
    } else {  # verified (strict): substrate bundle
      v <- c1$verification
      vr_path <- file.path(cases_root(), id, c1$bundle %||% "bundle",
                           "verification_report.json")
      vr <- if (file.exists(vr_path)) jsonlite::read_json(vr_path, simplifyVector = FALSE) else NULL
      if (!isTRUE(v$replay_byte_identical)) reasons <- c(reasons, "no byte-identical replay")
      if (is.null(vr)) reasons <- c(reasons, "missing verification_report.json")
      else {
        grounded <- sum(vapply(vr$claims, function(x) identical(x$status, "GROUNDED"), logical(1)))
        if (!identical(as.integer(grounded), length(c1$claims)) ||
            !identical(as.integer(v$n_grounded), length(c1$claims)))
          reasons <- c(reasons, "not all claims GROUNDED")
      }
    }
    data.frame(id = id, status = c1$status %||% NA_character_,
               ok = length(reasons) == 0L,
               reason = paste(reasons, collapse = "; "), stringsAsFactors = FALSE)
  }
  do.call(rbind, lapply(ids, chk))
}

`%||%` <- function(a, b) if (is.null(a)) b else a
