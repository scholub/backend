select Paper::Post {
  like_count,
  dislike_count
} filter .paper_id = <str>$paper_id;