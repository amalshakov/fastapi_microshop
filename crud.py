import asyncio

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import join, joinedload, selectinload

from microshop.core.models import Post, Profile, User, db_helper


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_users_with_posts(session: AsyncSession) -> list[User]:
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = (
        select(User)
        .options(
            # joinedload(User.posts),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    # users = await session.scalars(stmt)
    # result: Result = await session.execute(stmt)
    # users = result.unique().scalars()
    # users = result.scalars()
    users = await session.scalars(stmt)

    # for user in users.unique():
    for user in users:
        user: User
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)


async def get_users_with_posts_and_profiles(
    session: AsyncSession,
) -> list[User]:
    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)

    for user in users:
        user: User
        print("**" * 10)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post)


async def get_posts_with_authors(session: AsyncSession) -> list[Post]:
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts:
        post: Post
        print("*" * 20)
        print("post", post)
        print("author", post.user)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        )
        .where(User.username == "sam")
        .order_by(Profile.id)
    )

    profiles = await session.scalars(stmt)

    for profile in profiles:
        profile: Profile
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def get_user_by_username(
    session: AsyncSession, username: str
) -> User | None:
    stmt = select(User).where(User.username == username)
    user: User | None = await session.scalar(stmt)
    print("found user", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id, first_name=first_name, last_name=last_name
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    print(users)
    for user in users:
        print(user)


async def create_posts(
    session: AsyncSession, user_id: int, *posts_titles: str
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def main_relations(session: AsyncSession):
    # await create_user(session=session, username="alice")
    # await create_user(session=session, username="alexander")
    # user_alex = await get_user_by_username(
    #     session=session, username="alex"
    # )
    # user_sam = await get_user_by_username(
    #     session=session,
    #     username="sam",
    # )
    # user_alex = await get_user_by_username(
    #     session=session, username="alex"
    # )
    # await create_user_profile(
    #     session=session, user_id=user_alex.id, first_name="John"
    # )
    # await create_user_profile(
    #     session=session,
    #     user_id=user_sam.id,
    #     first_name="Sam",
    #     last_name="Petrov",
    # )
    # await get_user_by_username(session=session, username="ksu")
    # await show_users_with_profiles(session=session)
    # await create_posts(
    #     session,
    #     user_sam.id,
    #     "SQLA 2.0",
    #     "SQLA Joins",
    # )
    # await create_posts(
    #     session,
    #     user_alex.id,
    #     "FastAPI intro",
    #     "FastAPI Advanced",
    #     "FastAPI more",
    # )
    # await get_users_with_post(session=session)
    # await get_posts_with_authors(session=session)
    # await get_users_with_posts_and_profiles(session=session)
    await get_profiles_with_users_and_users_with_posts(session=session)


async def demo_m2m(session: AsyncSession):
    pass


async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session=session)
        await demo_m2m(session=session)


if __name__ == "__main__":
    asyncio.run(main())
