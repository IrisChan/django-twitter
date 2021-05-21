from rest_framework.permissions import BasePermission


class IsObjectOwner(BasePermission):
    """
    这个Permission负责检查obj.user 是不是==request.user
    这个类是比较通用的，今后如果其他也用到这个累的地方，可以将文件放到一个共享的位置
    Permission会一个个被执行
    -- 如果是detail=False的action，只检测has_permission
    -- 如果是detail=True的action，同时检测has_perission和has_object_permission
    如果出错的时候，默认的错误信息会显示IsObjectOwner.message 的内容
    """
    message = "You do not have permission to access this object"

    def has_permissions(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user