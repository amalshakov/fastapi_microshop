-- SELECT
--        users.username,
--        users.id,
--        profiles_1.first_name,
--        profiles_1.last_name,
--        profiles_1.bio,
--        profiles_1.id AS id_1,
--        profiles_1.user_id
-- FROM
--        users
--        LEFT OUTER JOIN profiles AS profiles_1 ON users.id = profiles_1.user_id
-- ORDER BY
--        users.id
-- SELECT
--        users.username,
--        users.id,
--        posts_1.title,
--        posts_1.body,
--        posts_1.id AS id_1,
--        posts_1.user_id
-- FROM
--        users
--        LEFT OUTER JOIN posts AS posts_1 ON users.id = posts_1.user_id
-- ORDER BY
--        users.id
-- SELECT
--        users.username,
--        users.id
-- FROM
--        users
-- ORDER BY
--        users.id
-- SELECT
--        posts.user_id AS posts_user_id,
--        posts.title AS posts_title,
--        posts.body AS posts_body,
--        posts.id AS posts_id
-- FROM
--        posts
-- WHERE
--        posts.user_id IN (2, 6, 7)
-- SELECT
--        posts.title,
--        posts.body,
--        posts.id,
--        posts.user_id,
--        users_1.username,
--        users_1.id AS id_1
-- FROM
--        posts
--        LEFT OUTER JOIN users AS users_1 ON users_1.id = posts.user_id
-- ORDER BY
--        posts.id
-- SELECT
--        users.username,
--        users.id,
--        profiles_1.first_name,
--        profiles_1.last_name,
--        profiles_1.bio,
--        profiles_1.id AS id_1,
--        profiles_1.user_id
-- FROM
--        users
--        LEFT OUTER JOIN profiles AS profiles_1 ON users.id = profiles_1.user_id
-- ORDER BY
--        users.id
-- SELECT
--        posts.user_id AS posts_user_id,
--        posts.title AS posts_title,
--        posts.body AS posts_body,
--        posts.id AS posts_id
-- FROM
--        posts
-- WHERE
--        posts.user_id IN (2, 6, 7)
SELECT
       profiles.first_name,
       profiles.last_name,
       profiles.bio,
       profiles.id,
       profiles.user_id,
       users_1.username,
       users_1.id AS id_1
FROM
       profiles
       JOIN users ON users.id = profiles.user_id
       LEFT OUTER JOIN users AS users_1 ON users_1.id = profiles.user_id
WHERE
       users.username = "sam"
ORDER BY
       profiles.id
SELECT
       posts.user_id AS posts_user_id,
       posts.title AS posts_title,
       posts.body AS posts_body,
       posts.id AS posts_id
FROM
       posts
WHERE
       posts.user_id IN (2)