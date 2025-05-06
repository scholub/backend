select User {
  email, password
} filter .email = <str>$email limit 1;

