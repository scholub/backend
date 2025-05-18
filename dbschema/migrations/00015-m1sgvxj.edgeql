CREATE MIGRATION m1sgvxjuunriwlmvidiuaahvancbgee7t7si6yp5w4dwf4fqqt5rba
    ONTO m1xjfcoto7c6vtmoy2vatozdggwcm5ao7za5z34xf5h6gkf6irksgq
{
  CREATE MODULE Comment IF NOT EXISTS;
  ALTER TYPE Paper::Comment RENAME TO Comment::Comment;
};
