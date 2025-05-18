CREATE MIGRATION m13svz72o5ena6tzzevkz7kguitrlejyh5nq3g5gcveubihwebiuga
    ONTO m1y5pz6gubfc4wqe3acoaggqbjoimkjcil573vhqgitftibwp5ruma
{
  ALTER TYPE Paper::Paper {
      ALTER PROPERTY name {
          RENAME TO title;
      };
  };
};
