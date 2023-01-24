class AbilityAdminMixin:
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return request.ability.queryset_for("view", self.model)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True

        can = request.ability.can
        return (
            can("view", self.model)
            or can("change", self.model)
            or can("delete", self.model)
        )

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.ability.can("add", self.model)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.ability.can("view", self.model)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.ability.can("change", self.model)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.ability.can("delete", self.model)
