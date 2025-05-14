select Paper::Post {
  comments: {
    created,
    dislike_count,
    like_count,
    user: { id, name, email }
  }
} filter .id = <uuid>$post_id;
