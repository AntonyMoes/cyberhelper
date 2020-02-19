from async_orm.orm import Model, IntPrimaryField, IntField, StringField


class Conversation(Model):
    cid = IntPrimaryField()
    id = IntField(required=True)
    name = StringField(required=False)
    last_ts = IntField(required=True)

    class Meta:
        table_name = 'conversations'


class Notification(Model):
    rid = IntPrimaryField()
    type = StringField(required=True)
    whom = IntField(required=True)
    ts = IntField(required=True)

    class Meta:
        table_name = 'notifications'
