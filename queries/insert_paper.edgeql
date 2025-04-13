insert Paper {
  paper_id := <str>$paper_id,
  modified := <datetime>$modified
} unless conflict on .paper_id else (
  select (update Paper set {
    modified := <datetime>$modified
  })
);

