select User {
  name, email, password, bookmarks: {
    paper_id,
    embedding
  }
} filter .email = <str>$email limit 1;

