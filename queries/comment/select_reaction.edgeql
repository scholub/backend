with
  comment := (select Comment::Comment filter .id = <uuid>$comment_id limit 1),
  user := (select User filter .id = <uuid>$user_id limit 1),
select Comment::Reaction {
  is_like
} filter .comment = comment and .user = user limit 1;
