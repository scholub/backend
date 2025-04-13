CREATE MIGRATION m1w4qms77qsaxyzcz3ca4wnjbh62mzbr77t54gk5uigrxv26sd6hka
    ONTO initial
{
  CREATE FUTURE simple_scoping;
  CREATE TYPE default::Paper {
      CREATE REQUIRED PROPERTY modified: std::str;
      CREATE REQUIRED PROPERTY paper_id: std::str;
  };
};
