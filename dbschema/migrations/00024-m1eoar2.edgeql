CREATE MIGRATION m1eoar2ax3izxsgpq3hqnziw42rmy3bruvoue47omadp625bou2vta
    ONTO m1tx56kxtg7zgmsl43fwmpnvvjro5y2l4kqtfjmy4l46rhnw74skaq
{
  ALTER TYPE Comment::Reaction {
      ALTER LINK comment {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
};
