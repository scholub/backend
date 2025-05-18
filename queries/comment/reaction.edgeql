with
  comment := (select Comment::Comment filter .id = <uuid>$comment_id limit 1),
  user := (select User filter .id = <uuid>$user_id limit 1),
insert Comment::Reaction {
  is_like := <bool>$is_like,
  user := user,
  comment := comment
} unless conflict on ((.user, .comment)) else (
  update Comment::Reaction filter .user = user and .comment = .comment set {
    is_like := <bool>$is_like
  }
);
update Comment::Comment filter .id = <uuid>$comment_id set {
  like_count := count((select Comment::Reaction filter .comment.id = <uuid>$comment_id and .is_like = true)),
  dislike_count := count((select Comment::Reaction filter .comment.id = <uuid>$comment_id and .is_like = false))
};

