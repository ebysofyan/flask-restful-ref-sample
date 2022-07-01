"""Django Rest Framework permissions like"""
from typing import List

from movie_api.db.models.account import USER_GROUPS, Group, User
from movie_api.entity.movie import AccountPermissionLevel
from movie_api.utils.general_helper import flatten_list

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class OperationHolderMixin:
    def __and__(self, other):
        return OperandHolder(AND, self, other)

    def __or__(self, other):
        return OperandHolder(OR, self, other)

    def __rand__(self, other):
        return OperandHolder(AND, other, self)

    def __ror__(self, other):
        return OperandHolder(OR, other, self)

    def __invert__(self):
        return SingleOperandHolder(NOT, self)


class SingleOperandHolder(OperationHolderMixin):
    def __init__(self, operator_class, op1_class):
        self.operator_class = operator_class
        self.op1_class = op1_class

    def __call__(self, *args, **kwargs):
        op1 = self.op1_class(*args, **kwargs)
        return self.operator_class(op1)


class OperandHolder(OperationHolderMixin):
    def __init__(self, operator_class, op1_class, op2_class):
        self.operator_class = operator_class
        self.op1_class = op1_class
        self.op2_class = op2_class

    def __call__(self, *args, **kwargs):
        op1 = self.op1_class(*args, **kwargs)
        op2 = self.op2_class(*args, **kwargs)
        return self.operator_class(op1, op2)


class AND:
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2

    def has_permission(self, user: User) -> bool:
        return bool(self.op1.has_permission(user) and self.op2.has_permission(user))


class OR:
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2

    def has_permission(self, user: User) -> bool:
        return bool(self.op1.has_permission(user) or self.op2.has_permission(user))


class NOT:
    def __init__(self, op1):
        self.op1 = op1

    def has_permission(self, user: User) -> bool:
        return not self.op1.has_permission(user)


class BasePermissionMetaclass(OperationHolderMixin, type):
    pass


class BasePermission(metaclass=BasePermissionMetaclass):
    def has_permission(self, user: User) -> bool:
        return True


class AllowAll(BasePermission):
    def has_permission(self, user: User) -> bool:
        return super().has_permission(user)


class IsAuthenticated(BasePermission):
    def has_permission(self, user: User) -> bool:
        # my_groups: List[str] = flatten_list(user.groups.with_entities(Group.name).all())
        # return user is not None and USER_GROUPS[0][0] in my_groups TODO: uncomment later
        return user is not None and user.account is not None


class IsAdminUser(IsAuthenticated):
    def has_permission(self, user: User) -> bool:
        return super().has_permission(user=user) and bool(
            user.account.permission_level == AccountPermissionLevel.admin
        )


class IsGroupAdminUser(IsAuthenticated):
    def has_permission(self, user: User) -> bool:
        my_groups: List[str] = flatten_list(user.groups.with_entities(Group.name).all())
        return super().has_permission(user=user) and USER_GROUPS[1][0] in my_groups


class IsSurveyAdminUser(IsAuthenticated):
    def has_permission(self, user: User) -> bool:
        my_groups: List[str] = flatten_list(user.groups.with_entities(Group.name).all())
        return super().has_permission(user=user) and USER_GROUPS[2][0] in my_groups
