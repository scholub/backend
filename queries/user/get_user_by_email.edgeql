select User {
  name,
  email,
  password,
  bookmarks: {
    paper_id,
    embedding
  },
  recommends:{
    paper_id
  },
  profile_image
} filter .email = <str>$email limit 1;

