class TrackingFieldsMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_fields = {}
        self._set_old_fields()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        result = super().save(force_insert, force_update, using, update_fields)
        self._set_old_fields()
        return result

    def _set_old_fields(self):
        for field in self._meta.fields:
            attname, column = field.get_attname_column()
            self._old_fields[attname] = getattr(self, attname)

    def get_old_fields(self):
        return self._old_fields

    # Returns the fields name that have been modified since they are loaded or saved most recently.
    def get_dirty_fields(self):
        dirty_fields = []
        for field in self._old_fields:
            if self._old_fields[field] != getattr(self, field):
                dirty_fields.append(field)
        return dirty_fields

    def get_old_field(self, field, default=None):
        if field in self._old_fields:
            return self._old_fields[field]
        return default

    def set_old_field(self, field, value):
        self._old_fields[field] = value        
