update User filter .email = <str>$email set {
  bookmarks += {
    (select Paper::Post filter .paper_id = <str>$paper_id)
  }
}
