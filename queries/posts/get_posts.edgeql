select Paper::Post {
  title,
  description,
  paper_id
} order by (.like_count - .dislike_count) desc;
