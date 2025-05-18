with
  post := (select Paper::Post filter .paper_id = <str>$paper_id limit 1),
  user := (select User filter .id = <uuid>$user_id limit 1),
delete Paper::Reaction filter .post = post and .user = user;
update Paper::Post filter .paper_id = <str>$paper_id set {
  like_count := count((select Paper::Reaction filter .post.paper_id = <str>$paper_id and .is_like = true)),
  dislike_count := count((select Paper::Reaction filter .post.paper_id = <str>$paper_id and .is_like = false))
};

