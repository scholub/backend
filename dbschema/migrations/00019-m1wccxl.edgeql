CREATE MIGRATION m1wccxlii6llqpkkrvgylootelgmiwn6tcqvnfukk5ovjyqmqoee3q
    ONTO m13svz72o5ena6tzzevkz7kguitrlejyh5nq3g5gcveubihwebiuga
{
  ALTER TYPE Paper::Post {
      ALTER PROPERTY category {
          SET OWNED;
      };
      ALTER PROPERTY description {
          SET OWNED;
      };
      ALTER PROPERTY paper_id {
          ALTER CONSTRAINT std::exclusive {
              SET OWNED;
          };
          SET OWNED;
      };
      ALTER PROPERTY tag {
          SET OWNED;
      };
      ALTER PROPERTY title {
          SET OWNED;
      };
      DROP EXTENDING Paper::Paper;
  };
  ALTER TYPE Paper::Paper {
      DROP PROPERTY category;
      DROP PROPERTY description;
      DROP PROPERTY paper_id;
      DROP PROPERTY tag;
      DROP PROPERTY title;
  };
  ALTER TYPE Paper::Post {
      ALTER PROPERTY category {
          RESET readonly;
          RESET CARDINALITY;
          SET REQUIRED;
          SET TYPE std::str;
      };
      ALTER PROPERTY description {
          RESET readonly;
          RESET CARDINALITY;
          SET REQUIRED;
          SET TYPE std::str;
      };
      ALTER PROPERTY paper_id {
          RESET readonly;
          RESET CARDINALITY;
          SET REQUIRED;
          SET TYPE std::str;
      };
      ALTER PROPERTY tag {
          RESET readonly;
          RESET CARDINALITY;
          SET REQUIRED;
          SET TYPE std::str;
      };
      ALTER PROPERTY title {
          RESET readonly;
          RESET CARDINALITY;
          SET REQUIRED;
          SET TYPE std::str;
      };
  };
  DROP TYPE Paper::Paper;
};
