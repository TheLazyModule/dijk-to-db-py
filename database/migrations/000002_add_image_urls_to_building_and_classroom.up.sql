-- Add the image_urls column to the building table
ALTER TABLE "building" ADD COLUMN "image_urls" TEXT[];

-- Add the image_urls column to the classroom table
ALTER TABLE "classroom" ADD COLUMN "image_urls" TEXT[];
