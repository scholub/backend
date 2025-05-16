select Paper::Post {
  comments: {
    created,
    dislike_count,
    like_count,
    content,
    user: { id, name, email }
  }
} filter .id = <uuid>$post_id;
