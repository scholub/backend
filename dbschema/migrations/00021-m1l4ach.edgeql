CREATE MIGRATION m1l4achbrpw6rtisi5uqscymjnpz6mwhqv3rdflvmtxzhiz4gq4kra
    ONTO m1cmmsolaen7qizf7r2ehs7nzg6d55bhwkfw7rsjja4sl7qme4o4aa
{
  CREATE EXTENSION pgvector VERSION '0.7';
  CREATE SCALAR TYPE Paper::Embedding EXTENDING ext::pgvector::vector<1536>;
  ALTER TYPE Paper::Post {
      CREATE REQUIRED PROPERTY embedding: Paper::Embedding {
          SET REQUIRED USING (<Paper::Embedding>{});
      };
      CREATE INDEX ext::pgvector::ivfflat_cosine(lists := 1) ON (.embedding);
  };
};
