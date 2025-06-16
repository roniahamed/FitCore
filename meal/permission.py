from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admin User can do anything
        if request.user and request.user.is_staff:
            return True
        # Read permissions are allowed to any request if safe method
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return request.user == obj.user

class IsFoodOwnerOrPublic(permissions.BasePermission):

    def has_object_permission(self,request, view, obj):
        if request.user and request.user.is_staff:
            return True 
        
        if request.method in permissions.SAFE_METHODS:
            return obj.is_public or (request.user == obj.user_added and not obj.is_public)
        
        return request.user == obj.user_added and not obj.is_public
