select User {
  name,
  email,
  password,
  bookmarks: {
    paper_id,
    embedding
  },
  profile_image
} filter .email = <str>$email limit 1;

