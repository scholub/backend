CREATE MIGRATION m1tx56kxtg7zgmsl43fwmpnvvjro5y2l4kqtfjmy4l46rhnw74skaq
    ONTO m16hffzdwo2zgpzufdo3zpx6eeq7bxnallmmyhpwfyevyusgy3vh5a
{
  ALTER TYPE default::User {
      CREATE MULTI LINK recommends: Paper::Post;
  };
};
