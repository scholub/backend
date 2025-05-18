select Paper::Post {
  title,
  description,
  paper_id,
  category,
  tag,
  created,
  modified,
  like_count,
  dislike_count
} filter .paper_id = <str>$paper_id;
