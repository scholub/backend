select Paper::Post {
  comments: {
    id,
    created,
    dislike_count,
    like_count,
    content,
    user: { id, name, email }
  }
} filter .paper_id = <str>$paper_id;
