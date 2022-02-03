from functools import wraps
from pyvalid import accepts
import json
import collections
import uuid
from jsonschema import validate
from pprint import pprint
import logging

#
#
@accepts(set)
def validate_form(keys:set=None,partial=False ):
    def inner_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data=None
            request= args[0]
            if not (keys): #keys not present expect an empty request body
                if len(request.body) != 0:
                    raise Exception('Invalid request body')
                else:
                    return func(*args, **kwargs)
            else:
                if len(request.body) == 0:
                        raise Exception('Empty request body')
                if len(request.body) == 0:
                    raise Exception('Empty request body')

                data = json.loads(request.body.decode('utf-8'))  # just json
                if not bool(data):  # empty form
                    raise Exception('Empty dictionary')
                if keys:
                    if not partial:
                        if collections.Counter(data.keys()) != collections.Counter(keys):
                            raise Exception(f'Invalid keys parameters asymmetric difference->{keys.symmetric_difference(set(data.keys()))}\nexpected={list(keys)}  received={list(data.keys())} ')
                    else:
                        if not set(data.keys()).issubset(keys):
                            raise Exception(f'Invalid keys parameters asymmetric difference->{keys.symmetric_difference(set(data.keys()))}\nexpected={list(keys)}  received={list(data.keys())} ')
                args=list(args)
                args.append(data)#add data to args list
                # print(*args, **kwargs)
                return func(*args, **kwargs)#return wrapped func(*args, **kwargs)
        return wrapper
    return inner_decorator


def validate_schema(schema):
    def inner_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                #print('validate_schema',args[1])

                validate(args[1],schema)
            except Exception as e:
                print(e.message)
                raise Exception('bad json schema') #TODO choose the right exception name latter

            return func(*args, **kwargs)#return wrapped func(*args, **kwargs)
        return wrapper
    return inner_decorator


def is_valid_uuid(value):
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False