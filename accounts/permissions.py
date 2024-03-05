from rest_framework import permissions


class IsOwnerOnly(permissions.BasePermission):
    """
    Custom permission to only allow the owner of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the owner of the object.
        return obj.owner == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the profile.
        return obj.user == request.user


class IsUnauthenticated(permissions.BasePermission):
    """
    Allows access only to Unauthenticated users.
    """

    def has_permission(self, request, view):
        return not request.user or not request.user.is_authenticated
