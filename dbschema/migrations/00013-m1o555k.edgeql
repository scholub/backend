CREATE MIGRATION m1o555kniccecwsdndijjuy4hsdcdgle2ldxmw7z6lp7nyagvx3oca
    ONTO m1znlld3ymyrvccnnbmwptqirkmgi2dm7skh5u5dftz3tng5tl7pzq
{
  ALTER TYPE default::User {
      CREATE REQUIRED PROPERTY name: std::str {
          SET REQUIRED USING (<std::str>{.email});
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
