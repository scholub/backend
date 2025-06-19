select User {
  name, email, password, bookmarks
} filter .email = <str>$email limit 1;

