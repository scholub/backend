CREATE MIGRATION m1twbhkpngudhzadcdry7m5g4l4dsibjwejm2nvmvkcm2nyskmiw2q
    ONTO m1eoar2ax3izxsgpq3hqnziw42rmy3bruvoue47omadp625bou2vta
{
  ALTER TYPE Paper::Post {
      ALTER LINK comments {
          ON TARGET DELETE ALLOW;
      };
  };
};
