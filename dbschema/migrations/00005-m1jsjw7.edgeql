CREATE MIGRATION m1jsjw7kkzp5qzx6e6l77agfpqr7fjxrcn4algi4bu5gayokl5qzua
    ONTO m1b7mlhfyapo4bqltcanofeirg3t5sznsjumwqtktkix5a4rguwbsa
{
  CREATE TYPE default::User {
      CREATE REQUIRED PROPERTY email: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY password: std::str;
  };
};
