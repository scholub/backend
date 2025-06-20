with 
  user := (select User filter .email = <str>$email),
  papers := (select Paper::Post filter .id in array_unpack(<array<uuid>>$recommendation))
update User 
filter .email = <str>$email
set {
  recommends := papers
};
