from rest_framework import permissions


class IsUserOrReadOnly(permissions.BasePermission):
    # Only allows the user who owns an object to edit it.

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        return obj == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    # Only allows the user who owns an object to edit it.

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        return obj.user == request.user


class IsMainFriendOrReadOnly(permissions.BasePermission):
    # Allows user (you) to edit friend and friend request objects
    # Forbids other users from editing, but allows them to view friends
    # Prevents anonymous users from viewing

    def has_object_permission(self, request, view, obj):

        if request.user.is_authenticated():

            if request.method in permissions.SAFE_METHODS:
                return True

            return obj.from_user == request.user


class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details, allows staff to view all records
        # Since objects, in this case, are users, check obj == request.user
        return request.user.is_staff or obj == request.user


class IsAdminOrPostOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            return True
        return request.user.is_staff()


class IsOwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user == obj.username
