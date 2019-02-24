Title: graphene-sqlalchemy and the n+1 problem
Date: 2019-02-24 22:30:00
Tags: technical, python, SQLAlchemy, GraphQL
Slug: graphene-sqlalchemy-n-plus-1

In this post I describe what the _n + 1_ problem is, how it relates to
graphene-sqlalchemy, I describe some possible solutions and finally
I'll describe the solution I created for a project that uses
graphene-sqlalchemy for my current employer (NRC Media B.V.).

<!-- PELICAN_END_SUMMARY -->

### The _n + 1_ problem

The _n + 1_ problem is a problem one typically encounters when using an
ORM: You query for a set of objects that have a relationship with
another model. An example using SQLAlchemy:

    ::python
    from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship, sessionmaker

    Base = declarative_base()

    class UserModel(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
        name = Column(String)
        posts = relationship("PostModel", back_populates="user")

    class PostModel(Base):
        __tablename__ = "posts"
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"))
        content = Column(String)
        users = relationship("UserModel", back_populates="posts")

    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add some data:
    for user_name in ("Noah", "Emma"):
        user = UserModel(name=user_name)
        session.add(user)
            for content in ("Lorem", "Ipsum", "dolor", "sit", "amet"):
                session.add(PostModel(user=user, content=content))
    session.commit()

When accessing the related model through the parent object's property, a
new query is executed to load the related data. If you do this for all
the objects in your original queryin a loop, the ORM will issue that
query for each object.

Assuming you have _n_ objects, to load all the related data the ORM will
issue a total of _n + 1_ queries (one to load the objects, one for each
object to load the related data).

    :::python
    # Print all posts:
    for user in session.query(UserModel):
        print(f"\n{user.name}:")
        posts = user.posts
        print(f" - {' '.join(post.content for post in posts)}..")

Running this demo will show the problem:

    INFO:sqlalchemy.engine.base.Engine SELECT users.id AS users_id, users.name AS users_name 
    FROM users
    INFO:sqlalchemy.engine.base.Engine ()

    Noah:
    INFO:sqlalchemy.engine.base.Engine SELECT posts.id AS posts_id, posts.user_id AS posts_user_id, posts.content AS posts_content 
    FROM posts 
    WHERE ? = posts.user_id
    INFO:sqlalchemy.engine.base.Engine (1,)
     - Lorem Ipsum dolor sit amet..

    Emma:
    INFO:sqlalchemy.engine.base.Engine SELECT posts.id AS posts_id, posts.user_id AS posts_user_id, posts.content AS posts_content 
    FROM posts 
    WHERE ? = posts.user_id
    INFO:sqlalchemy.engine.base.Engine (2,)
     - Lorem Ipsum dolor sit amet..

When accessing the `user.posts` property, SQLAlchemy will issue a new
query to load the required data.

By itself, it's not really a problem. It is however not the most
efficient way to use your relational database. For each secondary query,
another roundtrip to the database is made to load the data. Also, unless
you use a transaction, the data you request might be in an inconsistent
state due to updates on the database in between your separate queries.

Now imagine that there are a lot more relationships (comments,
attachments) and this is used in a high-traffic website. The roundtrips
will add up.

### Traditional solutions

Solving the _n + 1_ problem typically involves assisting your ORM by
telling it which relationships to load in advance, this is also known as
prefetching or eager loading. When using SQLAlchemy, you have two
options to do so: at the model level and on a per-query basis.
SQLAlchemy provides four strategies to prefetch data:

- `select`: The default, only load the related data when accessing the
    relationship field.
- `joined`: Use a `JOIN` clause to eagerly load the related data. Great
    when using one-to-one / only-a-few-to-one relationships or
    many-to-one relationships where the joined table does not have a lot
    of fields.
- `selectin`: Resolve the primary query first, then use a single second
    query that will resolve the related data by referencing the
    appropriate keys. Great when using many-to-many relationships or
    many-to-one where the related table has a lot of fields.
- `subquery`: Resolve the primary query first, then use another query
    with a `WHERE` clause that repeats the primary query as a subquery
    to select the appropriate rows on the related table. Usually only
    useful if your database server does not support the `selectin`
    strategy when using composite primary keys.

At the model level, you can tell SQLAlchemy to always use a specific
loading strategy.

For example, to always use the `selectin` strategy when loading a user's
comments, you can change the model:

    :::python
    class UserModel(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
        name = Column(String)
        posts = relationship(
            "PostModel",
            back_populates="user",
            lazy="selectin"
        )

The downsides of specifying this at the model level are that you're
encoding business logic in your model and that the data will always be
loaded whether it's actually needed or not. Great if you know exactly
what data you'll always need when accessing a certain model, not so
great if you end up pre-emptively loading a large set of related data
and not needing it.

You can also specify these loading strategies on a per-query basis. You
do this by calling the `.options()` method of a query and providing it
with the strategies you want to apply to the query. The downside of this
is that you need to do this for every query you run, forget one and you
potentially drag down performance. And you need access to the query
which is not always trivial when using an automatic serializer. When
you're not sure what data will be referenced, it can be hard to predict
an optimized loading strategy.

To use the `selectin` strategy as a query option with our example:

    :::python
    from sqlalchemy.orm import selectinload

    # Print all posts:
    for user in session.query(User).options(selectinload('posts')):
        print(f"\n{user.name}:")
        posts = user.posts
        print(f" - {' '.join(post.content for post in posts)}..")

Applying the `selectin` loader either at the model level or on the query
will result in the following output:

    INFO:sqlalchemy.engine.base.Engine SELECT users.id AS users_id, users.name AS users_name 
    FROM users
    INFO:sqlalchemy.engine.base.Engine ()
    INFO:sqlalchemy.engine.base.Engine SELECT users_1.id AS users_1_id, posts.id AS posts_id, posts.user_id AS posts_user_id, posts.content AS posts_content 
    FROM users AS users_1 JOIN posts ON users_1.id = posts.user_id 
    WHERE users_1.id IN (?, ?) ORDER BY users_1.id
    INFO:sqlalchemy.engine.base.Engine (1, 2)

    Noah:
     - Lorem Ipsum dolor sit amet..

    Emma:
     - Lorem Ipsum dolor sit amet..

SQLAlchemy emitted only two queries now: One to load the users and one
to efficiently load all the commits at once.

A novel solution to the limitations of both these methods was developed
in the form of
[sqlalchemy\_bulk\_lazy\_loader](https://github.com/operator/sqlalchemy_bulk_lazy_loader).
Instead of defining the loading strategies in advance, the bulk loader
will only emit the secondary query when the related property is used.
Downsides of this strategy are that the bulk loader hasn't been updated
in a while, that it doesn't support the `selectin` strategy and that is
doesn't work when using composite primary keys.

### graphene-sqlalchemy and _n + 1_

One problem that's tricky to solve properly with relational data models
is exposing them through an API. You usually end up with either
hand-written queries and endpoints or you use a serializer that
understands the ORM you use. The downside of such a serializer is that
it's usually not trivial to add data that does not come from your ORM
and that it might not be trivial to apply an efficient loading strategy.

Using GraphQL is a very natural way of exposing a relational data model
through an API. It allows you to describe what data you want and it will
allow you to easily add fields or connections that are not part of your
database structure.

A very easy way to expose your SQLAlchemy models using GraphQL is the
`graphene-sqlalchemy` library. It builds on `graphene` (a GraphQL
framework for python) and can map SQLAlchemy models to GraphQL types. It
allows for enough flexibility to easily specify what fields should be
mapped, you can easily override the way fields are resolved and it
supports and exposes SQLAlchemy relationships automatically.

An example based on the models described above:

    :::python
    import graphene
    from graphene_sqlalchemy import SQLAlchemyObjectType

    class User(SQLAlchemyObjectType):
        class Meta:
            model = UserModel

    class Post(SQLAlchemyObjectType):
        class Meta:
            model = PostModel

    class Query(graphene.ObjectType):
        users = graphene.List(User)

        def resolve_users(self, info):
            query = User.get_query(info)
            return query.all()

    schema = graphene.Schema(query=Query)

    query = '''
        query {
          users {
            name
            posts {
              content
            }
          }
        }
    '''
    result = schema.execute(query, context_value={'session': session})
    for user in result.data["users"]:
        print(f"\n{user['name']}:")
        posts = user["posts"]
        print(f" - {' '.join(post['content'] for post in posts)}..")

The way this works is that `graphene-sqlalchemy` exposes all fields and
relationships on `UserModel`, including its `posts`. When resolving the
results, graphene will loop through the users and fetch their posts
using _n + 1_ queries, just like in the previous examples:

    INFO:sqlalchemy.engine.base.Engine SELECT users.id AS users_id, users.name AS users_name 
    FROM users
    INFO:sqlalchemy.engine.base.Engine ()
    INFO:sqlalchemy.engine.base.Engine SELECT posts.id AS posts_id, posts.user_id AS posts_user_id, posts.content AS posts_content 
    FROM posts 
    WHERE ? = posts.user_id
    INFO:sqlalchemy.engine.base.Engine (1,)
    INFO:sqlalchemy.engine.base.Engine SELECT posts.id AS posts_id, posts.user_id AS posts_user_id, posts.content AS posts_content 
    FROM posts 
    WHERE ? = posts.user_id
    INFO:sqlalchemy.engine.base.Engine (2,)

    Noah:
     - Lorem Ipsum dolor sit amet..

    Emma:
     - Lorem Ipsum dolor sit amet..

There are several ways to apply a loading strategy when using
`graphene-sqlalchemy`. The easiest way is applying the loader strategy
at the model level. However, since one of the nice features of GraphQL
queries is that you might not always want all the data, this is a
sub-optimal solution.

Another option is to override the `get_query` method of the
`SQLAlchemyObjectType` class and applying the loading options there.
Which has the exact same problem: How to know in advance which
strategies to apply? Any type is potentially an entrypoint for a query,
and it can be nested any way the client wants.

The previously mentioned bulk loader would certainly work in this
scenario, but since it has its limitations, I'd rather not depend on it.

_Yacine_ provides an interesting
[solution](https://yacine.org/2017/02/27/graphqlgraphene-sqlalchemy-and-the-n1-problem/)
as well: Why not work through the query and the models and apply a
loading strategy automatically. It also has its downside: The code is a
bit hard to follow and it can only apply a single loading strategy for
all types of relationships.

This did inspire me to come up with my own solution. What if we can
somehow specify on a per type basis what strategies to apply?

### My solution

What if we could specify what relationships to load eagerly by defining
that in the node type's metadata? And that when creating an SQLAlchemy
query, we traverse the GraphQL query and for each selection we check if
a load strategy is defined and apply it if it is. If the selection
defines a nested query, we check if the initial field maps to a
relationship on the SQLAlchemy model and recurse into the strategy
applicator.

But first things first, let's think about how this would look and what
information we need to apply the loader strategy.

Also, what features do we support? To prevent this post from getting any
lengthier than it already is, I won't include support for GraphQL's
(inline) fragments, relay's connections and I'll hand-wave a lot of type
and error checking. I'll attach a copy at the end of the article that
does support all that.

To start, we'd need a custom graphene object type that inherits from
`SQLAlchemyObjectType` and implements its own meta type based on
`SQLAlchemyObjectTypeOptions` (which is what `graphene-sqlalchemy` uses to
describe its metadata). Let's call these `EagerSAObjectType` and
`EagerSAObjectTypeOptions`.

Then, to apply a loading strategy, we need access to the query, we need
the entire relationship path leading up to the current relationship
(_user -> post -> comment -> user_) and we need to know what strategy to
apply.

My proposal is to add a dictionary to the node's metadata that maps a
field on the type to a loader strategy and the path relative to the
current relationship path:

    :::python
    class User(EagerSAObjectType):
        class Meta:
            model = UserModel
            load_strategies = {
                "posts": (
                    (selectinload, ("posts",)),
                ),
            }

Let's create this `EagerSAObjectType` and its options:

    :::python
    class EagerSAObjectTypeOptions(SQLAlchemyObjectTypeOptions):
        # This is where we will store the loading strategies.
        load_strategies = None

    class EagerSAObjectType(SQLAlchemyObjectType):
        class Meta:
            abstract = True

        @classmethod
        def __init_subclass_with_meta__(
            cls,
            load_strategies=None,
            _meta=None,
            **options
        ):
            if _meta is None:
                _meta = EagerSAObjectTypeOptions(cls)
            _meta.load_strategies = load_strategies if load_strategies is not None else {}

            super(EagerSAObjectType, cls).__init_subclass_with_meta__(_meta=_meta, **options)

Now, override the `SQLAlchemyObjectType`'s `get_query` classmethod and
have it call another method on the query providing it with the query,
the node's type and the fields that are selected on the root of the
query:

    :::python
        @classmethod
        def get_query(cls, info):
            # Get the base query from graphene-sqlalchemy.
            query = super(EagerSAObjectType, cls).get_query(info)

            # Look up the GraphQL type for this graphene object type.
            node = info.schema.get_type(cls._meta.name)

            # Call the function that will traverse the query
            # and apply the loader strategies.
            return cls._apply_strategy(
                query,
                node,
                info.field_asts[0].selection_set.selections
            )

        @classmethod
        def _apply_strategy(cls, query, node, selections):
            # Do nothing for now.
            return query

For our first attempt, we only go one level deep. We iterate the
selection set, check if the node defines any load strategies for the
field and apply them:

    :::python
        @classmethod
        def _apply_strategy(cls, query, node, selections, path=()):
            # Get access to the node's metadata.
            meta = node.graphene_type._meta

            for field in selections:
                # Get the referenced field name.
                field_name = field.name.value

                # Get the load strategies from the type's metadata.
                field_load_strategies = meta.load_strategies.get(field_name, ())

                for loader, rel_path in field_load_strategies:
                    # Emit a helpful message.
                    logger.info('Applying %s on %s', loader.__name__, ' -> '.join(path + rel_path))

                    # Apply the load strategy.
                    query = query.options(loader(*(path + rel_path)))

            # Return the query with the load strategies applied.
            return query

Now try it!

    INFO:eager_loader:Applying selectinload on posts
    INFO:sqlalchemy.engine.base.Engine:SELECT users.id AS users_id, users.name AS users_name 
    FROM users
    INFO:sqlalchemy.engine.base.Engine:()
    INFO:sqlalchemy.engine.base.Engine:SELECT users_1.id AS users_1_id, posts.id AS posts_id, posts.user_id AS posts_user_id, posts.content AS posts_content 
    FROM users AS users_1 JOIN posts ON users_1.id = posts.user_id 
    WHERE users_1.id IN (?, ?) ORDER BY users_1.id
    INFO:sqlalchemy.engine.base.Engine:(1, 2)

So now what if we want to force SQLAlchemy to eagerly load the post's
user if we query that? Change the `Post` node type to:

    :::python
    class Post(EagerSAObjectType):
        class Meta:
            model = PostModel
            load_strategies = {
                "user": (
                    (joinedload, ("user",)),
                ),
            }

and the GraphQL query to:

    :::python
    query = """
        query {
          users {
            name
            posts {
              content
              user {
                name
              }
            }
          }
        }
    """

I agree, this is a silly example, but we have only two types available.
Even worse, without any assistance, SQLAlchemy would know that the
post's user is actually the user to which the post object belongs so it
won't issue _n + 1_ queries.

However, to show how to implement nesting the load strategy applicator,
we'll convince SQLAlchemy to perform a joined load in this situation
anyway.

We'll introduce recursion like this (insert this before the
`return query` statement in the `_apply_strategy` classmethod):

    :::python
                if not field.selection_set:
                    # This is just a field on the object, not a relationship.
                    continue

                # Get access to the field's GraphQL type.
                field_node = node.fields[field_name].type

                # If this is a one-to-many or many-to-many relationship, the
                # field's type will be a list. If that's the case, we get
                # the inner type here.
                if isinstance(field_node, GraphQLList):
                    field_node = field_node.of_type

                # Call the strategy applicator again with the new node,
                # the new selection and the nested path of the query.
                query = cls._apply_strategy(
                    query,
                    field_node,
                    field.selection_set.selections,
                    path + (field_name,),
                )

We can now see SQLAlchemy emitting the join from the post to the user:

    INFO:eager_loader:Applying selectinload on posts
    INFO:eager_loader:Applying joinedload on posts -> user
    INFO:sqlalchemy.engine.base.Engine:SELECT users.id AS users_id, users.name AS users_name 
    FROM users
    INFO:sqlalchemy.engine.base.Engine:()
    INFO:sqlalchemy.engine.base.Engine:SELECT users_1.id AS users_1_id, posts.id AS posts_id, posts.user_id AS posts_user_id, posts.content AS posts_content, users_2.id AS users_2_id, users_2.name AS users_2_name 
    FROM users AS users_1 JOIN posts ON users_1.id = posts.user_id LEFT OUTER JOIN users AS users_2 ON users_2.id = posts.user_id 
    WHERE users_1.id IN (?, ?) ORDER BY users_1.id
    INFO:sqlalchemy.engine.base.Engine:(1, 2)

Success!

### Considerations and download

As mentioned, the code sample above is rather naive.

In addition to not supporting non-SQLAlchemy relationships or indirect
relationships like relay connections, it doesn't support GraphQL
fragments, it doesn't respect the fact that graphene converts field
names to camelCase whereas your model probably uses snake\_case. It does
no defensive type checking like checking if the resulting property is
actually an SQLAlchemy relationship to the right type. Fortunately, all
that is easy to add.

But since it doesn't add much to the actual solution of the problem at
hand, I've decided not to describe them fully.

I do offer the complete version for you to
[download]({static}/downloads/graphene-sqlalchemy-n-plus-1/eager_loader.py).
