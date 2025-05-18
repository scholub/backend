with
  comment := (select Comment::Comment filter .id = <uuid>$comment_id limit 1),
  user := (select User filter .id = <uuid>$user_id limit 1),
delete Comment::Reaction filter .comment = comment and .user = user;
update Comment::Comment filter .id = <uuid>$comment_id set {
  like_count := count((select Comment::Reaction filter .comment.id = <uuid>$comment_id and .is_like = true)),
  dislike_count := count((select Comment::Reaction filter .comment.id = <uuid>$comment_id and .is_like = false))
};

