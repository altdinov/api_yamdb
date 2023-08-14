
class CurrentDefaultTitle:
    requires_context = True

    def __call__(self, serializer_field):
        view = serializer_field.context.get('view')
        title = view._get_title()
        return title
