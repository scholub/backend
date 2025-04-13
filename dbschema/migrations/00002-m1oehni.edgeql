CREATE MIGRATION m1oehniydt5ki23agmxhyjdueawnuwdobrc7bzqtjh44xr3bglq3zq
    ONTO m1w4qms77qsaxyzcz3ca4wnjbh62mzbr77t54gk5uigrxv26sd6hka
{
  ALTER TYPE default::Paper {
      ALTER PROPERTY modified {
          SET TYPE std::datetime USING (<std::datetime>.modified);
      };
  };
};
