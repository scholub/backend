update Paper::Post
filter .id = <uuid>$post_id
set {
  comments += (
    insert Paper::Comment {
      created := datetime_current(),
      content := <str>$content,
      user := (select User filter .id = <uuid>$user_id)
    }
  )
};
