select Paper::Cache {
  created
} filter .paper_id = <str>$paper_id limit 1;

