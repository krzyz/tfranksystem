import uuid
import json

from datetime import datetime
from pynamodb.models import Model
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, MapAttribute, ListAttribute, UTCDateTimeAttribute
from werkzeug.security import check_password_hash, generate_password_hash
import os

stage = os.environ.get('STAGE')

class BaseModel(Model):
    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)

    def to_dict(self):
        ret_dict = {}
        for name, attr in self.attribute_values.items():
            ret_dict[name] = self._attr2obj(attr)

        return ret_dict

    def _attr2obj(self, attr):
        # compare with list class. It is not ListAttribute.
        if isinstance(attr, list):
            _list = []
            for l in attr:
                _list.append(self._attr2obj(l))
            return _list
        elif isinstance(attr, MapAttribute):
            _dict = {}
            for k, v in attr.attribute_values.items():
                _dict[k] = self._attr2obj(v)
            return _dict
        elif isinstance(attr, datetime):
            return attr.isoformat()
        else:
            return attr

class PasswordAttribute(UnicodeAttribute):
    def serialize(self, value):
        return generate_password_hash(value)

    def deserialize(self, value):
        return value

class Player(BaseModel):
    class Meta:
        table_name = f'tfranksystem-player-{stage}'
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

class TeamMap(MapAttribute):
    players = ListAttribute(of=PlayerMap, null=False)

class Match(BaseModel):
    class Meta:
        table_name = f'tfranksystem-match-{stage}'
        region = 'eu-central-1'
        host = 'https://dynamodb.eu-central-1.amazonaws.com'

    def __init__(self, hash_key=None, range_key=None, **args):
        Model.__init__(self, hash_key, range_key, **args)
        if not self.match_id:
            self.match_id = str(uuid.uuid4())

    match_id = UnicodeAttribute(hash_key=True, null=False)
    datetime = UTCDateTimeAttribute(default=datetime.now, range_key=True, null=False)
    teams = ListAttribute(of=TeamMap, null=False)
    ranks = ListAttribute(null=False)

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            if isinstance(attr, MapAttribute):
                yield name, getattr(self, name).as_dict()
            else:
                yield name, attr.serialize(getattr(self, name))

class HistoricalRank(Model):
    class Meta:
        table_name = f'tfranksystem-historicalrank-{stage}'
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
    HistoricalRank.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)