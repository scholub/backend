update Paper::Post
filter .paper_id = <str>$paper_id
set {
  comments += (
    insert Comment::Comment {
      created := datetime_current(),
      content := <str>$content,
      user := (select User filter .id = <uuid>$user_id)
    }
  )
};
