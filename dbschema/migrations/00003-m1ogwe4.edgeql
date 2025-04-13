CREATE MIGRATION m1ogwe4ckyezv7qyj2ouxmettsxnhkyn2vkwpfkyi5smtq33db4kka
    ONTO m1oehniydt5ki23agmxhyjdueawnuwdobrc7bzqtjh44xr3bglq3zq
{
  ALTER TYPE default::Paper {
      ALTER PROPERTY paper_id {
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
