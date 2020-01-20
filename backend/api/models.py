import uuid

from datetime import datetime
from pynamodb.models import Model
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, MapAttribute, ListAttribute, UTCDateTimeAttribute
from werkzeug.security import check_password_hash, generate_password_hash

class PasswordAttribute(UnicodeAttribute):
    def serialize(self, value):
        return generate_password_hash(value)

    def deserialize(self, value):
        return value

class Player(Model):
    class Meta:
        table_name = "tfranksystem-player"
        region = 'eu-central-1'
        host = 'https://dynamodb.eu-central-1.amazonaws.com'

    def __init__(self, hash_key=None, range_key=None, **args):
        Model.__init__(self, hash_key, range_key, **args)
        if not self.player_id:
            self.player_id = str(uuid.uuid4())

    player_id = UnicodeAttribute(hash_key=True, null=False)
    name = UnicodeAttribute(null=False)
    password = PasswordAttribute(null=False)
    rank = NumberAttribute(null=False)
    sigma = NumberAttribute(null=False)

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            if isinstance(attr, MapAttribute):
                yield name, getattr(self, name).as_dict()
            else:
                yield name, attr.serialize(getattr(self, name))

    def check_password(self, password):
        return check_password_hash(self.password, password)

class PlayerIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "user_index"
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()
        region = 'eu-central-1'
        host = 'https://dynamodb.eu-central-1.amazonaws.com'

    player_id = UnicodeAttribute(hash_key=True)

class PlayerMap(MapAttribute):
    player_id = UnicodeAttribute(null=False)
    name = UnicodeAttribute(null=False)

class Match(Model):
    class Meta:
        table_name = "tfranksystem-match"
        region = 'eu-central-1'
        host = 'https://dynamodb.eu-central-1.amazonaws.com'
    match_id = UnicodeAttribute(hash_key=True, null=False)
    player_order = ListAttribute(of=PlayerMap, null=False)
    datetime = UTCDateTimeAttribute(default=datetime.now, range_key=True, null=False)

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            if isinstance(attr, MapAttribute):
                yield name, getattr(self, name).as_dict()
            else:
                yield name, attr.serialize(getattr(self, name))

class HistoricalRank(Model):
    class Meta:
        table_name = "tfranksystem-historicalrank"
        region = 'eu-central-1'
        host = 'https://dynamodb.eu-central-1.amazonaws.com'
    player_id = UnicodeAttribute(hash_key=True, null=False)
    player_index = PlayerIndex()
    match_id = UnicodeAttribute(null=False)
    rank = NumberAttribute(null=False)
    sigma = NumberAttribute(null=False)
    datetime = UTCDateTimeAttribute(default=datetime.now, range_key=True, null=False)

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            if isinstance(attr, MapAttribute):
                yield name, getattr(self, name).as_dict()
            else:
                yield name, attr.serialize(getattr(self, name))

if not Player.exists():
    Player.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

if not Match.exists():
    Match.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

if not HistoricalRank.exists():
    Match.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)