CREATE MIGRATION m1lltvntt6qjoytl4qscitf66pn3dvvui7hcptneqxotte2mzffmeq
    ONTO m1jsjw7kkzp5qzx6e6l77agfpqr7fjxrcn4algi4bu5gayokl5qzua
{
  CREATE MODULE Paper IF NOT EXISTS;
  CREATE TYPE Paper::Cache {
      CREATE REQUIRED PROPERTY modified: std::datetime;
      CREATE REQUIRED PROPERTY paper_id: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  CREATE TYPE Paper::Paper {
      CREATE REQUIRED PROPERTY category: std::str;
      CREATE REQUIRED PROPERTY description: std::str;
      CREATE MULTI PROPERTY keywords: std::str;
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE REQUIRED PROPERTY paper_id: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
