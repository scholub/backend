select Cache {
  paper_id,
  modified
} filter .paper_id = <str>$paper_id limit 1;
