CREATE MIGRATION m16hffzdwo2zgpzufdo3zpx6eeq7bxnallmmyhpwfyevyusgy3vh5a
    ONTO m1l4achbrpw6rtisi5uqscymjnpz6mwhqv3rdflvmtxzhiz4gq4kra
{
  ALTER TYPE default::User {
      CREATE REQUIRED PROPERTY profile_image: std::str {
          SET REQUIRED USING (<std::str>{''});
      };
  };
};
