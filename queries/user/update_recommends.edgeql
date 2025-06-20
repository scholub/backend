update User
filter .email = <str>$email
set {
  recommends := (
    select Paper::Post
    filter .id in array_unpack(<array<uuid>>$recommends)
  )
};
