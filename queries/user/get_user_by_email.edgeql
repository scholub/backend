select User {
  name, email, password
} filter .email = <str>$email limit 1;

