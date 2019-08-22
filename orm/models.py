from orm.orm import Model, IntPrimaryField, IntField, StringField


class Conversation(Model):
    cid = IntPrimaryField()
    id = IntField(required=True)
    name = StringField(required=True)

    class Meta:
        table_name = 'conversations'
