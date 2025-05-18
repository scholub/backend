CREATE MIGRATION m1y5pz6gubfc4wqe3acoaggqbjoimkjcil573vhqgitftibwp5ruma
    ONTO m1pup7ntiotg6j2rrgrc7armxv2s4kons6x6tgaay5qepmaty3jxyq
{
  ALTER TYPE Paper::Post {
      DROP PROPERTY body;
  };
  ALTER TYPE Paper::Post {
      CREATE PROPERTY category: std::str {
          SET REQUIRED USING (<std::str>{});
      };
  };
  ALTER TYPE Paper::Post {
      CREATE PROPERTY description: std::str {
          SET REQUIRED USING (<std::str>{});
      };
  };
  ALTER TYPE Paper::Post {
      CREATE PROPERTY name: std::str {
          SET REQUIRED USING (<std::str>{});
      };
  };
  ALTER TYPE Paper::Post {
      CREATE PROPERTY paper_id: std::str {
          SET REQUIRED USING (<std::str>{});
      };
  };
  ALTER TYPE Paper::Post {
      DROP PROPERTY title;
      EXTENDING Paper::Paper LAST;
      ALTER PROPERTY category {
          RESET OPTIONALITY;
          DROP OWNED;
          RESET TYPE;
      };
      ALTER PROPERTY description {
          RESET OPTIONALITY;
          DROP OWNED;
          RESET TYPE;
      };
      ALTER PROPERTY name {
          RESET OPTIONALITY;
          DROP OWNED;
          RESET TYPE;
      };
      ALTER PROPERTY paper_id {
          RESET OPTIONALITY;
          DROP OWNED;
          RESET TYPE;
      };
      ALTER PROPERTY tag {
          RESET OPTIONALITY;
          DROP OWNED;
          RESET TYPE;
      };
  };
};
