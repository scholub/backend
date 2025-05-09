CREATE MIGRATION m1cxyyawmrnmhv2arrklc5nsgphgcck2ztg5gkrcw4lkj37yrtk6kq
    ONTO m1ngayhgw5qsp5iig6xri72k5vwi7ciky7ro4l32j3ezabkpjajrlq
{
  ALTER TYPE default::User {
      CREATE MULTI LINK bookmarks: Paper::Post;
  };
};
