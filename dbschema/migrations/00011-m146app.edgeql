CREATE MIGRATION m146appscsuwmwocj3pwxhfghii3iaf5fr7a6sns7vpz5gq3alqzyq
    ONTO m1cxyyawmrnmhv2arrklc5nsgphgcck2ztg5gkrcw4lkj37yrtk6kq
{
  CREATE TYPE Paper::Reaction {
      CREATE REQUIRED LINK post: Paper::Post;
      CREATE REQUIRED LINK user: default::User;
      CREATE CONSTRAINT std::exclusive ON ((.user, .post));
      CREATE REQUIRED PROPERTY is_like: std::bool;
  };
};
