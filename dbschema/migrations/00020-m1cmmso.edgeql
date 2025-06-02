CREATE MIGRATION m1cmmsolaen7qizf7r2ehs7nzg6d55bhwkfw7rsjja4sl7qme4o4aa
    ONTO m1wccxlii6llqpkkrvgylootelgmiwn6tcqvnfukk5ovjyqmqoee3q
{
  CREATE TYPE Paper::Cache {
      CREATE REQUIRED PROPERTY created: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY paper_id: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  ALTER TYPE Paper::Post EXTENDING Paper::Cache LAST;
  ALTER TYPE Paper::Post {
      ALTER PROPERTY created {
          RESET OPTIONALITY;
          DROP OWNED;
          RESET TYPE;
      };
      ALTER PROPERTY paper_id {
          ALTER CONSTRAINT std::exclusive {
              DROP OWNED;
          };
          RESET OPTIONALITY;
          DROP OWNED;
          RESET TYPE;
      };
  };
};
