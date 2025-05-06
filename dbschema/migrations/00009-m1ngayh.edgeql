CREATE MIGRATION m1ngayhgw5qsp5iig6xri72k5vwi7ciky7ro4l32j3ezabkpjajrlq
    ONTO m1bwum7tt62xnsemode6tigocxzecumyu5kl66ssw4k6kloxuf7r5a
{
  ALTER TYPE Paper::Paper {
      DROP LINK tag;
  };
  ALTER TYPE Paper::Paper {
      CREATE REQUIRED PROPERTY tag: std::str {
          SET REQUIRED USING (<std::str>{});
      };
  };
  ALTER TYPE Paper::Post {
      DROP LINK tag;
  };
  ALTER TYPE Paper::Post {
      CREATE REQUIRED PROPERTY tag: std::str {
          SET REQUIRED USING (<std::str>{});
      };
  };
  DROP TYPE Paper::Tag;
};
