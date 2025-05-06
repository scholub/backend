select Paper::Comment {
  user,
  created,
  like_count,
  dislike_count
} filter .id = <uuid>$id;
