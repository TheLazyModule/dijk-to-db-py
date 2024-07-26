UPDATE building
SET image_urls = CASE
                     WHEN id = 3
                         THEN ARRAY['https://ik.imagekit.io/routing/routing_data/pbbb.jpg', 'https://ik.imagekit.io/routing/routing_data/pbbbbb.JPG', 'https://ik.imagekit.io/routing/routing_data/pb.jpg', 'https://ik.imagekit.io/routing/routing_data/pbuilding.JPG', 'https://ik.imagekit.io/routing/routing_data/petroleum.JPG']
                     WHEN id = 7
                         THEN ARRAY['https://ik.imagekit.io/routing/routing_data/kumaa.JPG','https://ik.imagekit.io/routing/routing_data/kkkpley.JPG', 'https://ik.imagekit.io/routing/routing_data/kkkply.JPG', 'https://ik.imagekit.io/routing/routing_data/ku.JPG', 'https://ik.imagekit.io/routing/routing_data/kuma.JPG', 'https://ik.imagekit.io/routing/routing_data/kumapp.JPG']
                     WHEN id = 63
                         THEN ARRAY['https://ik.imagekit.io/routing/routing_data/nbb.JPG','https://ik.imagekit.io/routing/routing_data/nbbb.JPG', 'https://ik.imagekit.io/routing/routing_data/nbl.JPG', 'https://ik.imagekit.io/routing/routing_data/nblo.JPG', 'https://ik.imagekit.io/routing/routing_data/nblock.JPG']
                     WHEN id = 13
                         THEN ARRAY['https://ik.imagekit.io/routing/routing_data/nbb.JPG','https://ik.imagekit.io/routing/routing_data/nbbb.JPG', 'https://ik.imagekit.io/routing/routing_data/nbl.JPG', 'https://ik.imagekit.io/routing/routing_data/aerooo.JPG', 'https://ik.imagekit.io/routing/routing_data/aerop.JPG', 'https://ik.imagekit.io/routing/routing_data/aerrr.JPG', 'https://ik.imagekit.io/routing/routing_data/bamfoo.JPG', 'https://ik.imagekit.io/routing/routing_data/bamfo_arr', 'https://ik.imagekit.io/routing/routing_data/plane.JPG']
    -- Add more cases as needed
    END
WHERE id IN (3, 7, 63); -- Add all the IDs that you are updating
