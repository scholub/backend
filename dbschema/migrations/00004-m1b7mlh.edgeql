CREATE MIGRATION m1b7mlhfyapo4bqltcanofeirg3t5sznsjumwqtktkix5a4rguwbsa
    ONTO m1ogwe4ckyezv7qyj2ouxmettsxnhkyn2vkwpfkyi5smtq33db4kka
{
  CREATE TYPE default::Cache {
      CREATE REQUIRED PROPERTY modified: std::datetime;
      CREATE REQUIRED PROPERTY paper_id: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  ALTER TYPE default::Paper {
      CREATE REQUIRED PROPERTY category: std::str {
          SET REQUIRED USING (<std::str>{});
      };
  };
  ALTER TYPE default::Paper {
      CREATE REQUIRED PROPERTY description: std::str {
          SET REQUIRED USING (<std::str>{});
      };
  };
  ALTER TYPE default::Paper {
      CREATE MULTI PROPERTY keywords: std::str;
  };
  ALTER TYPE default::Paper {
      DROP PROPERTY modified;
  };
  ALTER TYPE default::Paper {
      CREATE REQUIRED PROPERTY name: std::str {
          SET REQUIRED USING (<std::str>{});
      };
  };
};
