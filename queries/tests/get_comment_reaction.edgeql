select Comment::Comment {
  like_count,
  dislike_count
} filter .id = <uuid>$id;
