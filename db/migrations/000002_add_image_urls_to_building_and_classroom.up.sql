-- Add the image_urls column to the building table
ALTER TABLE "building"
    ADD COLUMN "image_urls" TEXT[];

-- Add the name column to the classroom table
ALTER TABLE "classroom"
    ADD COLUMN "name" varchar;

-- Add the description column to the classroom table
ALTER TABLE "classroom"
    ADD COLUMN "description" varchar;

-- Add the image_urls column to the classroom table
ALTER TABLE "classroom"
    ADD COLUMN "image_urls" TEXT[];

-- Alter column room_code to allow for null values
ALTER TABLE "classroom"
    ALTER COLUMN "room_code" DROP NOT NULL;