from orm.orm import Model, IntPrimaryField, IntField, StringField


class Conversation(Model):
    cid = IntPrimaryField()
    id = IntField(required=True)
    name = StringField(required=False)

    class Meta:
        table_name = 'conversations'
