"""
Written by Ingmar Steen for NRC Media B.V.

For more information, please refer to:
https://blurringexistence.net/graphene-sqlalchemy-n-plus-1.html

The MIT License (MIT)
Copyright © 2019 Ingmar Steen <iksteen@gmail.com> / NRC Media B.V.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import functools
import logging

from graphene.relay.connection import ConnectionOptions
from graphene.types.definitions import GrapheneObjectType
from graphene.types.resolver import attr_resolver
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy.types import SQLAlchemyObjectTypeOptions
from graphql import GraphQLList
from graphql.language.ast import Field, FragmentSpread, InlineFragment
from sqlalchemy import inspect as sa_inspect

__all__ = ["EagerSAObjectType"]

logger = logging.getLogger(__name__)


class EagerSAObjectTypeOptions(SQLAlchemyObjectTypeOptions):
    load_strategies = None


def _traverse_field(field, *path):
    for part in path:
        for field in field.selection_set.selections:
            if isinstance(field, Field) and field.name.value == part:
                break
        else:
            return None
    return field


class EagerSAObjectType(SQLAlchemyObjectType):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, load_strategies=None, _meta=None, **options):
        if _meta is None:
            _meta = EagerSAObjectTypeOptions(cls)
        _meta.load_strategies = load_strategies if load_strategies is not None else {}

        super(EagerSAObjectType, cls).__init_subclass_with_meta__(
            _meta=_meta, **options
        )

    @classmethod
    def get_query(cls, info):
        # Get the base query from graphene-sqlalchemy.
        query = super(EagerSAObjectType, cls).get_query(info)

        # Look up the GraphQL type for this graphene object type.
        node = info.schema.get_type(cls._meta.name)

        # Call the function that will traverse the query
        # and apply the loader strategies.
        return cls._apply_strategy(
            info, query, node, info.field_asts[0].selection_set.selections
        )

    @classmethod
    def _apply_strategy(cls, info, query, node, selections, path=()):
        meta = node.graphene_type._meta

        for field in selections:
            if isinstance(field, (InlineFragment, FragmentSpread)):
                if isinstance(field, FragmentSpread):
                    field = info.fragments[field.name.value]

                query = cls._apply_strategy(
                    info,
                    query,
                    info.schema.get_type(field.type_condition.name.value),
                    field.selection_set.selections,
                    path,
                )
                continue
            elif not isinstance(meta, SQLAlchemyObjectTypeOptions):
                continue

            # Get the referenced field name.
            field_name = field.name.value

            # Graphene helpfully changed our field name to camelCase. Undo that. Hisss..
            resolver = node.fields[field_name].resolver
            if (
                isinstance(resolver, functools.partial)
                and resolver.func is attr_resolver
            ):
                attr_name = resolver.args[0]
            else:
                # Hail mary.
                attr_name = field_name

            if isinstance(meta, EagerSAObjectTypeOptions):
                # Get the load strategies from the type's metadata.
                field_load_strategies = meta.load_strategies.get(attr_name, ())

                for loader, rel_path in field_load_strategies:
                    # Emit a helpful message.
                    logger.info(
                        "Applying %s on %s",
                        loader.__name__,
                        " -> ".join(path + rel_path),
                    )

                    # Apply the load strategy.
                    query = query.options(loader(*(path + rel_path)))

            if not field.selection_set:
                # This is just a field on the object, not a relationship.
                continue

            # Get access to the field's GraphQL type.
            field_node = node.fields[field_name].type

            # If this is a one-to-many or many-to-many relationship, the
            # field's type will be a list. If that's the case, we'll get
            # the inner type here.
            if isinstance(field_node, GraphQLList):
                field_node = field_node.of_type

            # Check if the resulting node is a graphene node.
            if not isinstance(node, GrapheneObjectType):
                logger.info("Node %s not of GrapheneObjectType", node)
                continue

            # And get its metadata.
            field_meta = field_node.graphene_type._meta

            if isinstance(field_meta, ConnectionOptions):
                # Relay connection. Resolve the connection's node type.
                field_node = info.schema.get_type(field_meta.node._meta.name)
                field = _traverse_field(field, "edges", "node")
                if field is None:
                    logger.info(
                        "Could not find edges -> node on connection %s", field_name
                    )
                    continue
                field_meta = field_node.graphene_type._meta

            if not isinstance(field_meta, SQLAlchemyObjectTypeOptions):
                logger.info(
                    "Node meta %s not of SQLAlchemyObjectTypeOptions", field_meta
                )
                continue

            relationships = sa_inspect(meta.model).relationships
            relationship = getattr(relationships, attr_name, None)
            if relationship is None:
                logger.info(
                    "Field %s does not map to a relationship on %s",
                    attr_name,
                    meta.model,
                )
                continue

            related_model = relationship.mapper.class_
            if related_model is not field_meta.model:
                logger.info(
                    "Field %s connects to unexpected model %s", attr_name, related_model
                )
                continue

            # Call the strategy applicator again with the new node,
            # the new selection and the nested path of the query.
            query = cls._apply_strategy(
                info,
                query,
                field_node,
                field.selection_set.selections,
                path + (attr_name,),
            )

        return query
