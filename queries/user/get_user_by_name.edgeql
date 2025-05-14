select User {
  name, email, password
} filter .name = <str>$name limit 1;

