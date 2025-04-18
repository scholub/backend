select (insert Cache {
  paper_id := <str>$paper_id,
  modified := <datetime>$modified
} unless conflict on .paper_id else (
  select (update Cache set {
    modified := <datetime>$modified
  })
)) {paper_id, modified};

