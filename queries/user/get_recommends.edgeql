select User {
  recommends: {
    paper_id,
    title,
    description
  }
} filter .email = <str>$email;

