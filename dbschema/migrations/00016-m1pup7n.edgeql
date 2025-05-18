CREATE MIGRATION m1pup7ntiotg6j2rrgrc7armxv2s4kons6x6tgaay5qepmaty3jxyq
    ONTO m1sgvxjuunriwlmvidiuaahvancbgee7t7si6yp5w4dwf4fqqt5rba
{
  CREATE TYPE Comment::Reaction {
      CREATE REQUIRED LINK comment: Comment::Comment;
      CREATE REQUIRED LINK user: default::User;
      CREATE CONSTRAINT std::exclusive ON ((.user, .comment));
      CREATE REQUIRED PROPERTY is_like: std::bool;
  };
};
