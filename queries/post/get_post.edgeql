select Paper::Post {
  title,
  body,
  tag,
  created,
  modified,
  like_count,
  dislike_count,
  comments
} filter .id = <uuid>$id;
