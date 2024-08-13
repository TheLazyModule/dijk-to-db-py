-- Remove the image_urls column from the building table
ALTER TABLE "building" DROP COLUMN if exists "image_urls";

-- Remove the image_urls column from the classroom table
ALTER TABLE "classroom" DROP COLUMN  if exists "image_urls";
