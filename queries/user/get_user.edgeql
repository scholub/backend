select User {
  email, password
} filter .id = <uuid>$id limit 1;

