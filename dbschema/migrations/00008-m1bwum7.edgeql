CREATE MIGRATION m1bwum7tt62xnsemode6tigocxzecumyu5kl66ssw4k6kloxuf7r5a
    ONTO m1u7njhcakl3ejg7ev3mqixcoh3kztpoaj7azkcji3mihrs3jk5ruq
{
  CREATE TYPE Paper::Comment {
      CREATE REQUIRED LINK user: default::User;
      CREATE REQUIRED PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY dislike_count: std::int64 {
          SET default := 0;
      };
      CREATE REQUIRED PROPERTY like_count: std::int64 {
          SET default := 0;
      };
  };
  CREATE TYPE Paper::Tag {
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE REQUIRED PROPERTY subtag: std::str;
  };
  CREATE TYPE Paper::Post {
      CREATE MULTI LINK comments: Paper::Comment;
      CREATE REQUIRED LINK tag: Paper::Tag;
      CREATE REQUIRED PROPERTY body: std::str;
      CREATE REQUIRED PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY dislike_count: std::int64 {
          SET default := 0;
      };
      CREATE REQUIRED PROPERTY like_count: std::int64 {
          SET default := 0;
      };
      CREATE REQUIRED PROPERTY modified: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY title: std::str;
  };
  ALTER TYPE Paper::Paper {
      CREATE REQUIRED LINK tag: Paper::Tag {
          SET REQUIRED USING (<Paper::Tag>{});
      };
  };
  ALTER TYPE Paper::Paper {
      DROP PROPERTY keywords;
  };
};
