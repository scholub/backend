with
  post := (select Paper::Post filter .paper_id = <str>$paper_id limit 1),
  user := (select User filter .id = <uuid>$user_id limit 1),
select Paper::Reaction {
  is_like
} filter .post = post and .user = user limit 1;
