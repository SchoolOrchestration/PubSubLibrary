import json
import datetime


class JSONEncoder(json.JSONEncoder):
    """Custom encoder for handling dates."""

    def default(self, obj):
        """Serializer dates and default to the JSONEncoder default for other data types."""

        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()

        return super().default(obj)
