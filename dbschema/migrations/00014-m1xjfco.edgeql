CREATE MIGRATION m1xjfcoto7c6vtmoy2vatozdggwcm5ao7za5z34xf5h6gkf6irksgq
    ONTO m1o555kniccecwsdndijjuy4hsdcdgle2ldxmw7z6lp7nyagvx3oca
{
  ALTER TYPE Paper::Comment {
      CREATE REQUIRED PROPERTY content: std::str {
          SET REQUIRED USING (<std::str>{});
      };
  };
};
