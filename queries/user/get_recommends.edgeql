select User {
  recommends: { paper_id }
} filter .email = <str>$email;

